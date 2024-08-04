package com.peakperformance.peakperformance_backend.user;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.goals.Goals;

@Service
public class UserService implements UserDetailsService{

    private final UserRepository userRepo;
    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public UserService(UserRepository userRepo) {
        this.userRepo = userRepo;
    }


    /*
     * Checks email user wants to sign up with, if already taken, will throw an EmailAlreadyTakenException
     * if not user will become registered
     */
    @Transactional
    public void registerUser(UserRegisterRequest userRegisterRequest) throws EmailAlreadyTakenException {
        Optional<User> userOptional = userRepo.findUserByEmail(userRegisterRequest.getEmail());
        if (userOptional.isPresent()) {
            throw new EmailAlreadyTakenException(userRegisterRequest.getEmail() + " is already taken by another user");
        }

        User user = new User(userRegisterRequest.getEmail(), passwordEncoder.encode(userRegisterRequest.getPassword()));
        userRepo.save(user);
    }


    /*
    * Returns whether password attempt is correct or not
    */
    public boolean isPasswordCorrect(String rawPassword, String encodedPassword) {
        return passwordEncoder.matches(rawPassword, encodedPassword);
    }

    /*
     * Will try to find user by id, will return null if none found with id
     * will throw UserNotFoundException if is null
     */
    public User getUserById(Long id) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findById(id);
        
        if(!userOptional.isPresent()) {
            throw new UserNotFoundException(id + "is not attached to any user");
        }

        User user = userOptional.get();
        return user;
    }

    /*
     * Will try to find user by email, will return null if none found with email
     * will throw UserNotFoundException if is null
     */
    public User getUserByEmail(String email) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findUserByEmail(email);
        if (!userOptional.isPresent()) {
            throw new UserNotFoundException("email not attched to any user");
        }

        User user = userOptional.get();
        return user;
    }

    public void deleteUserById(Long id) {
        userRepo.deleteById(id);
    }

    public List<User> getAllUsers() {
        return userRepo.findAll();
    }

    @Transactional
    //can be used for either updating a users weight or if the didnt put one originally
    public void updateWeightOfUserById(Long id, Integer weight) {
        userRepo.changeWeightOfUserById(id, weight);
    }

    public Integer getUserWeightById(Long id) {
        return userRepo.getWeightOfUserById(id);
    }

    @Transactional
    //can be used for either updating a users current lifts or if they didnt put any originally
    public void updateCurrentLiftsOfUserById(Long id, List<Lift> currentLifts) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findById(id);
        if (!userOptional.isPresent()) {
            throw new UserNotFoundException(id + " not attached to any user");
        }
        User user = userOptional.get();
        user.setCurrentLifts(currentLifts);
        userRepo.save(user);
    }

    @Transactional
    //add more lifts to an already made list or make current lifts lists if null
    public void addLiftToUserCurrentLiftsById(Long id, Lift lift) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findById(id);
        if (!userOptional.isPresent()) {
            throw new UserNotFoundException(id + " not attached to any user");
        }
        User user = userOptional.get();
        List<Lift> currentLifts = user.getCurrentLifts();

        //if user didnt add current lifts originally
        if (currentLifts == null) {
            currentLifts = new ArrayList<>();
            user.setCurrentLifts(currentLifts);
        }
        currentLifts.add(lift);
        userRepo.save(user);
    }

    @Transactional
    //update goals or put goals if not were originall given
    public void addGoalsToUserById(Long id, Goals goal) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findById(id);
        if (!userOptional.isPresent()) {
            throw new UserNotFoundException(id + " not attached to any user");
        }
        User user = userOptional.get();
        user.setGoals(goal);
        userRepo.save(user);
    }

    public List<Lift> getUserCurrentLiftsById(Long id) {
        return userRepo.getCurrentLiftsOfUserById(id);
    }

    public static class EmailAlreadyTakenException extends Exception {

        public EmailAlreadyTakenException(String string) {
            super(string);
        }
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Optional<User> userOptional = userRepo.findUserByEmail(username);
        if (!userOptional.isPresent()) {
            throw new UsernameNotFoundException("email not attched to any user");
        }

        User user = userOptional.get();
        return user;        
    }

    /*
     * Allows for the rest of the user details to be saved in the db
     */
    @Transactional
    public void addUserDetailsById(Long id, User userDetails) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findById(id);
        if (!userOptional.isPresent()) {
            throw new UserNotFoundException(id + " not attached to any user");
        }
        User user = userOptional.get();
        updateUserDeatils(user, userDetails);
        user.getGoals().setLiftGoals(userDetails.getGoals().getLiftGoals());
        user.getGoals().setWeightGoal(userDetails.getGoals().getWeightGoal());
        userRepo.save(user);
    }

    /*
     * Maps all values into the User object in the db
     */
    private void updateUserDeatils(User user, User userDetails) {
        user.setFirstName(userDetails.getFirstName());
        user.setLastName(userDetails.getLastName());
        user.setCurrentLifts(userDetails.getCurrentLifts());
        user.setHeight(userDetails.getHeight());
        user.setWeight(userDetails.getWeight());
        user.setDob(userDetails.getDob());
        
    }

    /*
     * Exception that is thrown when a query looking for a User returns null, meaning they do not exist
     */
    public class UserNotFoundException extends Exception {

        public UserNotFoundException(String string) {
            super(string);
        }
        
    }
    /*
     * Exception that is thrown when the password entered is wrong, when a user tries to log in
     */
    public class InvalidPasswordException extends Exception {

        public InvalidPasswordException(String string) {
            super(string);
        }
    }

}

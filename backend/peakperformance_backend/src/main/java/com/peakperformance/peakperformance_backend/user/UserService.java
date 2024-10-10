package com.peakperformance.peakperformance_backend.user;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercisesession.ExerciseSession;
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
    public ResponseEntity<?> getUserById(Long id) throws UserNotFoundException {
        try {
            User user = isUserPresent(id);
            return new ResponseEntity<>(user, HttpStatus.OK);
        } catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with id: " + id + "not found!", HttpStatus.NOT_FOUND);
        }
    }

    /*
     * Will try to find user by email, will return null if none found with email
     * will throw UserNotFoundException if is null
     */
    public ResponseEntity<?> getUserByEmail(String email)  {
        try {
            User user = isUserPresentByEmail(email);
            return new ResponseEntity<>(user, HttpStatus.OK);
        } catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with email: " + email + " not found!", HttpStatus.NOT_FOUND);
        }
    }

    private User isUserPresentByEmail(String email) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findUserByEmail(email);
        if (userOptional.isEmpty()) {
            throw new UserNotFoundException("email not attached to any user");
        }
        else {
            return userOptional.get();
        }
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
    public ResponseEntity<?> updateCurrentLiftsOfUserById(Long id, List<Lift> currentLifts) {
        try {
            User user = isUserPresent(id);
            user.setCurrentLifts(currentLifts);
            return new ResponseEntity<>(userRepo.save(user), HttpStatus.OK);
        } 
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with id: " + id+ " "+ "does not exist!", HttpStatus.NOT_FOUND);
        }
       
    }

    @Transactional
    //add more lifts to an already made list or make current lifts lists if null
    public ResponseEntity<?> addLiftToUserCurrentLiftsById(Long id, Lift lift) {
        try {
            User user = isUserPresent(id);
            List<Lift> currentLifts = user.getCurrentLifts();
    
            //if user didnt add current lifts originally
            if (currentLifts == null) {
                currentLifts = new ArrayList<>();
                user.setCurrentLifts(currentLifts);
            }
            currentLifts.add(lift);
            return new ResponseEntity<>(userRepo.save(user), HttpStatus.OK);
        } 
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with id: " + id+ " "+ "does not exist!", HttpStatus.NOT_FOUND);
        }
       
    }

    @Transactional
    //update goals or put goals if not were originall given
    public ResponseEntity<?> addGoalsToUserById(Long id, Goals goal) {
        try {
            User user = isUserPresent(id);
            user.setGoals(goal);
            return new ResponseEntity<>(userRepo.save(user), HttpStatus.OK);
        } catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with id: " + id+ " "+ "does not exist!", HttpStatus.NOT_FOUND);
        }
        
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
    public ResponseEntity<?> addUserDetailsById(Long id, User userDetails) {
        try {
            User user = isUserPresent(id);
            updateUserDeatils(user, userDetails);
            if (userDetails.getGoals() != null) {
            updateGoals(user, userDetails);       
            }
            return new ResponseEntity<>(userRepo.save(user), HttpStatus.OK); 
        } catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with id: " + id+ " "+ "does not exist!", HttpStatus.NOT_FOUND);
        }
       
    }

    private void updateGoals(User user, User userDetails) {
        user.getGoals().setLiftGoals(userDetails.getGoals().getLiftGoals());
        user.getGoals().setWeightGoal(userDetails.getGoals().getWeightGoal());
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
     * Adds an exercise session to user via their ID
     */
    @Transactional
    public ResponseEntity<?> addExerciseSessionById(Long id, ExerciseSession exerciseSession) throws UserNotFoundException {
        try {
            User user = isUserPresent(id);
            exerciseSession.setDateTimeofExercise(LocalDateTime.now());
            user.getExerciseSessions().add(exerciseSession);
            return new ResponseEntity<>(userRepo.save(user), HttpStatus.OK); 
        }
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("User with id: " + id+ " "+ "does not exist!", HttpStatus.NOT_FOUND);
        }
    }

    /*
     * Checks if user exists in db based on id
     * gets rid of repeating code
     */
    private User isUserPresent(Long id) throws UserNotFoundException {
        Optional<User> userOptional = userRepo.findById(id);
        if (userOptional.isEmpty()) {
            throw new UserNotFoundException(id + " not attached to any user");
        }
        else {
            return userOptional.get();
        }
    }

    /*
     * Exception that is thrown when a query looking for a User returns null, meaning they do not exist
     */
    public static class UserNotFoundException extends Exception {

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

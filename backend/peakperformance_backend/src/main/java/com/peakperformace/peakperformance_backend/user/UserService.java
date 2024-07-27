package com.peakperformace.peakperformance_backend.user;

import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;
import com.peakperformace.peakperformance_backend.exercise.model.Lift;

@Service
public class UserService {

    private final UserRepository userRepo;

    public UserService(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    //TODO RegisterUser and LoadUserByEmail once auth module finished

    /*
     * Will try to find user by id, will return null if none found with id
     * will throw UserNotFoundException if is null
     */
    public Optional<User> getUserById(Long id) throws UserNotFoundException {
        Optional<User> user = userRepo.findById(id);
        
        if(!user.isPresent()) {
            throw new UserNotFoundException(id + "is not attached to any user");
        }
        return user;
    }

    /*
     * Will try to find user by email, will return null if none found with email
     * will throw UserNotFoundException if is null
     */
    public Optional<User> getUserByEmail(String email) throws UserNotFoundException {
        Optional<User> user = userRepo.findUserByEmail(email);
        if (!user.isPresent()) {
            throw new UserNotFoundException("email not attched to any user");
        }
        return user;
    }

    public void deleteUserById(Long id) {
        userRepo.deleteById(id);
    }

    public List<User> getAllUsers() {
        return userRepo.findAll();
    }

    //can be used for either updating a users weight or if the didnt put one originally
    public void updateWeightOfUserById(Long id, Integer weight) {
        userRepo.changeWeightOfUserById(id, weight);
    }

    public Integer getUserWeightById(Long id) {
        return userRepo.getWeightOfUserById(id);
    }

    //can be used for either updating a users current lifts or if they didnt put any originally
    public void updateCurrentLiftsOfUserById(Long id, List<Lift> currentLifts) {
        userRepo.changeCurrentLiftsOfUserById(id, currentLifts);
    }

    public List<Lift> getUserCurrentLiftsById(Long id) {
        return userRepo.getCurrentLiftsOfUserById(id);
    }

    /*
     * Exception that is thrown when a query looking for a User returns null, meaning they do not exist
     */
    public class UserNotFoundException extends Exception {

        public UserNotFoundException(String string) {
            super(string);
        }
        
    }


}

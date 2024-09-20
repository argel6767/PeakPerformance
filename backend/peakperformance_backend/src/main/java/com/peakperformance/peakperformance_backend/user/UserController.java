package com.peakperformance.peakperformance_backend.user;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercisesession.ExerciseSession;
import com.peakperformance.peakperformance_backend.goals.Goals;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;



@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/id/{userId}")
    public User getUserById(@PathVariable("userId") Long id) {
        try {
            return userService.getUserById(id);
        }
        catch (UserNotFoundException unfe) {
            return null;
        }
    }

    @GetMapping("/email/{email}")
    public User getUserByEmail(@PathVariable("email") String email) throws UserNotFoundException {
        try {
            return userService.getUserByEmail(email);
        }
        catch (UserNotFoundException unfe) {
            return null;
        }  
    }

    @DeleteMapping("/delete/{userId}")
    public String deleteUser(@PathVariable("userId") Long id) {
            userService.deleteUserById(id);
            return "Success!";
    }
    
    @GetMapping("/allusers")
    public List<User> getUsers() {
        return userService.getAllUsers();
    }

    @PutMapping("/{userId}/weight")
    public ResponseEntity<String> addWeightOfUser(@PathVariable("userId") Long id,  @RequestBody Integer weight) {
            userService.updateWeightOfUserById(id, weight);
            return new ResponseEntity<>("Success", HttpStatus.OK);
    }

    @GetMapping("/{userId}/weight")
    public Integer getUserWeightB(@PathVariable("userId")Long id) {
        return userService.getUserWeightById(id);
    }

    @PutMapping("/{userId}/currentlifts")
    public ResponseEntity<String> addCurrentLiftsOfUser(@PathVariable("userId") Long id, @RequestBody List<Lift> currentLifts) {
        try {
            userService.updateCurrentLiftsOfUserById(id, currentLifts);
            return new ResponseEntity<>("Success", HttpStatus.OK);
        }
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("No user found with id " + id, HttpStatus.NOT_FOUND);
        }
    }

    @PutMapping("/{userId}/addlift")
    public ResponseEntity<String> addLiftToCurrentLifts(@PathVariable("userId") Long id, @RequestBody Lift lift) {
        try {
            userService.addLiftToUserCurrentLiftsById(id, lift);
            return new ResponseEntity<>("Success", HttpStatus.OK);
        }
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("No user found with id " + id, HttpStatus.NOT_FOUND);
        }
    }

    @PutMapping("/{userId}/addgoal")
    public ResponseEntity<String> addGoals(@PathVariable("userId") Long id, @RequestBody Goals goal) {        
        try {
            userService.addGoalsToUserById(id, goal);
            return new ResponseEntity<>("Success", HttpStatus.OK);
        }
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("No user found with id " + id, HttpStatus.NOT_FOUND);
        }
    }

    @PutMapping("{userId}/adddetails")
    public ResponseEntity<String> addUserDetails(@PathVariable("userId") Long id, @RequestBody User userDetails) {
        try {
            userService.addUserDetailsById(id, userDetails);
            return new ResponseEntity<>("Success", HttpStatus.OK);
        }
        catch (UserNotFoundException unfe) {
            return new ResponseEntity<>("No user found with id " + id, HttpStatus.NOT_FOUND);
        }
    }

    @PutMapping("/{userId}/addsession")
    public ResponseEntity<String> addExerciseSession(@PathVariable("userId") Long id, @RequestBody ExerciseSession exerciseSession) {
            try {
                userService.addExerciseSessionById(id, exerciseSession);
                return new ResponseEntity<>("Success", HttpStatus.OK);
            }        
            catch(UserNotFoundException unfe) {
                return new ResponseEntity<>("No user found with id " + id, HttpStatus.NOT_FOUND);
            }
    }

}

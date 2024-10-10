package com.peakperformance.peakperformance_backend.user;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercisesession.ExerciseSession;
import com.peakperformance.peakperformance_backend.goals.Goals;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;



@RestController
@RequestMapping("v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/id/{userId}")
    public ResponseEntity<?> getUserById(@PathVariable("userId") Long id) {
        return userService.getUserById(id);
    }

    @GetMapping("/email/{email}")
    public ResponseEntity<?> getUserByEmail(@PathVariable("email") String email) throws UserNotFoundException {
        return userService.getUserByEmail(email);
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
    public ResponseEntity<?> addWeightOfUser(@PathVariable("userId") Long id,  @RequestBody Integer weight) {
        return new ResponseEntity<>("Success", HttpStatus.OK);
    }

    @GetMapping("/{userId}/weight")
    public Integer getUserWeightB(@PathVariable("userId")Long id) {
        return userService.getUserWeightById(id);
    }

    @PutMapping("/{userId}/currentlifts")
    public ResponseEntity<?> addCurrentLiftsOfUser(@PathVariable("userId") Long id, @RequestBody List<Lift> currentLifts) {
        return userService.updateCurrentLiftsOfUserById(id, currentLifts);
    }

    @PutMapping("/{userId}/addlift")
    public ResponseEntity<?> addLiftToCurrentLifts(@PathVariable("userId") Long id, @RequestBody Lift lift) {
            return userService.addLiftToUserCurrentLiftsById(id, lift);
    }

    @PutMapping("/{userId}/addgoal")
    public ResponseEntity<?> addGoals(@PathVariable("userId") Long id, @RequestBody Goals goal) {
        return userService.addGoalsToUserById(id, goal);
    }

    @PutMapping("{userId}/adddetails")
    public ResponseEntity<?> addUserDetails(@PathVariable("userId") Long id, @RequestBody User userDetails) {
        return userService.addUserDetailsById(id, userDetails);
    }

    @PutMapping("/{userId}/addsession")
    public ResponseEntity<?> addExerciseSession(@PathVariable("userId") Long id, @RequestBody ExerciseSession exerciseSession) {
        return userService.addExerciseSessionById(id, exerciseSession);

    }

}

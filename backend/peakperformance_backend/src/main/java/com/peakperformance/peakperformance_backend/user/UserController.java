package com.peakperformance.peakperformance_backend.user;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;


@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/id/{userId}")
    public User getUserById(@PathVariable("userId") Long id) throws UserNotFoundException {
        return userService.getUserById(id);
    }

    @GetMapping("/email/{email}")
    public User getUserByEmail(@PathVariable("email") String email) throws UserNotFoundException {
        return userService.getUserByEmail(email);    
    }

    @DeleteMapping("/delete/{userId}")
    public void deleteUserById(@PathVariable("userId") Long id) {
        userService.deleteUserById(id);
    }

    @GetMapping("/allusers")
    public List<User> getUsers() {
        return userService.getAllUsers();
    }

    @PutMapping("/{userId}/weight")
    public void updateWeightOfUserById(@PathVariable("userId") Long id,  @RequestBody Integer weight) {
        userService.updateWeightOfUserById(id, weight);
    }

    @GetMapping("/{userId}/weight")
    public Integer getUserWeightById(@PathVariable("userId")Long id) {
        return userService.getUserWeightById(id);
    }

    @PutMapping("/{userId}/currentLifts")
    public void updateCurrentLiftsOfUserById(@PathVariable("userId") Long id, @RequestBody List<Lift> currentLifts) throws UserNotFoundException {
        userService.updateCurrentLiftsOfUserById(id, currentLifts);
    }

    @PutMapping("/{userId}/addlift")
    public void addLiftToCurrentLiftsById(@PathVariable Long id, @RequestBody Lift lift) throws UserNotFoundException {
        userService.addLiftToUserCurrentLiftsById(id, lift);
    }
    
}

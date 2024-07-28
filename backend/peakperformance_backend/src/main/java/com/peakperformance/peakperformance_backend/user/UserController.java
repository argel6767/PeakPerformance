package com.peakperformance.peakperformance_backend.user;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;

import org.springframework.web.bind.annotation.PathVariable;


@Controller
@RequestMapping("/users/")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping(path = "{userId}")
    public User getUserById(@PathVariable("userId") Long id) throws UserNotFoundException {
        return userService.getUserById(id);
    }

    @GetMapping(path = "{email}")
    public User getUserByEmail(@PathVariable("email") String email) throws UserNotFoundException {
        return userService.getUserByEmail(email);    
    }

    @DeleteMapping(path = "{userId}")
    public void deleteUserById(@PathVariable("userId") Long id) {
        userService.deleteUserById(id);
    }

    @GetMapping(path = "allusers")
    public List<User> getUsers() {
        return userService.getAllUsers();
    }

    @PutMapping(path = "{userId}/weight")
    public void updateWeightOfUserById(@PathVariable("userId") Long id,  @RequestBody Integer weight) {
        userService.updateWeightOfUserById(id, weight);
    }

    @GetMapping(path = "{userId}/weight")
    public Integer getUserWeightById(@PathVariable("userId")Long id) {
        return userService.getUserWeightById(id);
    }

    @PutMapping(path = "{userId}/currentLifts")
    public void updateCurrentLiftsOfUserById(@PathVariable("userId") Long id, @RequestBody List<Lift> currentLifts) {
        userService.updateCurrentLiftsOfUserById(id, currentLifts);
    }

    @PutMapping(path = "{userId}/addlift")
    public void addLiftToCurrentLiftsById(@PathVariable Long id, @RequestBody Lift lift) throws UserNotFoundException {
        userService.addLiftToUserCurrentLiftsById(id, lift);
    }
    
}

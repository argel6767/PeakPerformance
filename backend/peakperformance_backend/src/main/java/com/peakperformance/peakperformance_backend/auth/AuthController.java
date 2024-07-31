package com.peakperformance.peakperformance_backend.auth;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.peakperformance.peakperformance_backend.user.LoginRequest;
import com.peakperformance.peakperformance_backend.user.User;
import com.peakperformance.peakperformance_backend.user.UserRegisterRequest;
import com.peakperformance.peakperformance_backend.user.UserService;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;
import com.peakperformance.peakperformance_backend.user.UserService.EmailAlreadyTakenException;



@RestController
@RequestMapping("/auth")
public class AuthController {

    private final TokenService tokenService;
    private final UserService userService;

    public AuthController(TokenService tokenService, UserService userService) {
        this.tokenService = tokenService;
        this.userService = userService;
    }

    @PostMapping("/login")
    public String userLoginRequest(@RequestBody LoginRequest loginRequest) {
        String email = loginRequest.getEmail();
        String password = loginRequest.getPassword();
        try { //checks if loginRequest email is attached to user in db

            UserDetails user = userService.getUserByEmail(email);
            if (userService.isPasswordCorrect(password, user.getPassword())) { //verfies password
                return tokenService.generateToken((Authentication) user);
            }
            return "Password incorrect!";
        }
        catch (UserNotFoundException unfe) { //exeption thrown if no user has email
            return "User with email " + loginRequest.getEmail() + " does not exist!";
        }
    }

    @PostMapping("/register")
    public String registerNewUser(@RequestBody UserRegisterRequest userRegisterRequest) {
        String email = userRegisterRequest.getEmail();
        String password = userRegisterRequest.getPassword();
        try { //trys to register user with email and password details
            userService.registerUser(userRegisterRequest);
            UserDetails user = new User(email, password);
            return tokenService.generateToken((Authentication) user); //returns a token if user is sucessfullt registered
        }
        catch (EmailAlreadyTakenException eate) { //throws exception is email has already been used by another user
            return "Email " + email + " is already taken";
        }
    }
    
    
}

package com.peakperformance.peakperformance_backend.auth;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.peakperformance.peakperformance_backend.user.LoginRequest;
import com.peakperformance.peakperformance_backend.user.User;
import com.peakperformance.peakperformance_backend.user.UserService;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;


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
        try { //checks if loginRequest email is attached to user
            User user = userService.getUserByEmail(email);
            if (userService.isPasswordCorrect(password, user.getPassword())) { //verfies password
                return tokenService.generateToken((Authentication) user);
            }
            return "Password incorrect!";
        }
        catch (UserNotFoundException unfe) { //exeption thrown if no user has email
            return "User with email " + loginRequest.getEmail() + " does not exist!";
        }
    }
    
}

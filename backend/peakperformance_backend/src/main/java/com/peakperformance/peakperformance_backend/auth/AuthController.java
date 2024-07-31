package com.peakperformance.peakperformance_backend.auth;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.peakperformance.peakperformance_backend.user.LoginRequest;
import com.peakperformance.peakperformance_backend.user.UserService;


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
        Optional<User
        
        return entity;
    }
    
}

package com.peakperformance.peakperformance_backend.auth;

import org.springframework.context.annotation.Lazy;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
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
    private final AuthenticationManager authenticationManager;
    private UserService userService;


    public AuthController(TokenService tokenService, UserService userService, AuthenticationManager authenticationManager) {
        this.tokenService = tokenService;
        this.authenticationManager = authenticationManager;
        this.userService = userService;
    }

    @PostMapping("/login")
    public String userLoginRequest(@RequestBody LoginRequest loginRequest) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            loginRequest.getEmail(),
                            loginRequest.getPassword()
                    )
            );

            SecurityContextHolder.getContext().setAuthentication(authentication);

            return tokenService.generateToken(authentication);
        } catch (BadCredentialsException e) {
            return "Incorrect Email or Password";
        }
    }

    @PostMapping("/register")
    public String registerNewUser(@RequestBody UserRegisterRequest userRegisterRequest) {

      try { userService.registerUser(userRegisterRequest);
        Authentication authentication = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                    userRegisterRequest.getEmail(),
                    userRegisterRequest.getPassword()
            )
    );
            SecurityContextHolder.getContext().setAuthentication(authentication);
        return tokenService.generateToken(authentication);}
        catch(EmailAlreadyTakenException eate) {
            return "Email: " + userRegisterRequest.getEmail() + " is already taken.";
        }
    }

    
    
}

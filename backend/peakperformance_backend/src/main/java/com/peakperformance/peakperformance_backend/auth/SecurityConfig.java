package com.peakperformance.peakperformance_backend.auth;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import static org.springframework.security.config.Customizer.withDefaults;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable()) // Disable CSRF as tokens are used
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/").permitAll() // 
                .anyRequest().authenticated() // Secure all other endpoints
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS) // Stateless sessions
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(withDefaults()) // Use JWT for OAuth2 Resource Server
            );

        return http.build();
    }

}

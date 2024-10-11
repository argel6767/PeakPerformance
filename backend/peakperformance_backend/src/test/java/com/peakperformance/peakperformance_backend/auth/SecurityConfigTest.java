package com.peakperformance.peakperformance_backend.auth;

import com.peakperformance.peakperformance_backend.user.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;


@ExtendWith(MockitoExtension.class)
class SecurityConfigTest {

    @Mock
    private UserService userService;

    @Mock
    private AuthenticationConfiguration authenticationConfiguration;

    @Mock
    private HttpSecurity httpSecurity;

    private SecurityConfig securityConfig;

    @BeforeEach
    void setUp() {
        securityConfig = new SecurityConfig(userService);
    }

    @Test
    void passwordEncoder_ShouldReturnBCryptPasswordEncoder() {
        // Act
        var encoder = securityConfig.passwordEncoder();

        // Assert
        assertTrue(encoder instanceof BCryptPasswordEncoder);
    }

    @Test
    void authenticationProvider_ShouldConfigureCorrectly() {
        // Act
        DaoAuthenticationProvider provider = securityConfig.authenticationProvider();

        // Assert
        assertNotNull(provider);
        assertInstanceOf(UserService.class, userService);
    }

    @Test
    void authenticationManager_ShouldReturnAuthenticationManager() throws Exception {
        // Arrange
        AuthenticationManager expectedManager = mock(AuthenticationManager.class);
        when(authenticationConfiguration.getAuthenticationManager()).thenReturn(expectedManager);

        // Act
        AuthenticationManager actualManager = securityConfig.authenticationManager(authenticationConfiguration);

        // Assert
        assertSame(expectedManager, actualManager);
        verify(authenticationConfiguration).getAuthenticationManager();
    }

    @Test
    void corsConfigurationSource_ShouldConfigureCorrectly() {
        // Act
        CorsConfigurationSource source = securityConfig.corsConfigurationSource();
        // Assert
        assertNotNull(source);
    }

}
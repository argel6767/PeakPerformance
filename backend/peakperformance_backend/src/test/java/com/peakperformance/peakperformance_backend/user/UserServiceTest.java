package com.peakperformance.peakperformance_backend.user;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;

import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;

//TODO FINSIH THESE ONCE ExerciseSession is merged!!!!!
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @InjectMocks
    UserService userService;
    
    @Mock
    UserRepository userRepository;

    User user;

    @BeforeEach
    void init() {
        user = new User();
        user.setId(1L);
        user.setEmail("example@email.com");
        user.setWeight(23);
    }

    @Test
    void testDeleteUserById() {
        Long userId = 1L;
        Mockito.doNothing().when(userRepository).deleteById(userId);
        userService.deleteUserById(userId);
        Mockito.verify(userRepository, Mockito.times(1)).deleteById(userId);
    }

    @Test
    void testGetAllUsers() {
        
    }

    @Test
    void testGetUserByEmailWithValidEmail() throws UserNotFoundException {
        when(userRepository.findUserByEmail(user.getEmail())).thenReturn(Optional.of(user));
        User foundUser = userService.getUserByEmail(user.getEmail());
        assertTrue(foundUser != null);
        assertTrue(foundUser instanceof User);
        assertEquals(user.getEmail(), foundUser.getEmail());
    }

    @Test
    void testGetUserByEmailWithInvalidEmailThrowsUserNotFoundException() {
        when(userRepository.findUserByEmail("InvalidEmail@email.com")).thenReturn(Optional.empty());
        assertThrows(UserNotFoundException.class, () -> {
            userService.getUserByEmail("InvalidEmail@email.com");
        }, "UserNotFoundException should have been thrown!");
        verify(userRepository, times(1)).findUserByEmail("InvalidEmail@email.com");
    }
    @Test
    public void testGetUserByIdWithValidId() throws UserNotFoundException {
        Mockito.when(userRepository.findById(user.getId())).thenReturn(Optional.of(user));
        User foundUser = userService.getUserById(user.getId());
        assertNotNull(foundUser);
        assertEquals(user.getId(), foundUser.getId());
        assertEquals("example@email.com", foundUser.getEmail());
    }

    @Test
    void testGetUserByIdWithInvalidIdThrowsUserNotFoundException() {
        when(userRepository.findById(2L)).thenReturn(Optional.empty());
        assertThrows(UserNotFoundException.class, () -> {
            userService.getUserById(2L);
        }, "UserNotFoundException should have been thrown!");

    }

    @Test
    void testGetUserCurrentLiftsById() {

    }

    @Test
    void testGetUserWeightById() {

    }

    @Test
    void testUpdateCurrentLiftsOfUserById() {

    }

    @Test
    void testUpdateWeightOfUserById() {

    }
}

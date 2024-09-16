package com.peakperformance.peakperformance_backend.user;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercise.model.WeightReps;
import com.peakperformance.peakperformance_backend.user.UserService.UserNotFoundException;

//TODO FINSIH THESE ONCE ExerciseSession is merged!!!!!
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @InjectMocks
    UserService userService;
    
    @Mock
    UserRepository userRepository;

    User user;
    User user2;

    @BeforeEach
    void init() {
        user = new User();
        user.setId(1L);
        user.setEmail("example@email.com");
        user.setWeight(56);
        
        user2 = new User();
        user2.setId(3L);
        user2.setEmail("email@email.com");
        user2.setWeight(25);
        user2.setCurrentLifts(List.of(new Lift("Bench Press",  List.of(new WeightReps(500,2))),
        new Lift("DeadLift",  List.of(new WeightReps(100,64)))));
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
        when(userRepository.findAll()).thenReturn(List.of(user, user2));
        List<User> users = userService.getAllUsers();
        assertNotNull(users);
        assertEquals(2, users.size());
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
        verify(userRepository, times(1)).findById(2L);
    }

    @Test
    void testGetUserCurrentLiftsByIdWithValidId() {
        when(userRepository.getCurrentLiftsOfUserById(user2.getId())).thenReturn(user2.getCurrentLifts());
        List<Lift> currentLifts = userService.getUserCurrentLiftsById(user2.getId());
        assertTrue(currentLifts.size() == 2);
        assertEquals(user2.getCurrentLifts(), currentLifts);
        verify(userRepository, times(1)).getCurrentLiftsOfUserById(user2.getId());
    }

    @Test
    void testGetUserCurrentLiftsByIdWithValidButNoLiftsReturnsNull() {
        when(userRepository.getCurrentLiftsOfUserById(user.getId())).thenReturn(null);
        List<Lift> currtLifts = userService.getUserCurrentLiftsById(user.getId());
        assertNull(currtLifts);
        verify(userRepository, times(1)).getCurrentLiftsOfUserById(user.getId());
    }

    @Test
    void testGetUserWeightById() {
        when(userRepository.getWeightOfUserById(user2.getId())).thenReturn(user2.getWeight());
        Integer weight = userService.getUserWeightById(user2.getId());
        assertEquals(user2.getWeight(), weight);
        verify(userRepository, times(1)).getWeightOfUserById(user2.getId());
    }

    @Test
    void testUpdateCurrentLiftsOfUserById() {
    
    }

    @Test
    void testUpdateWeightOfUserById() {
        doNothing().when(userRepository).changeWeightOfUserById(user.getId(), 23);
        userService.updateWeightOfUserById(user.getId(), 23);
        verify(userRepository, times(1)).changeWeightOfUserById(user.getId(), 23);
    }
}

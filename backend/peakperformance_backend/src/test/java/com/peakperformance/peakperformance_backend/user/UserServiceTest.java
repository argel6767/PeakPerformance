package com.peakperformance.peakperformance_backend.user;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercisesession.ExerciseSession;
import com.peakperformance.peakperformance_backend.goals.Goals;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @Mock
    private UserRepository userRepo;

    @InjectMocks
    private UserService userService;


    /**
     * Test registering a user when the email is already taken.
     */
    @Test
    public void testRegisterUser_EmailAlreadyTaken() {
        // Arrange
        UserRegisterRequest request = new UserRegisterRequest("test@example.com", "password");
        when(userRepo.findUserByEmail("test@example.com")).thenReturn(Optional.of(new User()));
        // Act & Assert
        assertThrows(UserService.EmailAlreadyTakenException.class, () -> {
            userService.registerUser(request);
        });
        verify(userRepo, never()).save(any(User.class));
    }

    /**
     * Test registering a user successfully.
     */
    @Test
    public void testRegisterUser_Success() throws Exception {
        // Arrange
        UserRegisterRequest request = new UserRegisterRequest("test@example.com","password");
        when(userRepo.findUserByEmail("test@example.com")).thenReturn(Optional.empty());
        // Act
        userService.registerUser(request);
        // Assert
        verify(userRepo).save(any(User.class));
    }

    /**
     * Test retrieving a user by ID when the user is found.
     */
    @Test
    public void testGetUserById_UserFound() {
        // Arrange
        Long userId = 1L;
        User user = new User();
        user.setId(userId);
        when(userRepo.findById(userId)).thenReturn(Optional.of(user));
        // Act
        ResponseEntity<?> response = userService.getUserById(userId);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
    }

    /**
     * Test retrieving a user by ID when the user is not found.
     */
    @Test
    public void testGetUserById_UserNotFound() {
        // Arrange
        Long userId = 1L;
        // Act
        ResponseEntity<?> response = userService.getUserById(userId);
        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with id: 1not found!", response.getBody());
    }

    /**
     * Test retrieving a user by email when the user is found.
     */
    @Test
    public void testGetUserByEmail_UserFound() {
        // Arrange
        String email = "test@example.com";
        User user = new User();
        user.setEmail(email);
        when(userRepo.findUserByEmail(email)).thenReturn(Optional.of(user));
        // Act
        ResponseEntity<?> response = userService.getUserByEmail(email);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
    }

    /**
     * Test retrieving a user by email when the user is not found.
     */
    @Test
    public void testGetUserByEmail_UserNotFound() {
        // Arrange
        String email = "test@example.com";
        // Act
        ResponseEntity<?> response = userService.getUserByEmail(email);
        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with email: test@example.com not found!", response.getBody());
    }

    /**
     * Test deleting a user by ID.
     */
    @Test
    public void testDeleteUserById() {
        // Arrange
        Long userId = 1L;
        // Act
        userService.deleteUserById(userId);
        // Assert
        verify(userRepo).deleteById(userId);
    }

    /**
     * Test retrieving all users.
     */
    @Test
    public void testGetAllUsers() {
        // Arrange
        List<User> users = Arrays.asList(new User(), new User());
        when(userRepo.findAll()).thenReturn(users);
        // Act
        List<User> result = userService.getAllUsers();
        // Assert
        assertEquals(users, result);
    }

    /**
     * Test updating the weight of a user by ID.
     */
    @Test
    public void testUpdateWeightOfUserById() {
        // Arrange
        Long userId = 1L;
        Integer weight = 70;
        // Act
        userService.updateWeightOfUserById(userId, weight);
        // Assert
        verify(userRepo).changeWeightOfUserById(userId, weight);
    }

    /**
     * Test retrieving the weight of a user by ID.
     */
    @Test
    public void testGetUserWeightById() {
        // Arrange
        Long userId = 1L;
        Integer weight = 70;
        when(userRepo.getWeightOfUserById(userId)).thenReturn(weight);
        // Act
        Integer result = userService.getUserWeightById(userId);
        // Assert
        assertEquals(weight, result);
    }

    /**
     * Test updating current lifts of a user when the user exists.
     */
    @Test
    public void testUpdateCurrentLiftsOfUserById_UserExists() {
        // Arrange
        Long userId = 1L;
        List<Lift> currentLifts = Arrays.asList(new Lift(), new Lift());
        User user = new User();
        user.setId(userId);
        when(userRepo.findById(userId)).thenReturn(Optional.of(user));
        when(userRepo.save(user)).thenReturn(user);
        // Act
        ResponseEntity<?> response = userService.updateCurrentLiftsOfUserById(userId, currentLifts);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
        assertEquals(currentLifts, user.getCurrentLifts());
        verify(userRepo).save(user);
    }

    /**
     * Test updating current lifts of a user when the user does not exist.
     */
    @Test
    public void testUpdateCurrentLiftsOfUserById_UserNotFound() {
        // Arrange
        Long userId = 1L;
        List<Lift> currentLifts = Arrays.asList(new Lift(), new Lift());
        // Act
        ResponseEntity<?> response = userService.updateCurrentLiftsOfUserById(userId, currentLifts);
        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with id: 1 does not exist!", response.getBody());
        verify(userRepo, never()).save(any(User.class));
    }

    /**
     * Test adding a lift to a user's current lifts when the user exists.
     */
    @Test
    public void testAddLiftToUserCurrentLiftsById_UserExists() {
        // Arrange
        Long userId = 1L;
        Lift lift = new Lift();
        User user = new User();
        user.setId(userId);
        user.setCurrentLifts(new ArrayList<>());
        when(userRepo.findById(userId)).thenReturn(Optional.of(user));
        when(userRepo.save(user)).thenReturn(user);
        // Act
        ResponseEntity<?> response = userService.addLiftToUserCurrentLiftsById(userId, lift);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
        assertTrue(user.getCurrentLifts().contains(lift));
        verify(userRepo).save(user);
    }

    /**
     * Test adding a lift to a user's current lifts when the user does not exist.
     */
    @Test
    public void testAddLiftToUserCurrentLiftsById_UserNotFound() {
        // Arrange
        Long userId = 1L;
        Lift lift = new Lift();
        // Act
        ResponseEntity<?> response = userService.addLiftToUserCurrentLiftsById(userId, lift);
        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with id: 1 does not exist!", response.getBody());
        verify(userRepo, never()).save(any(User.class));
    }

    /**
     * Test adding goals to a user when the user exists.
     */
    @Test
    public void testAddGoalsToUserById_UserExists() {
        // Arrange
        Long userId = 1L;
        Goals goals = new Goals();
        User user = new User();
        user.setId(userId);
        when(userRepo.findById(userId)).thenReturn(Optional.of(user));
        when(userRepo.save(user)).thenReturn(user);
        // Act
        ResponseEntity<?> response = userService.addGoalsToUserById(userId, goals);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
        assertEquals(goals, user.getGoals());
        verify(userRepo).save(user);
    }

    /**
     * Test adding goals to a user when the user does not exist.
     */
    @Test
    public void testAddGoalsToUserById_UserNotFound() {
        // Arrange
        Long userId = 1L;
        Goals goals = new Goals();
        // Act
        ResponseEntity<?> response = userService.addGoalsToUserById(userId, goals);

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with id: 1 does not exist!", response.getBody());
        verify(userRepo, never()).save(any(User.class));
    }

    /**
     * Test retrieving a user's current lifts by ID.
     */
    @Test
    public void testGetUserCurrentLiftsById() {
        // Arrange
        Long userId = 1L;
        List<Lift> lifts = Arrays.asList(new Lift(), new Lift());
        when(userRepo.getCurrentLiftsOfUserById(userId)).thenReturn(lifts);
        // Act
        List<Lift> result = userService.getUserCurrentLiftsById(userId);
        // Assert
        assertEquals(2, result.size());
    }


    /**
     * Test loading a user by username (email) when the user is not found.
     */
    @Test
    public void testLoadUserByUsername_UserNotFound() {
        // Arrange
        String email = "test@example.com";
        // Act & Assert
        assertThrows(UsernameNotFoundException.class, () -> {
            userService.loadUserByUsername(email);
        });
    }

    /**
     * Test adding user details by ID when the user exists.
     */
    @Test
    public void testAddUserDetailsById_UserExists() {
        // Arrange
        Long userId = 1L;
        User userDetails = new User();
        userDetails.setFirstName("John");
        userDetails.setLastName("Doe");
        userDetails.setHeight(180);
        userDetails.setWeight(75);
        userDetails.setDob(LocalDate.now());
        User user = new User();
        user.setId(userId);
        when(userRepo.findById(userId)).thenReturn(Optional.of(user));
        when(userRepo.save(user)).thenReturn(user);
        // Act
        ResponseEntity<?> response = userService.addUserDetailsById(userId, userDetails);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
        assertEquals("John", user.getFirstName());
        assertEquals("Doe", user.getLastName());
        verify(userRepo).save(user);
    }

    /**
     * Test adding user details by ID when the user does not exist.
     */
    @Test
    public void testAddUserDetailsById_UserNotFound() {
        // Arrange
        Long userId = 1L;
        User userDetails = new User();
        // Act
        ResponseEntity<?> response = userService.addUserDetailsById(userId, userDetails);
        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with id: 1 does not exist!", response.getBody());
        verify(userRepo, never()).save(any(User.class));
    }

    /**
     * Test adding an exercise session to a user when the user exists.
     */
    @Test
    public void testAddExerciseSessionById_UserExists() {
        // Arrange
        Long userId = 1L;
        ExerciseSession session = new ExerciseSession();
        User user = new User();
        user.setId(userId);
        user.setExerciseSessions(new ArrayList<>());
        when(userRepo.findById(userId)).thenReturn(Optional.of(user));
        when(userRepo.save(user)).thenReturn(user);
        // Act
        ResponseEntity<?> response = userService.addExerciseSessionById(userId, session);
        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
        assertEquals(1, user.getExerciseSessions().size());
        verify(userRepo).save(user);
    }

    /**
     * Test adding an exercise session to a user when the user does not exist.
     */
    @Test
    public void testAddExerciseSessionById_UserNotFound() {
        // Arrange
        Long userId = 1L;
        ExerciseSession session = new ExerciseSession();
        // Act
        ResponseEntity<?> response = userService.addExerciseSessionById(userId, session);
        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("User with id: 1 does not exist!", response.getBody());
        verify(userRepo, never()).save(any(User.class));
    }
}

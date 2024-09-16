package com.peakperformance.peakperformance_backend.user;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;

//TODO FINSIH THESE ONCE ExerciseSession is merged!!!!!
@ExtendWith(MockitoExtension.class)
@SpringBootTest
public class UserServiceTest {

    @InjectMocks
    UserService userService;
    
    @Mock
    UserRepository userRepository;

    User user;

    @BeforeEach
    void init() {
        user = new User();
    }

    @Test
    void testDeleteUserById() {

    }

    @Test
    void testGetAllUsers() {

    }

    @Test
    void testGetUserByEmail() {

    }
    /*@Test
    public void testGetUserById() throws UserNotFoundException {
        Long userId = 1L;
        user.setId(userId);
        user.setEmail("test@example.com");

        Mockito.when(userRepository.findById(userId)).thenReturn(Optional.of(user));

        User foundUser = userService.getUserById(userId);

        assertNotNull(foundUser);

        assertEquals(userId, foundUser.getId());
        assertEquals("test@example.com", foundUser.getEmail());
    }*/

    @Test
    void testGetUserByIdThrowsUserNotFoundException() {
        user.setId(Long.valueOf(2));

        //Mockito.when(userService.getUserById(null))

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

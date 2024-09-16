package com.peakperformance.peakperformance_backend.user;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;


@WebMvcTest(UserController.class)
public class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService; // Mock dependency
    @Test
    void testAddLiftById() {

    }

    @Test
    void testDeleteUserById() {

    }

    @Test
    void testGetUserByEmail() {

    }

    @Test
    void testGetUserById() {

    }

    @Test
    void testGetUserWeightById() {

    }

    @Test
    void testGetUsers() {

    }

    @Test
    void testUpdateCurrentLiftsOfUserById() {

    }

    @Test
    void testUpdateWeightOfUserById() {

    }
}

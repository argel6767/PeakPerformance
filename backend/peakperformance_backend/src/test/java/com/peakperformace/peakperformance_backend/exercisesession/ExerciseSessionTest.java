package com.peakperformace.peakperformance_backend.exercisesession;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

import com.peakperformace.peakperformance_backend.exercise.Exercise;
import com.peakperformace.peakperformance_backend.exercise.model.WeightReps;
import com.peakperformace.peakperformance_backend.exercise.model.WorkoutType;
import com.peakperformace.peakperformance_backend.user.User;

public class ExerciseSessionTest {
    
    //make a set of a workout
    WeightReps latPulldown = new WeightReps(160, 10);
    List<WeightReps> set1 = List.of(latPulldown);

    //make a exercise
    Exercise lateralPulldown = new Exercise("Lateral Pulldown", WorkoutType.BACK);

    //make a user
    User user1 = new User("Jerry", "Roberts", "Jrob10@gmail.com", "HelloWorld", LocalDate.of(2006, 03, 30), 5, 205);

    @Test
    void testExerciseSessionCreation(){

    ExerciseSession exerciseSession = new ExerciseSession(LocalDateTime.of(2024, 06, 05, 5, 20), set1, lateralPulldown, user1);
    assertEquals(LocalDateTime.of(2024, 06,  05, 5, 20), exerciseSession.getDateTimeofExercise());
    assertEquals(set1, exerciseSession.getSets());
    assertEquals(lateralPulldown, exerciseSession.getExercise());
    assertEquals(user1, exerciseSession.getUser());
    }
}

package com.peakperformace.peakperformance_backend.exercise;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.peakperformace.peakperformance_backend.exercise.model.Exercise;
import com.peakperformace.peakperformance_backend.exercise.model.WorkoutType;

public class ExerciseTest {
    
    @Test
    void testExerciseCreation(){

    Exercise exercise = new Exercise("Lateral Pulldown", WorkoutType.BACK);
    assertEquals("Lateral Pulldown", exercise.getName());
    assertEquals(WorkoutType.BACK, exercise.getWorkoutType());
    }

}

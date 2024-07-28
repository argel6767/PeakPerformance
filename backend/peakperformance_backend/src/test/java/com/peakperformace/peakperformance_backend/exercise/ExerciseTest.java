package com.peakperformace.peakperformance_backend.exercise;

import org.junit.jupiter.api.Test;

import com.peakperformance.peakperformance_backend.exercise.Exercise;
import com.peakperformance.peakperformance_backend.exercise.model.WorkoutType;

import static org.junit.jupiter.api.Assertions.*;

public class ExerciseTest {
    
    @Test
    void testExerciseCreation(){

    Exercise exercise = new Exercise("Lateral Pulldown", WorkoutType.BACK);
    assertEquals("Lateral Pulldown", exercise.getName());
    assertEquals(WorkoutType.BACK, exercise.getWorkoutType());
    }

}

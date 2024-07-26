package com.peakperformace.peakperformance_backend.exercisesession;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

import org.junit.jupiter.api.Test;

import com.peakperformace.peakperformance_backend.exercise.Exercise;
import com.peakperformace.peakperformance_backend.exercise.model.WeightReps;
import com.peakperformace.peakperformance_backend.exercise.model.WorkoutType;

public class ExerciseSessionTest {
    
    //make a set of a workout
    WeightReps latPulldown = new WeightReps(160, 10);
    List<WeightReps> set1 = List.of(latPulldown);

    //make a exercise
    Exercise lateralPulldown = new Exercise("Lateral Pulldown", WorkoutType.BACK);

    @Test
    void testExerciseSessionCreation(){

    ExerciseSession exerciseSession = new ExerciseSession(LocalTime.of(5,10), LocalDate.of(2024, 6, 18), set1, lateralPulldown);
    assertEquals(LocalTime.of(5,10), exerciseSession.getTimeOfExercise());
    assertEquals(LocalDate.of(2024, 6, 18), exerciseSession.getDateOfExercise());
    assertEquals(set1, exerciseSession.getSets());
    assertEquals(lateralPulldown, exerciseSession.getExercise());

    }
}

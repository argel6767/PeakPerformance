package com.peakperformace.peakperformance_backend.goals;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import com.peakperformace.peakperformance_backend.exercise.liftmodel.*;

public class GoalsTest {

    Goals goals;

    @Test
    void testGetLiftGoalsIfNull() {
        goals = new Goals(1);
        assertTrue(goals.getLiftGoals()==null);  
    }

    @Test
    void testGetWeightGoalIfNull() {
    //pretend lifting goals
    WeightReps bench = new WeightReps(100, 10);
    WeightReps squat = new WeightReps(300, 4);

    //holding the sets in their own list
        List<WeightReps> set1 = List.of(bench);
        List<WeightReps> set2 = List.of(squat);

        // make Lift object for each lift goal
        Lift benchPressLift = new Lift("bench press", set1);
        Lift squatLift = new Lift("squat", set2);

        goals = new Goals(List.of(benchPressLift, squatLift));
        assertTrue(goals.getWeightGoal() == null);
    }
}

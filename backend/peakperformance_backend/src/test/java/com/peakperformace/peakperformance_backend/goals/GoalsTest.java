package com.peakperformace.peakperformance_backend.goals;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import com.peakperformance.peakperformance_backend.exercise.model.*;
import com.peakperformance.peakperformance_backend.goals.Goals;

public class GoalsTest {

    Goals goals;
    //pretend lifting goals
    WeightReps bench = new WeightReps(100, 10);
    WeightReps squat = new WeightReps(300, 4);
    
    //holding the sets in their own list
    List<WeightReps> set1 = List.of(bench);
    List<WeightReps> set2 = List.of(squat);
    
    // make Lift object for each lift goal
    Lift benchPressLift = new Lift("bench press", 100, 10);
    Lift squatLift = new Lift("squat", 100, 10);
    List<Lift> liftingGoals = List.of(benchPressLift, squatLift);

    @Test
    void testIfBothGoalsAreNotNull() {
        goals = new Goals(1, liftingGoals);
        assertEquals("both goals set", goals.overallGoalsStatus());
    }

    @Test
    void testIfWeightGoalIsNull() {

        goals = new Goals(liftingGoals);

        assertTrue(goals.getWeightGoal() == null);
        assertEquals("weight goal not set", goals.weightGoalStatus());
        assertEquals("only lift goals set", goals.overallGoalsStatus());
    }

    @Test
    void testIfLiftGoalsIsNull() {
        goals = new Goals(1);

        assertTrue(goals.getLiftGoals()==null);
        assertEquals("lift goals not set", goals.liftGoalStatus()); 
        assertEquals("only weight goal set", goals.overallGoalsStatus());
    }


    @Test 
    void testIfBothLiftGoalsAndWeightGoalAreNull() {
        goals = new Goals();

        assertTrue(goals.getWeightGoal() == null && goals.getLiftGoals() == null);
        assertEquals("no goals set", goals.overallGoalsStatus());
    }
}

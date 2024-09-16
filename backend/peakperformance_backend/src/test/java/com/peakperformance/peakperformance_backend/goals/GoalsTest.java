package com.peakperformance.peakperformance_backend.goals;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercise.model.WeightReps;

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
    void testIfBothGoalsAreGiven() {
        goals = new Goals(1, liftingGoals);
        assertEquals("both goals set", goals.overallGoalsStatus());
    }

    @Test
    void testIfWeightGoalIsNullWhenNoneIsGiven() {

        goals = new Goals(liftingGoals);

        assertTrue(goals.getWeightGoal() == null);
        assertEquals("weight goal not set", goals.weightGoalStatus());
        assertEquals("only lift goals set", goals.overallGoalsStatus());
    }

    @Test
    void testIfLiftGoalsAreEmptyWhenNoneAreGiven() {
        goals = new Goals(1);

        assertTrue(goals.getLiftGoals().size() == 0);
        assertEquals("lift goals not set", goals.liftGoalStatus()); 
        assertEquals("only weight goal set", goals.overallGoalsStatus());
    }


    @Test 
    void testIfBothLiftGoalsAndWeightGoalAreNotPresntWhenNeitherAreGiven() {
        goals = new Goals();

        assertTrue(goals.getWeightGoal() == null && goals.getLiftGoals().size() == 0);
        assertEquals("no goals set", goals.overallGoalsStatus());
    }
}

package com.peakperformace.peakperformance_backend.exercise.liftmodel;

import java.util.List;


/*The exercise name and the  weight and reps done per set where a set is the index of a cell in sets + 1*/
public class Lift {
    private String exerciseName;
    private List<WeightReps> sets;

    public Lift(String exerciseName, List<WeightReps> sets) {
        this.exerciseName = exerciseName;
        this.sets = sets;
    }

    public String getExerciseName() {
        return exerciseName;
    }

    public void setExerciseName(String exerciseName) {
        this.exerciseName = exerciseName;
    }

    public List<WeightReps> getSets() {
        return sets;
    }

    public void setSets(List<WeightReps> sets) {
        this.sets = sets;
    }
    
}

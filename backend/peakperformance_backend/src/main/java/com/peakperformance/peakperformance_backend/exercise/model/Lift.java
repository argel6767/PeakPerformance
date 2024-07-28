package com.peakperformance.peakperformance_backend.exercise.model;

import java.util.List;
import java.util.ArrayList;


/*The exercise name and the  weight and reps done per set where a set is the index of a cell in sets + 1*/
public class Lift {
    private String exerciseName;
    private List<WeightReps> sets = new ArrayList<>();

    @Override
    public String toString() {
        return "Lift [exerciseName=" + exerciseName + ", sets =" + setsToString() + "]";
    }

    public Lift(){}

    public Lift(String exerciseName, int weight, int reps) {
        this.exerciseName = exerciseName;
        this.sets.add(new WeightReps(weight, reps));
    }

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

    //actual WeightReps object alreadt made
    public void addSet(WeightReps set) {
        this.sets.add(set);
    }

    //raw values
    public void addSet(int weight, int reps) {
        this.sets.add(new WeightReps(weight, reps));
    }

    public String setsToString() {
        String weightAndReps = "";
        for (WeightReps set: sets) {
            weightAndReps += set.toString() + ", ";
        }
        return weightAndReps;
    }


}

package com.peakperformace.peakperformance_backend.exercise.liftmodel;

/*
 * Thw weight and reps done for a single set
 */
public class WeightReps {
    private int weight;
    private int reps;

    public WeightReps(int weight, int reps) {
        this.weight = weight;
        this.reps = reps;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }

    public int getReps() {
        return reps;
    }

    public void setReps(int reps) {
        this.reps = reps;
    }
    
    
}

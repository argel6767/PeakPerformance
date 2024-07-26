package com.peakperformace.peakperformance_backend.exercise.model;

/*
 * The weight and reps done for a single set
 */
public class WeightReps {
    private int weight;
    private int reps;


    public WeightReps(){}

    public WeightReps(int weight, int reps) {
        this.weight = weight;
        this.reps = reps;
    }

    @Override
        public String toString() {
            return " [weight=" + weight + ", reps=" + reps + "]";
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

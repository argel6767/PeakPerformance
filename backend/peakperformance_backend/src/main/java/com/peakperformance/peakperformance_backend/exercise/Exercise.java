package com.peakperformance.peakperformance_backend.exercise;

import com.peakperformance.peakperformance_backend.exercise.model.WorkoutType;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;

@Entity
@Table

public class Exercise {
    @Id
    @SequenceGenerator (
        name = "exercise_sequence",
        sequenceName = "exercise_sequence",
        allocationSize = 1
    )
    @GeneratedValue (
        strategy = GenerationType.SEQUENCE,
        generator = "exersize_sequence"
    )
    private Long id;
    
    private String name;

    @Enumerated(EnumType.STRING)
    private WorkoutType workoutType;

    public Exercise(){}
    
    public Exercise(String name, WorkoutType workoutType) {
        this.name = name;
        this.workoutType = workoutType;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public WorkoutType getWorkoutType() {
        return workoutType;
    }

    public void setWorkoutType(WorkoutType workoutType) {
        this.workoutType = workoutType;
    }

}

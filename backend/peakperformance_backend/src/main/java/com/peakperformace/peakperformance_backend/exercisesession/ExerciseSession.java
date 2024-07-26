package com.peakperformace.peakperformance_backend.exercisesession;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

import com.peakperformace.peakperformance_backend.exercise.Exercise;
import com.peakperformace.peakperformance_backend.exercise.model.WeightReps;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.SequenceGenerator;

@Entity
@Table

public class ExerciseSession {
    @Id
    @SequenceGenerator (
        name = "exercisesession_sequence",
        sequenceName = "exercisesession_sequence",
        allocationSize = 1
    )
    @GeneratedValue (
        strategy = GenerationType.SEQUENCE,
        generator = "exercisesession_sequence"
    )

    private LocalTime timeOfExercise;
    private LocalDate dateOfExercise;
    
    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "exercise_id", nullable = false)
    private Exercise exercise;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = Object.class)//placehold until JsonConver class is made
    private List<WeightReps> sets;
    
    public ExerciseSession(LocalTime timeOfExercise, LocalDate dateOfExercise, List<WeightReps> sets,
            Exercise exercise) {
        this.timeOfExercise = timeOfExercise;
        this.dateOfExercise = dateOfExercise;
        this.sets = sets;
        this.exercise = exercise;

    }

    public LocalTime getTimeOfExercise() {
        return timeOfExercise;
    }

    public void setTimeOfExercise(LocalTime timeOfExercise) {
        this.timeOfExercise = timeOfExercise;
    }

    public LocalDate getDateOfExercise() {
        return dateOfExercise;
    }

    public void setDateOfExercise(LocalDate dateOfExercise) {
        this.dateOfExercise = dateOfExercise;
    }

    public Exercise getExercise() {
        return exercise;
    }

    public void setExercise(Exercise exercise) {
        this.exercise = exercise;
    }

    public List<WeightReps> getSets() {
        return sets;
    }

    public void setSets(List<WeightReps> sets) {
        this.sets = sets;
    }

}

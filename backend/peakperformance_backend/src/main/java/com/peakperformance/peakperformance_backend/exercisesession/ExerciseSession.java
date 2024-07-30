package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.List;

import com.peakperformance.peakperformance_backend.converter.JSONBConverter;
import com.peakperformance.peakperformance_backend.exercise.Exercise;
import com.peakperformance.peakperformance_backend.exercise.model.WeightReps;
import com.peakperformance.peakperformance_backend.user.User;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
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

    private LocalDateTime dateTimeofExercise;
    
    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "exercise_id", nullable = false)
    private Exercise exercise;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = JSONBConverter.class)
    private List<WeightReps> sets;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
    
    public ExerciseSession(LocalDateTime dateTimeofExercise, List<WeightReps> sets,
            Exercise exercise) {
        this.dateTimeofExercise = dateTimeofExercise;
        this.sets = sets;
        this.exercise = exercise;

    }

    public LocalDateTime getDateTimeofExercise() {
        return dateTimeofExercise;
    }

    public void setDateTimeofExercise(LocalDateTime dateTimeofExercise) {
        this.dateTimeofExercise = dateTimeofExercise;
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
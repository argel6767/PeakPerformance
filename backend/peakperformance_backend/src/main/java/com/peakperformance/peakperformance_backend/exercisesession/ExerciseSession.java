package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.Type;

import com.peakperformance.peakperformance_backend.converter.JSONBConverter;
import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.exercise.model.WorkoutType;
import com.peakperformance.peakperformance_backend.user.User;

import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.Column;
import jakarta.persistence.Convert;
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
    private Long id;
    
    @Enumerated(EnumType.STRING)
    private WorkoutType workoutType;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = JSONBConverter.class)
    @Type(JsonType.class)
    private Lift lift;

    

    @CreationTimestamp
    private LocalDateTime dateTimeofExercise;

    public ExerciseSession(){}
    
    public ExerciseSession(WorkoutType workoutType, Lift lift, User user) {
        this.workoutType = workoutType;
        this.lift = lift;
    }
    
    public LocalDateTime getDateTimeofExercise() {
        return dateTimeofExercise;
    }

    public void setDateTimeofExercise(LocalDateTime dateTimeofExercise) {
        this.dateTimeofExercise = dateTimeofExercise;
    }

    public void setExercise(WorkoutType workoutType) {
        this.workoutType = workoutType;
    }

    public Lift getLift() {
        return lift;
    }

    public void setLift(Lift lift) {
        this.lift = lift;
    }



    public WorkoutType getWorkoutType() {
        return workoutType;
    }

    public void setWorkoutType(WorkoutType workoutType) {
        this.workoutType = workoutType;
    }
}

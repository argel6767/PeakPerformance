package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.Type;

import com.peakperformance.peakperformance_backend.converter.JSONBConverter;
import com.peakperformance.peakperformance_backend.exercise.Exercise;
import com.peakperformance.peakperformance_backend.exercise.model.WeightReps;
import com.peakperformance.peakperformance_backend.user.User;

import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToOne;
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
    
    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "exercise_id")
    private Exercise exercise;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = JSONBConverter.class)
    @Type(JsonType.class)
    private List<WeightReps> sets = new ArrayList<>();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @CreationTimestamp
    private LocalDateTime dateTimeofExercise;

    public ExerciseSession(){}
    
    public ExerciseSession(List<WeightReps> sets,
            Exercise exercise, User user, Long id) {
        this.sets = sets;
        this.exercise = exercise;
        this.user = user;
        this.id = id;
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

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

}

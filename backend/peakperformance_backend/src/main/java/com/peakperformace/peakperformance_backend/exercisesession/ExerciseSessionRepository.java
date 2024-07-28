package com.peakperformace.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.peakperformace.peakperformance_backend.exercise.Exercise;
import com.peakperformace.peakperformance_backend.user.User;


public interface ExerciseSessionRepository extends JpaRepository<ExerciseSession, LocalDateTime> {

    //finds an exercise session by datetime
    @Query("SELECT es FROM ExerciseSession es WHERE es.date_performed = 06-10-2024")
    public Exercise findByDateTimeofExercise(LocalDateTime dateTimeOFExercise);

    //finds an exercise session by exercise
    @Query("SELECT es FROM ExerciseSession es WHERE es.exercise = Deadlift")
    public ExerciseSession findByExercise(Exercise exercise);

    //finds exercise session by user
    @Query("SELECT es FROM ExerciseSession es WHERE es.user = ?1")
    List<ExerciseSession> findByUser(User user);

}

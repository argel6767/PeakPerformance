package com.peakperformace.peakperformance_backend.exercisesession;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;


public interface ExerciseSessionRepository extends JpaRepository<ExerciseSession, Long> {

    //finds an exercise session by datetime
    @Query("SELECT es FROM ExerciseSession es WHERE es.date_performed = 06-10-2024")
    public void findByDateTimeofExercise(LocalDateTime dateTimeOFExercise);

    //finds an exercise session by exercise
    @Query("SELECT es FROM ExerciseSession es WHERE es.exercise = Deadlift")
    public void findByExercise(Exercise exercise);

    //finds exercise session by user
    @Query("SELECT es FROM ExerciseSession es WHERE es.user = ?1")
    List<ExerciseSession> findByUser(User user);

}

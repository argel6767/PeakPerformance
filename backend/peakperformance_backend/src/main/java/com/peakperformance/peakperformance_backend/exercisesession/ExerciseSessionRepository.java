package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;


public interface ExerciseSessionRepository extends JpaRepository<ExerciseSession, Long> {

    //finds an exercise session by datetime
    @Query("SELECT es FROM ExerciseSession es WHERE es.dateTimeofExercise = :dateTimeOfExerciseSession")
    public ExerciseSession findByDateTimeofExerciseSession(LocalDateTime dateTimeOfExerciseSession);

    //custom find exercisesession by id method
    @Query("SELECT es FROM ExerciseSession es WHERE es.exersisesessionid = :exercisesessionid")
    public ExerciseSession findExerciseSessionById(Long id);
}

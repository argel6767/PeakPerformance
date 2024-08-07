package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.peakperformance.peakperformance_backend.exercise.Exercise;
import com.peakperformance.peakperformance_backend.user.User;


public interface ExerciseSessionRepository extends JpaRepository<ExerciseSession, LocalDateTime> {

    //finds an exercise session by datetime
    @Query("SELECT es FROM ExerciseSession es WHERE es.dateTimeofExercise = :dateTimeOfExerciseSession")
    public ExerciseSession findByDateTimeofExerciseSession(LocalDateTime dateTimeOfExerciseSession);

    //finds an exercise session by exercise
    @Query("SELECT es FROM ExerciseSession es WHERE es.exercise = :exercise")
    public ExerciseSession findByExercise(Exercise exercise);

    //finds exercise session by user
    @Query("SELECT es FROM ExerciseSession es WHERE es.user = :user")
    List<ExerciseSession> findByUser(User user);

    //custom find exercisesession by id method
    @Query("SELECT es FROM ExerciseSession es WHERE es.exersisesessionid = :exercisesessionid")
    public ExerciseSession findExerciseSessionById(Long Id);
}

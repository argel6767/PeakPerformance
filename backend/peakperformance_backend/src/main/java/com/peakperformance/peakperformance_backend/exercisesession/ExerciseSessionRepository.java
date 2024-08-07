package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.peakperformance.peakperformance_backend.user.User;


public interface ExerciseSessionRepository extends JpaRepository<ExerciseSession, Long> {

    //finds an exercise session by datetime
    @Query("SELECT es FROM ExerciseSession es WHERE es.dateTimeofExercise = :dateTimeOfExerciseSession")
    public ExerciseSession findByDateTimeofExerciseSession(LocalDateTime dateTimeOfExerciseSession);

 
    //finds exercise session by user
    @Query("SELECT es FROM ExerciseSession es WHERE es.user = ?1")
    List<ExerciseSession> findByUser(User user);

}

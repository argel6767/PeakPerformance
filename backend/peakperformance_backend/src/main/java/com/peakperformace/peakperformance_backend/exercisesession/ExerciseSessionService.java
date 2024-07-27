package com.peakperformace.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.peakperformace.peakperformance_backend.exercise.Exercise;

@Service
public class ExerciseSessionService {

    private final ExerciseSessionRepository exerciseSessionRepository;

    @Autowired
    public ExerciseSessionService(ExerciseSessionRepository exerciseSessionRepository) {
        this.exerciseSessionRepository = exerciseSessionRepository;
    }

    public List<ExerciseSession> getAllExerciseSessions() {
        return exerciseSessionRepository.findAll();
    }

    public List<ExerciseSession> getExerciseSessionByExercise(Exercise exercise) {
        return exerciseSessionRepository.findByExercise(exercise);
    }

        public Optional<ExerciseSession> getExerciseSessionById(Long id) {
        return exerciseSessionRepository.findById(id);

    public List<ExerciseSession> getExerciseByDateTime(LocalDateTime dateTimeOFExercise) throws ExerciseSessionNotFoundException {
        if (getExerciseByDateTime(null)){
            throw new ExerciseSessionNotFoundException("There is no exercise session under this date");
        }

        return exerciseSessionRepository.findByDateTimeofExercise(dateTimeOFExercise);
    }
}

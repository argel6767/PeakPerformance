package com.peakperformace.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Service;

import com.peakperformace.peakperformance_backend.exercise.Exercise;

@Service
public class ExerciseSessionService {

    private final ExerciseSessionRepository exerciseSessionRepository;

    public ExerciseSessionService(ExerciseSessionRepository exerciseSessionRepository) {
        this.exerciseSessionRepository = exerciseSessionRepository;
    }

    public List<ExerciseSession> getExerciseSessionByExercise(Exercise exercise) throws ExerciseSessionNotFoundException {
        if (exerciseSessionRepository.findByExercise(exercise) == null){
            throw new ExerciseSessionNotFoundException("There is no exercise session doing this exercise");
        }
        return exerciseSessionRepository.findByExercise(exercise);
    }


    public List<ExerciseSession> getExerciseByDateTime(LocalDateTime dateTimeOfExercise) throws ExerciseSessionNotFoundException {
        if (exerciseSessionRepository.findByDateTimeofExercise(dateTimeOfExercise) == null){
            throw new ExerciseSessionNotFoundException("There is no exercise session under this date");
        }

    return exerciseSessionRepository.findByDateTimeofExercise(dateTimeOfExercise);
    }
        
    public class ExerciseSessionNotFoundException extends Exception {

        public ExerciseSessionNotFoundException(String string) {
            super(string);
            }
        }
    }
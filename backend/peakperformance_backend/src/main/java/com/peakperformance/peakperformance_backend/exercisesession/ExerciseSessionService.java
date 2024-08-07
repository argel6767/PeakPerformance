package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;

import org.springframework.stereotype.Service;

import com.peakperformance.peakperformance_backend.exercise.Exercise;

@Service
public class ExerciseSessionService {

    private final ExerciseSessionRepository exerciseSessionRepository;

    public ExerciseSessionService(ExerciseSessionRepository exerciseSessionRepository) {
        this.exerciseSessionRepository = exerciseSessionRepository;
    }

    public ExerciseSession getExerciseSessionByExercise(Exercise exercise) throws ExerciseSessionNotFoundException {
        if (exerciseSessionRepository.findByExercise(exercise) == null){
            throw new ExerciseSessionNotFoundException("There is no exercise session doing this exercise");
        }
        return exerciseSessionRepository.findByExercise(exercise);
    }

    public ExerciseSession getExerciseSessionById(Long id) throws ExerciseSessionNotFoundException {
        if (exerciseSessionRepository.findExerciseSessionById(id) == null){
            throw new ExerciseSessionNotFoundException("There is no exercise session id");
        }
        return exerciseSessionRepository.findExerciseSessionById(id);
    }

    public ExerciseSession getExerciseSessionByDateTime(LocalDateTime dateTimeOfExerciseSession) throws ExerciseSessionNotFoundException {
        if (exerciseSessionRepository.findByDateTimeofExerciseSession(dateTimeOfExerciseSession) == null){
            throw new ExerciseSessionNotFoundException("There is no exercise session under this date");
        }
        return exerciseSessionRepository.findByDateTimeofExerciseSession(dateTimeOfExerciseSession);
    }
        
    public ExerciseSession saveExerciseSession(ExerciseSession exerciseSession) {
        return exerciseSessionRepository.save(exerciseSession);
    }

    

    public class ExerciseSessionNotFoundException extends Exception {

        public ExerciseSessionNotFoundException(String string) {
            super(string);
            }
        }
    }

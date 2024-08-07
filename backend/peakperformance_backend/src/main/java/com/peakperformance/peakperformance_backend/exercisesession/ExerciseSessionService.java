package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;

import org.springframework.stereotype.Service;


@Service
public class ExerciseSessionService {

    private final ExerciseSessionRepository exerciseSessionRepository;

    public ExerciseSessionService(ExerciseSessionRepository exerciseSessionRepository) {
        this.exerciseSessionRepository = exerciseSessionRepository;
    }




    public ExerciseSession getExerciseSessionByDateTime(LocalDateTime dateTimeOfExerciseSession) throws ExerciseSessionNotFoundException {
        if (exerciseSessionRepository.findByDateTimeofExerciseSession(dateTimeOfExerciseSession) == null){
            throw new ExerciseSessionNotFoundException("There is no exercise session under this date");
        }

    return exerciseSessionRepository.findByDateTimeofExerciseSession(dateTimeOfExerciseSession);
    }
        
    public class ExerciseSessionNotFoundException extends Exception {

        public ExerciseSessionNotFoundException(String string) {
            super(string);
            }
        }
    }

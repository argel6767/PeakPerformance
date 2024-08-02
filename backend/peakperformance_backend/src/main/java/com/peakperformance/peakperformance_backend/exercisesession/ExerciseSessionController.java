package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.peakperformance.peakperformance_backend.exercise.Exercise;
import com.peakperformance.peakperformance_backend.exercisesession.ExerciseSessionService.ExerciseSessionNotFoundException;

@Controller
@RequestMapping("/exercisesession/")
public class ExerciseSessionController {
    private final ExerciseSessionService exerciseSessionService;

    public ExerciseSessionController(ExerciseSessionService exerciseSessionService) {
        this.exerciseSessionService = exerciseSessionService;
    }
    
    @GetMapping("exercisesession/byDateTime")
    public ExerciseSession getExerciseSessionByDateTime(@RequestParam("dateTime") String dateTime) throws ExerciseSessionNotFoundException {
        LocalDateTime localDateTime = LocalDateTime.parse(dateTime);
        return exerciseSessionService.getExerciseSessionByDateTime(localDateTime);
    }

    @GetMapping("exercisesession/byExercise")
    public ExerciseSession getExerciseSessionByExercise(@RequestParam("exerciseId") Long exerciseId) throws ExerciseSessionNotFoundException {
        Exercise exercise = exerciseService.getExerciseById(exerciseId);
        return exerciseSessionService.getExerciseSessionByExercise(exercise);
    }
}
package com.peakperformance.peakperformance_backend.exercisesession;

import java.time.LocalDateTime;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.peakperformance.peakperformance_backend.exercise.Exercise;
import com.peakperformance.peakperformance_backend.exercisesession.ExerciseSessionService.ExerciseSessionNotFoundException;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PathVariable;


@Controller
@RequestMapping("/exercisesession")
public class ExerciseSessionController {
    private final ExerciseSessionService exerciseSessionService;

    public ExerciseSessionController(ExerciseSessionService exerciseSessionService) {
        this.exerciseSessionService = exerciseSessionService;
    }
    
    @GetMapping("/byDateTime")
    public ExerciseSession getExerciseSessionByDateTime(@RequestParam("dateTime") String dateTime) throws ExerciseSessionNotFoundException {
        LocalDateTime localDateTime = LocalDateTime.parse(dateTime);
        return exerciseSessionService.getExerciseSessionByDateTime(localDateTime);
    }


    @PutMapping("exercisesession/{id}")
    public ExerciseSession updateExerciseSession(@PathVariable Long id, @RequestBody ExerciseSession updatedExerciseSession) throws ExerciseSessionNotFoundException {
        
        return exerciseSessionService.updateExerciseSession(id, updatedExerciseSession);
    }

    @DeleteMapping("exercisesession/{id}")
    public void deleteExerciseSession(@PathVariable Long id) throws ExerciseSessionNotFoundException {
        exerciseSessionService.deleteExerciseSession(id);
    }

}

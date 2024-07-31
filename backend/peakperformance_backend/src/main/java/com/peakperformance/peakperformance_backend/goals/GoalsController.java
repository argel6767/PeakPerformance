package com.peakperformance.peakperformance_backend.goals;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.goals.GoalsService.GoalNotFoundException;
import com.peakperformance.peakperformance_backend.user.User;




@Controller
@RequestMapping("/goals/")
public class GoalsController {

    private final GoalsService goalsService;

    public GoalsController(GoalsService goalsService) {
        this.goalsService = goalsService;
    }

    @GetMapping(path ="{goalId}")
    public Goals getGoalById(@PathVariable("goalId") Long id) throws GoalNotFoundException {
        return goalsService.getGoalById(id);
    }

    @GetMapping(path = "{goalId}/user")
    public User getUserAttchedToGoalById(@PathVariable("goalId") Long id) throws GoalNotFoundException{
        return goalsService.getUserAttachedToGoalById(id);
    }

    @GetMapping("{goalId}/liftingGoals")
    public List<Lift> getMethodName(@PathVariable("goalId") Long id) throws GoalNotFoundException{
        return goalsService.getGoalLiftsById(id);
    }


    @PutMapping("{goalId}/addlift")
    public void addAGoalLiftById(@PathVariable("goalId") Long id, @RequestBody Lift newLiftGoal) throws GoalNotFoundException {
        goalsService.addAGoalLiftById(id, newLiftGoal);
    }

    @PutMapping("{goalId}/addlifts")
    public void updateGoalLiftsById(@PathVariable("goalId") Long id, @RequestBody List<Lift> liftingGoals) throws GoalNotFoundException {
        goalsService.updateGoalLiftsById(id, liftingGoals);        
    }
    
    

}

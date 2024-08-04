package com.peakperformance.peakperformance_backend.goals;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.goals.GoalsService.GoalNotFoundException;
import com.peakperformance.peakperformance_backend.user.User;





@RestController
@RequestMapping("/goals")
public class GoalsController {

    private final GoalsService goalsService;

    public GoalsController(GoalsService goalsService) {
        this.goalsService = goalsService;
    }

    @GetMapping("/{goalId}")
    public Goals getGoalById(@PathVariable("goalId") Long id) {
        try{
            return goalsService.getGoalById(id);
        }
        catch(GoalNotFoundException gnfe) {
            return null;
        }
    }

    @GetMapping("/allgoals")
    public List<Goals> getAllGoals() {
        return goalsService.getAllGoals();
    }
    

    @GetMapping("/{goalId}/user")
    public User getUserAttchedToGoalById(@PathVariable("goalId") Long id) {
        try{
            return goalsService.getUserAttachedToGoalById(id);
        }
        catch(GoalNotFoundException gnfe) {
            return null;
        }
    }

    @GetMapping("/{goalId}/liftingGoals")
    public List<Lift> getLiftingGoalsById(@PathVariable("goalId") Long id) {
         try{
            return goalsService.getGoalLiftsById(id);
        }
        catch(GoalNotFoundException gnfe) {
            return null;
        }
    }

    @PutMapping("/{goalId}/weight")
    public String updateGoalWeight(@PathVariable("goalId") Long id, @RequestBody Integer weightGoal) {
        try{
            goalsService.updateGoalWeightById(id, weightGoal);
            return "Sucess!";
        }
        catch(GoalNotFoundException gnfe) {
            return "id: " + id + " does not belong to any goal";
        }
    }

    @PutMapping("/{goalId}/addlift")
    public String addAGoalLiftById(@PathVariable("goalId") Long id, @RequestBody Lift newLiftGoal) {
        try{
            goalsService.addAGoalLiftById(id, newLiftGoal);
            return "Sucess!";
        }
        catch(GoalNotFoundException gnfe) {
            return "id: " + id + " does not belong to any goal";
        }
    }

    @PutMapping("/{goalId}/addlifts")
    public String updateGoalLiftsById(@PathVariable("goalId") Long id, @RequestBody List<Lift> liftingGoals) throws GoalNotFoundException {
        try{
            goalsService.updateGoalLiftsById(id, liftingGoals);
            return "Sucess!";
        }
        catch(GoalNotFoundException gnfe) {
            return "id: " + id + " does not belong to any goal";
        }      
    }
    
    

}

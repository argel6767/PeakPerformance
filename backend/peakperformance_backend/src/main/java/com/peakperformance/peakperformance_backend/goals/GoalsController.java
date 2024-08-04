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
    public Goals getGoalById(@PathVariable("goalId") Long id) throws GoalNotFoundException {
        return goalsService.getGoalById(id);
    }

    @GetMapping("/allgoals")
    public List<Goals> getAllGoals() {
        return goalsService.getAllGoals();
    }
    

    @GetMapping("/{goalId}/user")
    public User getUserAttchedToGoalById(@PathVariable("goalId") Long id) throws GoalNotFoundException{
        return goalsService.getUserAttachedToGoalById(id);
    }

    @GetMapping("/{goalId}/liftingGoals")
    public List<Lift> getLiftingGoalsById(@PathVariable("goalId") Long id) throws GoalNotFoundException{
        return goalsService.getGoalLiftsById(id);
    }

    @PutMapping("/{goalId}/weight")
    public void updateGoalWeight(@PathVariable("goalId") Long id, @RequestBody Integer weightGoal) throws GoalNotFoundException {
        goalsService.updateGoalWeightById(id, weightGoal);
    }

    @PutMapping("/{goalId}/addlift")
    public void addAGoalLiftById(@PathVariable("goalId") Long id, @RequestBody Lift newLiftGoal) throws GoalNotFoundException {
        goalsService.addAGoalLiftById(id, newLiftGoal);
    }

    @PutMapping("/{goalId}/addlifts")
    public void updateGoalLiftsById(@PathVariable("goalId") Long id, @RequestBody List<Lift> liftingGoals) throws GoalNotFoundException {
        goalsService.updateGoalLiftsById(id, liftingGoals);        
    }
    
    

}

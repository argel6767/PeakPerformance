package com.peakperformance.peakperformance_backend.goals;

import org.springframework.stereotype.Service;

import com.peakperformance.peakperformance_backend.user.User;

import java.util.Optional;
import java.util.List;
import com.peakperformance.peakperformance_backend.exercise.model.Lift;



@Service
public class GoalsService {

    private final GoalsRepository goalsRepo;

    public GoalsService(GoalsRepository goalsRepo) {
        this.goalsRepo = goalsRepo;
    }

    public Goals getGoalById(Long id) throws GoalNotFoundException {
        Optional<Goals> goalOptional = goalsRepo.findById(id);

        if (!goalOptional.isPresent()) {
            throw new GoalNotFoundException();
        }

        Goals goal = goalOptional.get();
        return goal;
    }

    public User getUserAttachedToGoalById(Long id) throws GoalNotFoundException{
        Optional<Goals> goalOptional = goalsRepo.findById(id);

        if (!goalOptional.isPresent()) {
            throw new GoalNotFoundException();
        }

        Goals goal = goalOptional.get();
        User user = goal.getUser();

        return user;
    }

    public List<Lift> getGoalLiftsById(Long id) throws GoalNotFoundException{
        Optional<Goals> goalOptional = goalsRepo.findById(id);

        if (!goalOptional.isPresent()) {
            throw new GoalNotFoundException();
        }

        Goals goal = goalOptional.get();

        List<Lift> liftGoals = goal.getLiftGoals();

        return liftGoals;
    }

    @Transactional
    public void addAGoalLiftById(Long id, Lift newLiftGoal) throws GoalNotFoundException {
        Optional<Goals> goalOptional = goalsRepo.findById(id);

        if (!goalOptional.isPresent()) {
            throw new GoalNotFoundException();
        }

        Goals goal = goalOptional.get();

        List<Lift> liftGoals = goal.getLiftGoals();
        liftGoals.add(newLiftGoal);

        goalsRepo.save(goal);
    }



    public class GoalNotFoundException extends Exception {

        public GoalNotFoundException(String message) {
            super(message);
        }

        public GoalNotFoundException() {
            super();
        }
    }
}

package com.peakperformace.peakperformance_backend.goals;

import org.springframework.stereotype.Service;

import com.peakperformace.peakperformance_backend.user.User;

@Service
public class GoalsService {

    private final GoalsRepository goalsRepo;

    public GoalsService(GoalsRepository goalsRepo) {
        this.goalsRepo = goalsRepo;
    }


    public Goals getUsersGoalsById(Long userId) {
        
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

package com.peakperformance.peakperformance_backend.goals;

import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToOne;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import java.util.List;

import com.peakperformance.peakperformance_backend.converter.JSONBConverter;
import com.peakperformance.peakperformance_backend.exercise.model.Lift;
import com.peakperformance.peakperformance_backend.user.User;

@Entity
@Table

/*
 * goals given by the user are put into a Goal object when they first make account
 * goals can also be added after the fact as well, and are optional
 */
public class Goals {
    @Id
    @SequenceGenerator (
        name = "goals_sequence",
        sequenceName = "goals_sequence",
        allocationSize = 1
    )
    @GeneratedValue (
        strategy = GenerationType.SEQUENCE,
        generator = "goals_sequence"
    )

    private Long id;
    private Integer weightGoal;
    
    @Column(columnDefinition = "jsonb", nullable = true)
    @Convert(converter = JSONBConverter.class) 
    private List<Lift> liftGoals;

    @OneToOne(mappedBy = "goals")
    private User user;
    
    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    //both weight and lift goals are given
    public Goals(Integer weightGoal, List<Lift> liftGoals) {
        this.weightGoal = weightGoal;
        this.liftGoals = liftGoals;
    }
    
    //only weight goal is given
    public Goals(Integer weightGoal) {
        this.weightGoal = weightGoal;
        this.liftGoals = null;
    }
    
    //only lift goals are given
    public Goals(List<Lift> liftGoals) {
        this.weightGoal = null;
        this.liftGoals = liftGoals;
    }

    //no goals are given
    public Goals() {
        this.weightGoal = null;
        this.liftGoals = null;
    }
    
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getWeightGoal() {
        return weightGoal;
    }
    public void setWeightGoal(Integer weightGoal) {
        this.weightGoal = weightGoal;
    }
    //returns status of weightGoal
    public String weightGoalStatus() {
        if (hasWeightGoal()) return "weight goal set";
        else return "weight goal not set";
    }

    //checks if a weight goal is present
    private boolean hasWeightGoal() {
        return weightGoal != null;
    }

    public List<Lift> getLiftGoals() {
        return liftGoals;
    }
    public void setLiftGoals(List<Lift> liftGoals) {
        this.liftGoals = liftGoals;
    } 
    //returns status of liftGoals
    public String liftGoalStatus() {
        if (hasLiftGoals()) return "lift goals set";
        else return "lift goals not set";
    }
    //checks if lifting goals are present
    private boolean hasLiftGoals() {
        return liftGoals != null;
    }

    //overall status as to what goals have/haven't been set
    public String overallGoalsStatus() {
        if (!hasWeightGoal() && !hasLiftGoals()) return "no goals set";
        else if (!hasWeightGoal()) return "only lift goals set";
        else if (!hasLiftGoals()) return "only weight goal set";
        else return "both goals set";
    }

}

package com.peakperformace.peakperformance_backend.goals;

import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import java.util.List;

import com.peakperformace.peakperformance_backend.exercise.liftmodel.Lift;

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
    @Column(columnDefinition = "jsonb")
    @Convert(converter = Object.class) // Object placeholder for until Jsonb converter class is made
    private List<Lift> liftGoals;
    
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

    public Integer getWeightGoal() {
        return weightGoal;
    }
    public void setWeightGoal(Integer weightGoal) {
        this.weightGoal = weightGoal;
    }
    
    public List<Lift> getLiftGoals() {
        return liftGoals;
    }
    public void setLiftGoals(List<Lift> liftGoals) {
        this.liftGoals = liftGoals;
    }

}

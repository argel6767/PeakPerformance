package com.peakperformace.user;

import java.time.LocalDate;
import java.time.LocalDateTime;

import java.util.List;

import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;

@Entity
@Table
public class User {
    @Id
    @SequenceGenerator (
        name = "user_sequence",
        sequenceName = "user_sequence",
        allocationSize = 1
    )
    @GeneratedValue (
        strategy = GenerationType.SEQUENCE,
        generator = "user_sequence"
    )

    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private String password; 
    private LocalDate dob;   
    private Integer height;
    private Integer weight;
    @Column(columnDefinition = "jsonb")
    @Convert(converter = Object.class)//placehold until JsonConver class is made
    private List<Object> currentLifts; //placeholder until lift and LiftSet classes are made
    private Object goals; //placeholder until Goal class is made
    @CreationTimestamp
    private LocalDateTime createdAt;

    //goals and current lifts are given by user
    public User(String firstName, String lastName, String email, String password, LocalDate dob, Integer height, Integer weight, List<Object> currentLifts, Object goals) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
        this.dob = dob;
        this.height = height;
        this.weight = weight;
        this.currentLifts = currentLifts;
        this.goals = goals;
    }

    
    //no current lifts given
    public User(String firstName, String lastName, String email, String password, LocalDate dob, Integer height,
            Integer weight, Object goals) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
        this.dob = dob;
        this.height = height;
        this.weight = weight;
        this.currentLifts = null;
        this.goals = goals;
    }

    //no goals given
    public User(String firstName, String lastName, String email, String password, LocalDate dob, Integer height,
            Integer weight, List<Object> currentLifts) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
        this.dob = dob;
        this.height = height;
        this.weight = weight;
        this.currentLifts = currentLifts;
    }

    //no current lifts or goals given
    public User(String firstName, String lastName, String email, String password, LocalDate dob, Integer height,
            Integer weight) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
        this.dob = dob;
        this.height = height;
        this.weight = weight;
    }

    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }

    public LocalDate getDob() {
        return dob;
    }
    public void setDob(LocalDate dob) {
        this.dob = dob;
    }

    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }

    public Integer getHeight() {
        return height;
    }
    public void setHeight(Integer height) {
        this.height = height;
    }

    public Integer getWeight() {
        return weight;
    }
    public void setWeight(Integer weight) {
        this.weight = weight;
    }

    public List<Object> getCurrentLifts() {
        return currentLifts;
    }
    public void setCurrentLifts(List<Object> currentLifts) {
        this.currentLifts = currentLifts;
    }

    public Object getGoals() {
        return goals;
    }
    public void setGoals(Object goals) {
        this.goals = goals;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    @Override
    public String toString() {
        return "User [id=" + id + ", firstName=" + firstName + ", lastName=" + lastName + ", email=" + email + ", dob="
                + dob + ", password=" + password + ", height=" + height + ", weight=" + weight + ", currentLifts="
                + currentLifts + ", goals=" + goals + ", createdAt=" + createdAt + "]";
    }
    
}

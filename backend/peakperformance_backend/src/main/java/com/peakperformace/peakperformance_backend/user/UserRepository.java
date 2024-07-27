package com.peakperformace.peakperformance_backend.user;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import com.peakperformace.peakperformance_backend.exercise.model.Lift;
import java.util.List;

@Repository
public interface UserRepository extends JpaRepository<User, Long>{

    @Query("SELECT u FROM User u WHERE u.email = ?1")
    public Optional<User> findUserByEmail(String email);

    //finds user by id then updates their weight
    @Modifying
    @Query("UPDATE User u SET u.weight = :weight WHERE u.id = :id")
    public void changeWeightOfUserById(Long id, Integer weight);

    @Query("SELECT u.weight FROM User u WHERE u.id = :id")
    public Integer getWeightOfUserById(Long id);

    //finds user by id then updates their currentlifts
    @Modifying
    @Query("UPDATE User u set u.currentLifts = :currentLifts WHERE u.id = :id") 
    public void changeCurrentLiftsOfUserById(Long id, List<Lift> currentLifts);

    @Query("SELECT u.currentLifts FROM User u WHERE u.id = :id")
    public List<Lift> getCurrentLiftsOfUserById(Long id);
} 
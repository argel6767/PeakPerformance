package com.peakperformace.peakperformance_backend.goals;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GoalsRepository extends JpaRepository<Goals, Long>  {

}

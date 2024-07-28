package com.peakperformance.peakperformance_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import io.github.cdimascio.dotenv.Dotenv;

@SpringBootApplication
public class PeakperformanceBackendApplication {

	public static void main(String[] args) {

		 // Load environment variables from .env file
        Dotenv dotenv = Dotenv.configure().directory("backend/peakperformance_backend/.env").load();
		

        // Set system properties
        System.setProperty("DATABASE_URL", dotenv.get("DATABASE_URL"));
		System.setProperty("DATABASE_USERNAME", dotenv.get("DATABASE_USERNAME"));
		System.setProperty("DATABASE_PASSWORD", dotenv.get("DATABASE_PASSWORD"));

		SpringApplication.run(PeakperformanceBackendApplication.class, args);
	}

}

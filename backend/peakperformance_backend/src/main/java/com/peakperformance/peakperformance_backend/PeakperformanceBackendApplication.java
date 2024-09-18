package com.peakperformance.peakperformance_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

import com.peakperformance.peakperformance_backend.auth.RsaKeyProperties;

import io.github.cdimascio.dotenv.Dotenv;

@SpringBootApplication
@EnableConfigurationProperties(RsaKeyProperties.class)
public class PeakperformanceBackendApplication {

	public static void main(String[] args) {

		 // Load environment variables from .env file
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
		

        // Set system properties
        System.setProperty("SUPABASE_DB_URL", dotenv.get("SUPABASE_DB_URL"));
		System.setProperty("SUPABASE_DB_USERNAME", dotenv.get("SUPABASE_DB_USERNAME"));
		System.setProperty("SUPABASE_DB_PASSWORD", dotenv.get("SUPABASE_DB_PASSWORD"));

		SpringApplication.run(PeakperformanceBackendApplication.class, args);
	}

}

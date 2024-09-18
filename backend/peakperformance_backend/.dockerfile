FROM openjdk:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the JAR file from local system into the container
COPY target/peakperformance_backend-0.0.1-SNAPSHOT.jar app.jar

# Expose the port your PeakPerformance app listens on
EXPOSE 8080

# Command to run  PeakPerformance application
ENTRYPOINT ["java", "-jar", "app.jar"]
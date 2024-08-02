
# PeakPerformance

Welcome to **PeakPerformance**, a web fitness application designed to help you track and achieve your fitness goals. This README provides a brief overview of the project and its technologies. 

## Overview

**PeakPerformance** is a web-based fitness application that will eventually be available as a mobile app using web view technology. The goal of this app is to provide users with a platform to log workouts, track progress, and stay motivated on their fitness journey.

## Technologies

- **Backend:**
  - Spring Boot 3.0
  - PostgreSQL

- **Frontend:**
  - React

- **Mobile Integration:**
  - Capacitor (for converting the web app into a mobile app)

## Features

- Log workouts and track your progress over time.
- Set fitness goals and monitor achievements.
- View detailed statistics and analytics of your workouts.
- User authentication and personalized profiles.

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/peakperformance-backend.git
   cd peakperformance-backend
   ```

2. Set up PostgreSQL and configure the database connection in `application.properties`.

3. Build and run the Spring Boot application:
   ```bash
   ./mvnw clean install
   ./mvnw spring-boot:run
   ```

### Frontend

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/peakperformance-frontend.git
   cd peakperformance-frontend
   ```

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Start the React application:
   ```bash
   npm start
   ```

### Mobile App (Future Implementation)

1. Set up Capacitor in the frontend project:
   ```bash
   npm install @capacitor/core @capacitor/cli
   npx cap init
   ```

2. Add the desired platform (e.g., iOS, Android):
   ```bash
   npx cap add android
   npx cap add ios
   ```

3. Build the project and sync with Capacitor:
   ```bash
   npm run build
   npx cap copy
   npx cap open android
   # or
   npx cap open ios
   ```

## Contributing

We are currently not accepting outside contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or inquiries, please contact us at <a href="mailto:argel6767@gmail.com">argel6767@gmail.com</a>.

# PeakPerformance

Welcome to **PeakPerformance**, a fitness application designed to help you track and achieve your fitness goals while connecting with friends. This README provides a brief overview of the project and its technologies.

## Overview

**PeakPerformance** is a mobile fitness application built with React Native. The goal of this app is to provide users with a platform to log workouts, track progress, connect with friends, and stay motivated on their fitness journey through friendly competition.

## Technologies

- **Backend:**
  - Django
  - PostgreSQL

- **Frontend:**
  - React Native

## Features

- Log workouts and track your progress over time
- Set fitness goals and monitor achievements
- View detailed statistics and analytics of your workouts
- User authentication and personalized profiles
- Add friends and build your fitness community
- Compare your progress with friends
- "Strongest of the Week" feature highlighting which friend made the most strength improvements

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/peakperformance-backend.git
   cd peakperformance-backend
   ```

2. Set up a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL and configure the database connection in `settings.py`.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

### Frontend

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/peakperformance-frontend.git
   cd peakperformance-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React Native development server:
   ```bash
   npx react-native start
   ```

4. Run on Android or iOS:
   ```bash
   npx react-native run-android
   # or
   npx react-native run-ios
   ```

## Contributing

We are currently not accepting outside contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or inquiries, please contact us at <a href="mailto:argel6767@gmail.com">argel6767@gmail.com</a>.

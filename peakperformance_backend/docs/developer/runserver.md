# Running Development Server for PeakPerformance

This documentation explains how to run the PeakPerformance backend server using Docker.

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## 1. Building the Container

- Ensure you are in the `PeakPerformance/peakperformance_backend` directory
- To build the container run the following command:

```docker
docker-compose build
```

## 2. Starting the Server

- After building the container, you can start the development server by running the following command:

```docker
docker-compose up -d
```

## 3. Accessing the Server

- You can now view created endpoints using Django Rest Framework by entering `localhost:8000` into your web browser.

## 4. Available Endpoints

- To access the admin endpoint:

```url
localhost:8000/admin/
```

- To access user endpoints:

```url
localhost:8000/peakperformance_backend/users/user-info/
localhost:8000/peakperformance_backend/users/register/
localhost:8000/peakperformance_backend/users/login/
localhost:8000/peakperformance_backend/users/logout/
localhost:8000/peakperformance_backend/users/refresh/
localhost:8000/peakperformance_backend/users/verify-2fa/
localhost:8000/peakperformance_backend/users/password-reset/
localhost:8000/peakperformance_backend/users/password-reset/confirm/
```

## 5. Stopping the Server

- To stop the development server, run the following command:

```docker
docker-compose down
```

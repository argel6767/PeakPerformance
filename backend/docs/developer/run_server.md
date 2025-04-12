# Running Development Backend Server for PeakPerformance

This documentation explains how to run the PeakPerformance backend server using Docker.

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## 1. Starting the Server

- Ensure you are in the `PeakPerformance/backend` directory
- To build the container, run the following command:

```bash
python scripts/run_server.py
```

## 2. Accessing the Server

- You can now view created endpoints using Django Rest Framework by entering `localhost:8000` into your web browser.

## 3. Available Endpoints

- To access the admin endpoint:

```bash
localhost:8000/admin/
```

- To access user endpoints:

```bash
localhost:8000/api/users/user-info/
localhost:8000/api/users/register/
localhost:8000/api/users/login/
localhost:8000/api/users/logout/
localhost:8000/api/users/refresh/
localhost:8000/api/users/verify-2fa/
localhost:8000/api/users/password-reset/
localhost:8000/api/users/password-reset/confirm/
```

- To access movement endpoints:

```bash
localhost:8000/api/movements
```

- To access muscles endpoints:
```bash
localhost:8000/api/muscles
```

## 4. Stopping the Server

- To stop the development server, press `Ctrl + C` in the terminal, or run the following command in a different terminal:

```bash
python scripts/end_server.py
```

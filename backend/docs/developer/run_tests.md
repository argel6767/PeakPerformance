# Running Development Server for PeakPerformance

This documentation explains how to run the PeakPerformance backend test suite using Docker.

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## Running Tests

- Ensure you are in the `PeakPerformance/backend` directory
- To build the testing container, run the following command:

```bash
python scripts/run_tests.py
```

Test results will be logged in the terminal, and the container will stop and delete itself once the all tests have been ran.
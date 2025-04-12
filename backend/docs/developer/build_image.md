# Building PeakPerformance Backend Server Image

This documentation explains how to build the PeakPerformance backend server using Docker.

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## Building the Image

- Ensure you are in the `PeakPerformance/backend` directory
- To build the container run the following command:

```bash
python scripts/build_image.py
```

This will build PeakPerformance's Django backend image with the newest changes done.

**Note**: *This will not run the actual backend dev server. To run the backend see [run_server.md](run_server.md).*
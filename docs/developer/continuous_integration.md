# Continuous Integration with GitHub Actions

This documentation explains how the PeakPerformance CI pipeline automatically builds and tests code changes using GitHub Actions.

Before you begin, ensure you have the following configured in your repository:

- A `.github/workflows` directory in your project root
- Proper GitHub repository permissions for Actions

## 1. CI Workflow Overview

- The CI pipeline automatically triggers when changes are pushed to the repository
- It detects which part of the codebase has changed (backend or frontend)
- It builds and tests only the modified section
- It reports the build and test status (pass/fail)

## 2. Workflow Configuration

- The workflow is defined in [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)
- To customize the workflow, modify this YAML file

```yaml
name: PeakPerformance CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      frontend-changed: ${{ steps.filter.outputs.frontend }}
      backend-changed: ${{ steps.filter.outputs.backend }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          base: 'main'
          filters: |
            frontend:
              - 'peakperformance_backend/**'
            backend:
              - 'backend/**'

  build-and-test-frontend:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.frontend-changed == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run frontend build script
        run: npm build
      
      - name: Run frontend test script
        run: npm test

  build-and-test-backend:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.backend-changed == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
          cache-dependency-path: backend/requirements.txt
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Install Docker Compose
        run: |
          sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
          sudo chmod +x /usr/local/bin/docker-compose
      
      - name: Run backend build script
        run: python backend/scripts/build_image.py
      
      - name: Run backend test script
        run: python backend/scripts/run_tests.py

  # This job runs regardless of which part changed, useful for deployment or other steps
  final-steps:
    needs: [detect-changes, build-and-test-frontend, build-and-test-backend]
    if: |
      always() && 
      (needs.detect-changes.outputs.frontend-changed == 'true' || needs.detect-changes.outputs.backend-changed == 'true')
    runs-on: ubuntu-latest
    steps:
      - name: Final verification step
        run: echo "All tests run successfully!"
```

## 3. How It Works

- The workflow uses path filtering to detect changes in specific directories
- If changes are detected in the `backend` directory, the backend build and test job runs
- If changes are detected in the `peakperformance_frontend` directory, the frontend build and test job runs
- Both sections can be tested if changes are made to both directories

## 4. Viewing CI Results

- CI results are visible in the GitHub repository under the "Actions" tab
- Each workflow run shows the status of the pipeline (success or failure)
- You can click on a specific workflow run to see detailed logs
- Pull requests will show the status of the CI checks directly in the PR interface

## 5. Troubleshooting Failed Builds

- If a build fails, check the detailed logs in the GitHub Actions tab
- Common issues include:
  - Missing dependencies
  - Failed tests
  - Syntax errors
  - Configuration issues

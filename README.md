# Holistic Industrial Digital Twin MVP

## vision
A "Holistic Industrial Digital Twin" that demonstrates how raw, chaotic sensor data is automatically transformed into business value using a "Spec Kit" methodology.

## System Architecture
*   **Simulator**: Generates synthetic, chaotic sensor data for multiple assets (HVAC, Conveyor, Robot).
*   **Spec Kit**: A metadata registry that normalizes raw data into meaningful metrics.
*   **Frontend**: Streamlit dashboard for real-time visualization.
*   **Backend**: Python core logic with Firebase integration for persistence.

## Setup Instructions

### Prerequisites
*   Python 3.9+
*   Google Cloud SDK (optional, for deployment)

### Local Development
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    streamlit run src/ui/app.py
    ```

3.  (Optional) Setup Firebase:
    *   Place your `serviceAccountKey.json` in the root directory.
    *   Or set `FIREBASE_CREDENTIALS` environment variable.

## Deployment to Cloud Run
Build and deploy the container:
```bash
gcloud run deploy digital-twin --source .
```

# robolab_mlops
The repository serves as a boiler plate for setting up MLOps config for RL Training.

## Running locally

1. Set up directories to store your db files and mlartifacts in docer-compose.yaml file. Default:

        ~/mlops/data/

2. Run containers

        docker compose up --build

## Testing with examples

1. Go to `/examples`

2. Create `venv`: `python3 -m venv .venv`

3. Enter `venv`: `source .venv/bin/activate`

4. Run `example.py`

5. Open `.ipynb` file and go through

6. Go to MLFlow (`localhost:5000`) and check if experiments are listed there. Go through and verify the artefacts that are created to each experiment.

7. Go to Optuna Dashboard (`localhost:8080`) and check if experiments are created.

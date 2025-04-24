# robolab_mlops
The repository serves as a boiler plate for setting up MLOps config for RL Training.

## Running locally

- Set up directories to store your db files and mlartifacts in docer-compose.yaml file. Default:

        ~/mlops/data/

- Run containers

        docker compose up --build

## Testing with examples

- Go to `/examples`

- Create `venv`: `python3 -m venv .venv`

- Enter `venv`: `source .venv/bin/activate`

- Install dependencies: `pip install -r requirements.txt`

- Run `example.py`

- Open `.ipynb` file and go through

- Go to MLFlow (`localhost:5000`) and check if experiments are listed there. Go through and verify the artefacts that are created to each experiment.

- Go to Optuna Dashboard (`localhost:8080`) and check if experiments are created.

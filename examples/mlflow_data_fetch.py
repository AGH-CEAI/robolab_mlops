import os
import pandas as pd

from mlflow.tracking import MlflowClient

import matplotlib.pyplot as plt

    
def get_metric_data(run_id: str, metric_name: str):
    client = MlflowClient()
    
    metric_history = client.get_metric_history(run_id, metric_name)
    metric_data = [{'step': point.step, 'value': point.value} for point in metric_history]
    metric_df = pd.DataFrame.from_records(metric_data)
    
    return metric_df


def main():
    # assert "MLFLOW_TRACKING_URI" in os.environ
    # os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
    # os.environ["MLFLOW_TRACKING_USERNAME"] = "username"
    # os.environ["MLFLOW_TRACKING_PASSWORD"] = "password"
    
    test_run_id = ""
    test_metric_name = ""
    
    metric_df = get_metric_data(test_run_id, test_metric_name)
    metric_df.plot(x='step', y='value')
    
    plt.grid()
    plt.title(test_metric_name)
    plt.show()
    

if __name__ == "__main__":
    main()

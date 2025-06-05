import os
import pandas as pd
import sys
import yaml
import numpy as np

from mlflow.tracking import MlflowClient
import mlflow

import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 16,
    "font.size": 14,
    "legend.fontsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})
# plt.style.use('seaborn-v0_8-whitegrid')

COLORBLIND_COLORS = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion/orange
    "#009E73",  # green
    "#F0E442",  # yellow
    "#56B4E9",  # light blue
    "#CC79A7",  # purple
    "#E69F00",  # orange
    "#000000",  # black
]
    
    
def get_metric_data(run_id: str, metric_name: str):
    client = MlflowClient()
    
    metric_history = client.get_metric_history(run_id, metric_name)
    metric_data = [{'step': point.step, 'value': point.value} for point in metric_history]
    metric_df = pd.DataFrame.from_records(metric_data)
    return metric_df

def get_experiment_id(experiment_name: str):
    experiment = mlflow.get_experiment_by_name(experiment_name)
    
    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found.")
    
    return experiment.experiment_id

def main():
    # Get experiments file name from command line arguments 
    if len(sys.argv) < 2:
        print("Usage: python mlflow_data_fetch.py <experiments_file.txt>")
        exit(1)
    experiments_file = sys.argv[1]

    # assert "MLFLOW_TRACKING_URI" in os.environ
    os.environ["MLFLOW_TRACKING_URI"] = "http://geonosis:5000"
    os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
    os.environ["MLFLOW_TRACKING_PASSWORD"] = "cdsiadminmlflowceai"
    
    # experiment_name = "experiment-1"
    # current_experiment=dict(mlflow.get_experiment_by_name(experiment_name))
    # experiment_id=current_experiment['experiment_id']

    # Load list of experiments for txt file
    with open(experiments_file, "r") as f:
        recipe_cfgs = yaml.safe_load(f)
        
    for key in recipe_cfgs:
        recipe_cfg = recipe_cfgs[key]

        experiments = recipe_cfg.get("experiments", None)
        metric_name = recipe_cfg.get("metric_name", None)
        order_by = recipe_cfg.get("order_by", None)
        num_of_runs = recipe_cfg.get("num_of_runs", None)
        plot_title = recipe_cfg.get("title", None)
        x_label = recipe_cfg.get("x_label", None)
        y_label = recipe_cfg.get("y_label", None)
        filename = recipe_cfg.get("filename", None)

        
        plt.figure(figsize=(5, 4))
        for exp_cnt in experiments:
            experiment = experiments[exp_cnt]
            experiment_name = experiment["name"]
            experiment_pretty_name = experiment["pretty_name"]
            
            exp_id = get_experiment_id(experiment_name)
            print(f">>> Experiment: {experiment_name} | ID: {exp_id}")

            # df = mlflow.search_runs([experiment_name], order_by=[f"metrics.'{metric_name}' DESC"])
            # df.plot(x='step', y='value')
            df = mlflow.search_runs([exp_id], order_by=[f"metrics.'{order_by}' DESC"])
            
            metrics_dfs = [None] * num_of_runs
            for idx, row in df.iterrows():
                metrics_dfs[idx] = get_metric_data(row["run_id"], metric_name)
                
                if idx == num_of_runs - 1:
                    print(f"Fetched {len(metrics_dfs)} runs for experiment '{experiment_name}'")
                    break

            # Merge all runs on 'step'
            if not metrics_dfs:
                raise ValueError(f"No runs found for experiment '{experiment_name}' with metric '{metric_name}'")
                
            merged = pd.concat(metrics_dfs, keys=range(len(metrics_dfs)), names=['run', 'row']).reset_index(level=0)
            # Pivot to have runs as columns, steps as index
            pivot = merged.pivot(index='step', columns='run', values='value')
            mean = pivot.mean(axis=1)
            min_ = pivot.min(axis=1)
            max_ = pivot.max(axis=1)

            color = COLORBLIND_COLORS[exp_cnt % len(COLORBLIND_COLORS)]

            plt.plot(mean.index, mean.values, label=f"{experiment_pretty_name}", color=color)
            # plt.fill_between(mean.index, min_, max_, alpha=0.2, label=f"{experiment_name} min/max")
            plt.fill_between(mean.index, min_, max_, alpha=0.2, color=color)
        
            # Set x-axis to start from the minimum step value
            steps = mean.index.values
            plt.xlim(mean.index.min() - 0.5, mean.index.max() + 0.5)
            plt.xticks(np.arange(steps.min()-1, steps.max() + 1, step=2))

                

        plt.xlabel(x_label)
        plt.ylabel(y_label) 
        plt.grid()
        plt.title(plot_title)
        plt.legend()
        
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))  # Scientific notation for y-axis

        
        # plt.show()
        # Save the plot and cleanup
        plt.savefig(filename, bbox_inches='tight')
        print(f">>> Plot saved to {filename}")
        plt.clf()  # or plt.close() to fully release memory

if __name__ == "__main__":
    main()

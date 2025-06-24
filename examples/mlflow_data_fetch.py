import os
import pandas as pd
import sys
import yaml
import numpy as np
import string

from mlflow.tracking import MlflowClient
import mlflow

import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "axes.labelsize": 16,
        "font.size": 14,
        "legend.fontsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    }
)
# plt.style.use('seaborn-v0_8-whitegrid')

COLORBLIND_COLORS = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion/orange
    "#009E73",  # green
    "#56B4E9",  # light blue
    "#CC79A7",  # purple
    "#E69F00",  # orange
    "#000000",  # black
    "#F0E442",  # yellow
]


def get_metric_data(run_id: str, metric_name: str):
    client = MlflowClient()

    metric_history = client.get_metric_history(run_id, metric_name)
    metric_data = [
        {"step": point.step, "value": point.value} for point in metric_history
    ]
    metric_df = pd.DataFrame.from_records(metric_data)
    return metric_df


def get_experiment_id(experiment_name: str):
    experiment = mlflow.get_experiment_by_name(experiment_name)

    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found.")

    return experiment.experiment_id


def main():
    # # Get experiments file name from command line arguments
    # if len(sys.argv) < 2:
    #     print("Usage: python mlflow_data_fetch.py <experiments_file.txt>")
    #     exit(1)
    # experiments_file = sys.argv[1]
    
    CHART_FILENAME = "deeprl_all_charts.pdf"
    
    # assert "MLFLOW_TRACKING_URI" in os.environ
    os.environ["MLFLOW_TRACKING_URI"] = "http://geonosis:5000"
    os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
    os.environ["MLFLOW_TRACKING_PASSWORD"] = "cdsiadminmlflowceai"
    
    config_files = [
        "deeprl_baselines.yaml",
        "deeprl_pretrained_models.yaml",
        "deeprl_pretrained_aes.yaml",
    ]
    
    with open(config_files[0], "r") as f:
        tmp_recipe_cfg = yaml.safe_load(f)
            
    rows_n = len(tmp_recipe_cfg)
    cols_n = len(config_files)
    fig, axes = plt.subplots(rows_n, cols_n, figsize=(18, 10))
    axes = axes.flatten()
    
    plt.rcParams["text.usetex"] = True
    # plt.figure(figsize=(5, 4))


    for idx, config_file in enumerate(config_files):
        with open(config_file, "r") as f:
            recipe_cfgs = yaml.safe_load(f)

        for key in recipe_cfgs:
            recipe_cfg = recipe_cfgs[key]

            experiments = recipe_cfg.get("experiments", None)
            metric_name = recipe_cfg.get("metric_name", None)
            order_by = recipe_cfg.get("order_by", None)
            num_of_runs = recipe_cfg.get("num_of_runs", None)
            plot_title = recipe_cfg.get("title", None)
            x_label = recipe_cfg.get("x_label", "")
            y_label = recipe_cfg.get("y_label", "")
            filename = recipe_cfg.get("filename", None)
            x_step = recipe_cfg.get("x_step", 2)
            enable_legend = recipe_cfg.get("enable_legend", True)
            filter_string = recipe_cfg.get("filter_string", "")
            plot_min_max = recipe_cfg.get("plot_min_max", True)
            plot_std_dev = recipe_cfg.get("plot_std_dev", False)
            ymin, ymax = recipe_cfg.get("y_min_max", (None, None))
            hide_x_ticks_labels = recipe_cfg.get("hide_x_ticks_labels", False)
            hide_y_ticks_labels = recipe_cfg.get("hide_y_ticks_labels", False)

            ax = axes[idx + key * cols_n]
            
            for exp_cnt in experiments:
                experiment = experiments[exp_cnt]
                experiment_name = experiment["name"]
                experiment_pretty_name = experiment["pretty_name"]
                exp_extra_filter = experiment.get("extra_filter", "")

                exp_id = get_experiment_id(experiment_name)
                print(f">>> Experiment: {experiment_name} | ID: {exp_id}")
                df = mlflow.search_runs(
                    [exp_id],
                    order_by=[f"metrics.'{order_by}' DESC"],
                    filter_string=f"{filter_string} AND {exp_extra_filter}",
                )

                metrics_dfs = [None] * num_of_runs
                for run_idx, row in df.iterrows():
                    metrics_dfs[run_idx] = get_metric_data(row["run_id"], metric_name)

                    if run_idx == num_of_runs - 1:
                        print(
                            f"> Fetched {len(metrics_dfs)} runs for experiment '{experiment_name}'"
                        )
                        break

                # Merge all runs on 'step'
                if not metrics_dfs:
                    raise ValueError(
                        f"> No runs found for experiment '{experiment_name}' with metric '{metric_name}'"
                    )

                print(
                    f"> Merging {len(metrics_dfs)} runs for experiment '{experiment_name}'"
                )
                merged = pd.concat(
                    metrics_dfs, keys=range(len(metrics_dfs)), names=["run", "row"]
                ).reset_index(level=0)
                print(f"> Merged DataFrame shape.")
                print("> Preparing data for plotting...")
                
                
                # Pivot to have runs as columns, steps as index
                pivot = merged.pivot(index="step", columns="run", values="value")
                mean = pivot.mean(axis=1)
                color = COLORBLIND_COLORS[exp_cnt % len(COLORBLIND_COLORS)]

                print("> Plotting data...")
                ax.plot(
                    mean.index, mean.values, label=f"{experiment_pretty_name}", color=color
                )
                if plot_min_max:
                    min_ = pivot.min(axis=1)
                    max_ = pivot.max(axis=1)
                    ax.fill_between(mean.index, min_, max_, alpha=0.1, color=color)
                if plot_std_dev:
                    std = pivot.std(axis=1)
                    ax.fill_between(mean.index, mean - std, mean + std, alpha=0.2, color=color)

            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(plot_title)
            ax.grid()
            ax.ticklabel_format(
                style="sci", axis="y", scilimits=(0, 0)
            )  # Scientific notation for y-axis
            ax.set_ylim(ymin, ymax)
            if enable_legend:
                ax.legend(
                    loc="lower center",  # Place legend above the plot
                    bbox_to_anchor=(0.5, 1.02),  # 0.5 centers it, 1.02 puts it just above the axes
                    ncol=2,  # Number of columns (adjust as needed)
                    frameon=True,  # Optional: remove legend frame
                )
            print(f">> Plotting for {filename} done.")
    
    # Add labels below each chart in the last row
    labels = list(string.ascii_uppercase[:cols_n])
    for col in range(cols_n):
        ax = axes[(rows_n - 1) * cols_n + col]
        ax.annotate(
            f"$\\mathbf{{{labels[col]}}}$",
            xy=(0.5, -0.25),  # Centered below the axis
            xycoords='axes fraction',
            ha='center',
            va='center',
            fontsize=18,
            fontweight='bold'
        )
    
    # plt.show()
    # Save the plot and cleanup
    plt.tight_layout()
    plt.savefig(CHART_FILENAME, bbox_inches="tight")
    print(f">>> Plot saved to {CHART_FILENAME}")
    plt.clf()  # or plt.close() to fully release memory


if __name__ == "__main__":
    main()

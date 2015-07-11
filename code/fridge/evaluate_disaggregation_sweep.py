import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, mean_absolute_error

RESULTS_PATH = "../../bash_runs"

import os
import glob


def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


def f_score(df, lim=20):
    gt = (df > lim)[["GT"]]
    pred = (df > 20)[["CO", "FHMM", "Hart"]]
    o = {}
    for algo in ["CO", "FHMM", "Hart"]:
        o[algo] = f1_score(gt["GT"], pred[algo])
    return o


def mne(df):
    out_energy = {}
    x = df[["GT"]]
    gt_energy = x.sum().values[0]
    for algo in ["CO", "FHMM", "Hart"]:
        y = df[[algo]]
        algo_energy = y.sum().values[0]
        out_energy[algo] = np.abs(algo_energy - gt_energy) / gt_energy
    return out_energy

def mae(df):
    out = {}
    x = df[["GT"]].values
    for algo in ["CO", "FHMM", "Hart"]:
        y = df[[algo]].values
        out[algo] = mean_absolute_error(x, y)
    return out


metrics = {"mae power":mae,
            "error energy": mne,
           "f_score": f_score}

subdirs = get_immediate_subdirectories(RESULTS_PATH)

out = {}
for dir in subdirs:
    params = dir.split("_")
    num_states = int(params[0][1:])
    K = int(params[1][1:])
    train_fraction = int(params[2][1:])
    if num_states not in out:
        out[num_states] = {}
    if K not in out[num_states]:
        out[num_states][K] = {}
    if train_fraction not in out[num_states][K]:
        out[num_states][K][train_fraction] = {}
    # Find all H5 files
    dir_full_path = os.path.join(RESULTS_PATH, dir)
    homes = glob.glob(dir_full_path + "/*.h5")
    for home in homes:
        print num_states, K, train_fraction, home
        home_full_path = os.path.join(os.path.join(RESULTS_PATH, dir), home)
        with pd.HDFStore(home) as store:
            df = store['/disag'].dropna()
        home_name = home.split("/")[-1].split(".")[0]
        out[num_states][K][train_fraction][home_name] = {}
        for metric_name, metric_func in metrics.iteritems():
            out[num_states][K][train_fraction][home_name][metric_name] = metric_func(df)

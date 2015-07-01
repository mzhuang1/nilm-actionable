import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append("../common")


BASELINE_DUTY = 0.37

df = pd.read_csv("../../data/fridge/fridge_compressor_door.csv")
df_regular = df[df.Type == "Regular"].copy()


df_regular["on_minutes"] = (pd.to_datetime(df_regular["On end time"]) - pd.to_datetime(df_regular["On start time"])).astype("int") / (1e9 * 60)
df_regular["off_minutes"] = (pd.to_datetime(df_regular["Off end time"]) - pd.to_datetime(df_regular["Off start time"])).astype("int") / (
    1e9 * 60)

df_regular["duty_percentage"] = df_regular.on_minutes / (df_regular.on_minutes + df_regular.off_minutes)

#
def find_usage(df):
    cycle_mins =  (df["on_minutes"] + df["off_minutes"])
    usage_df = df.on_minutes - (cycle_mins*BASELINE_DUTY)
    usage_mins = usage_df.sum()
    return usage_mins

energy_activities_df = df_regular[df_regular["Energy activity"]]

true_usage_mins = find_usage(energy_activities_df)


error = {}
for threshold_percentage in range(1, 40):
    threshold = BASELINE_DUTY*1.0*threshold_percentage/100 + BASELINE_DUTY
    pred_df = df_regular[df_regular.duty_percentage>threshold]
    pred_df_mins = find_usage(pred_df)
    error[threshold_percentage] = (pred_df_mins-true_usage_mins)*1.0/true_usage_mins




result_df = pd.DataFrame({"error":error}).abs()


from common_functions import latexify, format_axes

for field in ["error"]:
    latexify(columns=1)
    ax = result_df[field].plot()
    ax.set_ylabel(r'Usage Energy Error $\%$')
    ax.set_xlabel("Percentage threshold")
    format_axes(ax)
    #plt.ylim((0, 1))
    plt.tight_layout()
    plt.savefig("../../figures/fridge/%s_fridge_activity_energy.png" %field)
    plt.savefig("../../figures/fridge/%s_fridge_activity_energy.pdf" %field)
    plt.close()




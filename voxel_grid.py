import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from demoparser2 import DemoParser
import os

def run_demo_pipeline(demo_path):
    print(f"Loading demo binary: {demo_path}")
    parser = DemoParser(demo_path)
    fields = ["X", "Y", "Z", "team_num"]
    df = parser.parse_ticks(fields)
    total_raw_ticks = len(df)
    print(f"Ingested {total_raw_ticks} raw ticks.")
    #filter dead/spec rows
    null_coords = df["X"].isna().sum() + df["Y"].isna().sum()
    spectator_ticks = len(df) - len(df[df["team_num"].isin([2, 3])])
    df = df.dropna(subset=["X", "Y"])
    df = df[df["team_num"].isin([2, 3])]
    print("\n--- Data Quality Summary ---")
    print(f"Total Ticks Parsed:    {total_raw_ticks}")
    print(f"Null Coordinates:      {null_coords}")
    print(f"Spectator Rows Dropped: {spectator_ticks}")
    print(f"Clean Records Retained: {len(df)}")
    print(f"Data Integrity Yield:   {round((len(df) / total_raw_ticks) * 100, 2)}%\n")
    #converting space to 25 unit grid
    voxel_size = 25
    df["grid_x"] = (df["X"] // voxel_size).astype(int)
    df["grid_y"] = (df["Y"] // voxel_size).astype(int)
    #saving data for powerbi/excel
    csv_out = "cleaned_match_telemetry.csv"
    df[["grid_x", "grid_y", "team_num"]].to_csv(csv_out, index=False)
    print(f"Exported tabular asset: {csv_out}")
    print("Generating visualization...")
    plt.figure(figsize=(12, 9))
    t_df = df[df["team_num"] == 2]
    ct_df = df[df["team_num"] == 3]
    plt.scatter(t_df["grid_x"], t_df["grid_y"], c="crimson", alpha=0.01, s=1, label="T")
    plt.scatter(ct_df["grid_x"], ct_df["grid_y"], c="dodgerblue", alpha=0.01, s=1, label="CT")
    plt.title("Spatial Telemetry: 25-Unit Grid Density Layout")
    plt.xlabel("Grid X")
    plt.ylabel("Grid Y")
    plt.legend(loc="upper left")
    plt.grid(True, linestyle=":", alpha=0.5)
    img_out = "spatial_density_map.png"
    plt.savefig(img_out, dpi=300, bbox_inches="tight")
    print(f"visualization saved: {img_out}")

if __name__ == "__main__":
    file_name = "spirit-vs-falcons-m3-dust2.dem"
    if os.path.exists(file_name):
        run_demo_pipeline(file_name)
    else:
        print(f"Err: Missing file '{file_name}' in current directory.")

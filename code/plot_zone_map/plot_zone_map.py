#!/usr/bin/env python3
"""
plot_management_zones.py

Combines NDVI (vegetation vigor) and soil fertility index data to classify
each grid cell into one of four management zones, then produces a 3-panel
figure (NDVI map, fertility map, management zone map) with a legend panel.

Management zones are defined by whether NDVI and fertility are above/below
their respective medians:
    0: High vigor / High fertility
    1: High vigor / Low fertility
    2: Low vigor / High fertility  (possible non-nutrient stress)
    3: Low vigor / Low fertility   (priority zone)

Usage:
    python plot_management_zones.py --ndvi <ndvi.csv> --fertility <fertility.csv> --output <plot.png>

Input CSVs must both contain a "col" and "row" column so they can be merged,
plus:
    --ndvi file:       "ndvi" column
    --fertility file:  "fertility_index" column
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend (safe for headless/script use)
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


def to_grid(df, value_col):
    """
    Convert a long-format dataframe (with 'row', 'col', value_col) into a
    2D numpy array suitable for imshow(), where grid[row, col] = value.

    Cells with no corresponding row/col in the dataframe are left as NaN.
    """
    ncols = df["col"].max() + 1
    nrows = df["row"].max() + 1
    grid = np.full((nrows, ncols), np.nan)

    # Vectorized assignment (equivalent to looping over rows, but faster)
    rows = df["row"].to_numpy(dtype=int)
    cols = df["col"].to_numpy(dtype=int)
    grid[rows, cols] = df[value_col].to_numpy()

    return grid


def classify_zone(row, ndvi_med, fert_med):
    """
    Classify a single grid cell into a management zone (0-3) based on
    whether its NDVI and fertility index are at/above their medians.
    """
    high_veg = row["ndvi"] >= ndvi_med
    high_fert = row["fertility_index"] >= fert_med

    if high_veg and high_fert:
        return 0
    elif high_veg and not high_fert:
        return 1
    elif not high_veg and high_fert:
        return 2
    else:
        return 3


def parse_args():
    """Parse and return command-line arguments."""
    p = argparse.ArgumentParser(description="Plot NDVI, fertility, and management zone maps.")
    p.add_argument("--ndvi", required=True, help="Path to CSV with col, row, ndvi columns")
    p.add_argument("--fertility", required=True, help="Path to CSV with col, row, fertility_index columns")
    p.add_argument("--output", required=True, help="Path to save the output figure (e.g. plot.png)")
    p.add_argument("--title", default="Field Management Zones", help="Title for the figure")
    return p.parse_args()


def main():
    args = parse_args()

    # --- Validate input files ------------------------------------------------
    for path, label in [(args.ndvi, "NDVI"), (args.fertility, "fertility")]:
        if not os.path.isfile(path):
            sys.exit(f"Error: {label} input file not found: {path}")

    ndvi = pd.read_csv(args.ndvi)
    fert = pd.read_csv(args.fertility)

    # --- Validate required columns -------------------------------------------
    required_ndvi_cols = {"col", "row", "ndvi"}
    required_fert_cols = {"col", "row", "fertility_index"}

    missing_ndvi = required_ndvi_cols - set(ndvi.columns)
    missing_fert = required_fert_cols - set(fert.columns)

    if missing_ndvi:
        sys.exit(f"Error: NDVI file missing column(s): {', '.join(sorted(missing_ndvi))}")
    if missing_fert:
        sys.exit(f"Error: fertility file missing column(s): {', '.join(sorted(missing_fert))}")

    # --- Merge datasets on grid position --------------------------------------
    df = ndvi.merge(fert, on=["col", "row"])

    if df.empty:
        sys.exit("Error: no matching (col, row) pairs found between NDVI and fertility files.")

    # --- Classify each cell into a management zone ----------------------------
    # Zones are relative: "high" means at/above the median value for this field.
    ndvi_med = df["ndvi"].median()
    fert_med = df["fertility_index"].median()

    df["zone"] = df.apply(lambda row: classify_zone(row, ndvi_med, fert_med), axis=1)

    # --- Convert long-format data into 2D grids for plotting ------------------
    ndvi_grid = to_grid(df, "ndvi")
    fert_grid = to_grid(df, "fertility_index")
    zone_grid = to_grid(df, "zone")

    zone_labels = [
        "High vigor / High fertility",
        "High vigor / Low fertility",
        "Low vigor / High fertility\n(check for non-nutrient stress)",
        "Low vigor / Low fertility\n(priority zone)",
    ]
    zone_colors = ["#1a9850", "#91cf60", "#fee08b", "#d73027"]

    # Count cells per zone (ensures all 4 zones appear even if count is 0)
    counts = df["zone"].value_counts().reindex(range(4), fill_value=0)

    # --- Build figure: 3 data panels + 1 legend panel -------------------------
    # width_ratios keeps the legend panel narrower than the plot panels
    fig, axes = plt.subplots(
        1, 4, figsize=(15, 4.5), dpi=150,
        gridspec_kw={"width_ratios": [1, 1, 1, 0.55]},
    )

    # Panel 1: NDVI heatmap
    im0 = axes[0].imshow(ndvi_grid, cmap="RdYlGn", vmin=df["ndvi"].min(), vmax=df["ndvi"].max())
    axes[0].set_title("Vegetation vigor (NDVI)", fontsize=11, fontweight="bold")
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    # Panel 2: Fertility heatmap
    im1 = axes[1].imshow(fert_grid, cmap="YlGnBu",
                          vmin=df["fertility_index"].min(), vmax=df["fertility_index"].max())
    axes[1].set_title("Soil fertility index", fontsize=11, fontweight="bold")
    fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

    # Panel 3: Discrete management zone map
    cmap = ListedColormap(zone_colors)
    axes[2].imshow(zone_grid, cmap=cmap, vmin=0, vmax=3)
    axes[2].set_title("Management zones", fontsize=11, fontweight="bold")

    # Shared axis formatting for the 3 data panels
    for ax in axes[:3]:
        ax.set_xlabel("Column")
        ax.set_ylabel("Row")
        ax.invert_yaxis()  # row 0 at top, matching typical grid/raster convention

    # --- Dedicated legend panel (no axes, no overlap with plots) -------------
    legend_ax = axes[3]
    legend_ax.axis("off")
    handles = [
        Patch(color=zone_colors[i], label=f"{zone_labels[i]}  (n={counts[i]})")
        for i in range(4)
    ]
    legend_ax.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(0.0, 0.5),
        fontsize=8.5,
        frameon=False,
        title="Zone legend",
        title_fontsize=9,
        handlelength=1.2,
        labelspacing=1.3,
    )

    fig.suptitle(args.title, fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(args.output, bbox_inches="tight")

    print(f"Saved plot to {args.output}")
    print(counts.to_string())


if __name__ == "__main__":
    main()
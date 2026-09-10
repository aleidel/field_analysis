#!/usr/bin/env python3
"""
compute_ndvi.py

Computes the Normalized Difference Vegetation Index (NDVI) for each grid cell
based on near-infrared (NIR) and red reflectance values.

NDVI = (NIR - Red) / (NIR + Red)

Usage:
    python compute_ndvi.py --reflectance <input.csv> --output <output.csv>

Input CSV must contain columns: col, row, nir, red
"""

import argparse
import os
import sys

import pandas as pd


def parse_args():
    """Parse and return command-line arguments."""
    p = argparse.ArgumentParser(description="Compute NDVI from reflectance data.")
    p.add_argument("--reflectance", required=True, help="Path to input CSV with NIR/Red reflectance")
    p.add_argument("--output", required=True, help="Path to write output CSV with NDVI values")
    return p.parse_args()


def main():
    args = parse_args()

    # --- Validate input file ------------------------------------------------
    if not os.path.isfile(args.reflectance):
        sys.exit(f"Error: input file not found: {args.reflectance}")

    df = pd.read_csv(args.reflectance)

    # --- Validate required columns ------------------------------------------
    required_cols = {"col", "row", "nir", "red"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        sys.exit(f"Error: missing required column(s): {', '.join(sorted(missing_cols))}")

    # --- Compute NDVI --------------------------------------------------------
    # NDVI compares reflected near-infrared light against reflected red light,
    # ranging from -1 to 1. Higher values typically indicate healthier/denser vegetation.
    denominator = df["nir"] + df["red"]

    # Guard against division by zero (e.g. where nir + red == 0)
    if (denominator == 0).any():
        print("Warning: found grid cell(s) with nir + red == 0; resulting NDVI will be NaN.")

    df["ndvi"] = (df["nir"] - df["red"]) / denominator

    # --- Write output ----------------------------------------------------------
    out = df[["col", "row", "ndvi"]]
    out.to_csv(args.output, index=False)

    # --- Summary report ----------------------------------------------------------
    print(f"Computed NDVI for {len(out)} grid cells.")
    print(f"NDVI range: {out['ndvi'].min():.3f} - {out['ndvi'].max():.3f}")
    print(f"Output written to: {args.output}")


if __name__ == "__main__":
    main()
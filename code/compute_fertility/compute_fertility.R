#!/usr/bin/env Rscript
# =============================================================================
# compute_fertility_index.R
#
# Computes a normalized soil fertility index (0-1) for each grid cell based on
# nitrate concentration and organic matter content. 
# This workflow can be run using the r-base:4.4.1 container image.
#
# Usage:
#   Rscript compute_fertility_index.R --soil <input.csv> --output <output.csv>
#
# Input CSV must contain columns: col, row, nitrate_ppm, organic_matter_pct
# =============================================================================

# --- Parse command-line arguments -------------------------------------------

args_raw <- commandArgs(trailingOnly = TRUE)

# Simple helper to extract the value following a given flag
# (e.g. get_arg("--soil") returns whatever comes after "--soil")
get_arg <- function(flag, default = NULL) {
  idx <- which(args_raw == flag)
  if (length(idx) == 0) return(default)
  args_raw[idx + 1]
}

soil_path   <- get_arg("--soil")
output_path <- get_arg("--output")

# Fail early with a helpful message if required args are missing
if (is.null(soil_path) || is.null(output_path)) {
  stop("Usage: Rscript compute_fertility_index.R --soil <input.csv> --output <output.csv>")
}

if (!file.exists(soil_path)) {
  stop(sprintf("Input file not found: %s", soil_path))
}

# --- Load data ---------------------------------------------------------------

df <- read.csv(soil_path, stringsAsFactors = FALSE)

required_cols <- c("col", "row", "nitrate_ppm", "organic_matter_pct")
missing_cols  <- setdiff(required_cols, names(df))

if (length(missing_cols) > 0) {
  stop(sprintf("Missing required column(s): %s", paste(missing_cols, collapse = ", ")))
}

# --- Compute fertility index --------------------------------------------------

# Min-max normalization scales a numeric vector to the range [0, 1]
minmax <- function(x) (x - min(x)) / (max(x) - min(x))

nitrate_norm <- minmax(df$nitrate_ppm)
om_norm      <- minmax(df$organic_matter_pct)

# Fertility index = equally weighted average of normalized nitrate and organic matter
df$fertility_index <- 0.5 * nitrate_norm + 0.5 * om_norm

# --- Write output -------------------------------------------------------------

out <- df[, c("col", "row", "fertility_index")]
write.csv(out, output_path, row.names = FALSE)

# --- Summary report -----------------------------------------------------------

cat(sprintf("Computed fertility index for %d grid cells.\n", nrow(out)))
cat(sprintf("Fertility index range: %.3f - %.3f\n",
            min(out$fertility_index), max(out$fertility_index)))
cat(sprintf("Output written to: %s\n", output_path))
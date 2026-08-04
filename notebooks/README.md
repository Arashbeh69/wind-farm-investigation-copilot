# Wind Farm Investigation Notebooks

This folder contains the analytical notebooks for the **Wind Farm Investigation Copilot** project.

## Why This Notebook Was Created

The final goal of the project is to build a system that can detect wind-turbine underperformance, retrieve relevant operational evidence, and generate a cautious investigation summary using GenAI.

Before building that system, we needed to understand the raw SCADA and status-event data:

- how the files are structured;
- whether timestamps and measurements are reliable;
- which variables are useful for performance investigations;
- how actual and potential production should be compared;
- whether production losses can be connected to turbine status events;
- what the future cleaning pipeline must produce.

This notebook is therefore the project’s initial data-validation and exploratory-analysis phase. It is not the finished copilot.

## Notebook

### [01 — Kelmarsh 2016 Data Validation and EDA](./01_2016_data_validation_and_eda.ipynb)

The notebook inventories six 2016 Kelmarsh SCADA files and six status-event files. All six SCADA schemas are compared, while detailed analysis focuses on Turbine 1 as a manageable development sample.

## What We Did

In this notebook we:

1. Inspected the Greenbyte export format and identified how the CSV files must be loaded.
2. Confirmed that all six 2016 SCADA files contain the same 299-column schema.
3. Validated Turbine 1 timestamps, data types, missingness, and measurement coverage.
4. Examined wind speed, actual power, and default potential power.
5. Created distributions and actual-versus-potential power curves.
6. Calculated power gaps and ten-minute energy differences.
7. Compared full-, reduced-, and zero-capacity operation.
8. Examined recorded downtime, performance, and curtailment losses.
9. Created monthly energy, wind, downtime, and coverage summaries.
10. Loaded and validated the status-event data.
11. Selected one evidence-rich period and aligned its SCADA behaviour with overlapping status events.
12. Defined the provisional data contract for the future reusable pipeline.

## Main Findings

For Turbine 1 in 2016:

- The SCADA data contains **52,416 ten-minute observations** and **299 columns**.
- A complete leap-year schedule would contain 52,704 observations.
- The first **288 timestamps are absent**, covering January 1–2.
- Wind speed, actual power, and potential power each have approximately **92.5% measurement availability**.
- Their 3,931 missing values occur on the same rows and are identified by the `Data Availability` field.
- Available capacity is equivalent to time-based system availability on a 2,050 kW scale, so both variables are not needed as separate evidence.
- Approximately **87.54%** of all observations show full available capacity, **8.14%** show zero capacity, **0.33%** show reduced capacity, and **3.99%** have missing capacity.
- Recorded downtime explains most typical power-gap energy during reduced- and zero-capacity operation.
- All inspected curtailment-loss fields are zero for this turbine-year. They cannot be permanently excluded until other turbines and years are checked.
- The status dataset contains **2,122 records**, including **1,473 closed intervals** and **649 start-only records**.
- Every closed status interval has a recorded duration matching its calculated start-to-end duration.

## Example Investigation

The notebook investigates Turbine 1 on **6 April 2016**, when the turbine moved between unavailable, reduced-capacity, and full-capacity operation.

During the day:

- Actual energy was approximately **21.03 MWh**.
- Potential energy was approximately **44.64 MWh**.
- Power-gap energy was approximately **23.61 MWh**.
- Recorded downtime loss was approximately **18.10 MWh**.
- The turbine spent approximately **11.33 hours at zero capacity** and **12.33 hours at full capacity**.

A `Repeating error BP52` forced outage from approximately 07:19 to 11:32 closely overlaps the period of zero available capacity. After the outage ended, `System OK` and `Gearbox warm-up stage` messages align with the turbine’s return to full capacity around 11:40.

This demonstrates the intended copilot workflow:

1. detect abnormal production;
2. examine wind, power, and availability;
3. retrieve overlapping status evidence;
4. calculate supporting metrics;
5. produce an evidence-based explanation;
6. clearly state uncertainty.

The timing provides strong supporting evidence, but it is not treated as automatic proof of causation.

## Notebook Outputs

The notebook produces:

- data-quality and temporal-coverage summaries;
- missingness and availability analysis;
- wind and power distributions;
- actual and potential power curves;
- capacity-state and production-loss summaries;
- monthly performance visualizations;
- validated status-event data;
- one documented investigation case;
- requirements for three future datasets:
  - a clean SCADA table;
  - a clean status-event table;
  - an investigation-case table.

## Scope and Limitations

Detailed analysis focuses on one turbine and one year. The findings must be validated across the other turbines and available years before the final data contract and cleaning pipeline are implemented.

Potential power is a reference estimate. A positive power gap is not automatically a confirmed fault or confirmed production loss.

The April 6 case was manually selected. Automated case detection will be developed and evaluated in a later project phase.

## Running the Notebook

The notebook was validated using Python 3.12 with pandas, NumPy, and Matplotlib.

Place the raw exports in:

```text
data/raw/kelmarsh_2016/

```

Raw datasets are excluded from Git because of their size.

Open the notebook with the project virtual environment, restart the kernel, and run all cells from top to bottom. All **55 code cells** were validated with zero execution errors.

## Next Phase

The next phase will profile all available turbines and years. The results will finalize the data contract before implementation of the reusable cleaning pipeline, case detector, status-evidence engine, and GenAI copilot.
# Wind Farm Investigation Notebooks

These notebooks establish the analytical foundation for the **Wind Farm
Investigation Copilot**. They examine how Kelmarsh wind-turbine performance can
be measured, how operational evidence can be retrieved from Status events, and
which data-quality rules the reusable pipeline must enforce.

The notebooks validate and document the data. They do not yet implement the
finished case detector or GenAI investigation interface.

## Notebook Index

### [01 — Kelmarsh 2016 Data Validation and EDA](./01_2016_data_validation_and_eda.ipynb)

This notebook uses Turbine 1 in 2016 as a detailed development sample. It
explores the Greenbyte export format, missingness, wind and power behaviour,
availability states, recorded production losses, monthly patterns, and Status
events.

It also develops one manual investigation case by aligning SCADA behaviour with
overlapping operational events.

### [02 — Cross-Turbine and Cross-Year Validation](./02_cross_turbine_cross_year_validation.ipynb)

This notebook validates the conclusions from the 2016 sample across all six
turbines and seven years. It profiles 42 SCADA files and 42 Status files without
combining the complete raw dataset in memory.

It verifies file completeness, schema evolution, timestamp coverage,
measurement availability, value ranges, Status-event integrity, and the final
cross-year data contract. It also exports the public
[`file_inventory.csv`](../data/file_inventory.csv).

## Detailed 2016 Investigation

The first notebook:

1. identifies how Greenbyte SCADA and Status exports must be loaded;
2. confirms that the six 2016 SCADA files share a 299-column schema;
3. validates Turbine 1 timestamps, data types, and missingness;
4. compares wind speed, actual power, and default potential power;
5. calculates power gaps and ten-minute energy differences;
6. examines full-, reduced-, and zero-capacity operation;
7. compares recorded downtime, performance, and curtailment evidence;
8. creates monthly energy, wind, downtime, and coverage summaries; and
9. aligns one underperformance period with overlapping Status events.

Key results for Turbine 1 in 2016 include:

- 52,416 ten-minute observations and 299 SCADA columns;
- 288 absent timestamps covering 1–2 January;
- approximately 92.5% availability for wind speed, actual power, and default
  potential power;
- 87.54% of observations at full available capacity, 8.14% at zero capacity,
  0.33% at reduced capacity, and 3.99% with missing capacity; and
- 2,122 Status records containing 1,473 closed intervals and 649 start-only
  records.

The example investigation examines Turbine 1 on 6 April 2016. A forced outage
labelled `Repeating error BP52` overlaps a long zero-capacity period, while later
`System OK` and `Gearbox warm-up stage` records align with recovery. This timing
is treated as supporting evidence rather than automatic proof of causation.

## Cross-Year Validation

The second notebook establishes that:

- all 84 expected SCADA and Status files are present exactly once at the
  turbine-year-file-type level;
- all observed SCADA timestamps are ordered, unique, and separated by regular
  ten-minute intervals;
- the six 2016 files begin on 3 January, while 2017–2022 have complete calendar
  timestamp coverage;
- SCADA contains 299 columns and Status contains 9 columns through 2020;
- 2021–2022 add four SCADA fields and two Status classification fields without
  removing earlier columns;
- the required investigation measurements exist in all 42 SCADA files;
- all turbines share a nominal rated power of 2,050 kW;
- small actual-power exceedances above the nominal rating and negative
  actual-power values occur consistently and should not be clipped
  automatically;
- curtailment-total evidence is meaningful only in 2022 and therefore remains
  optional and year-sensitive;
- 63,523 valid closed Status intervals have exact agreement between recorded
  and timestamp-derived durations;
- one malformed Status interval will be preserved with a quality flag but
  excluded from interval calculations; and
- 573 redundant exact Status rows, approximately 0.15% of all Status records,
  require deduplication in the cleaned table while the raw exports remain
  unchanged.

## Resulting Data Contract

The validation supports two separate processed tables.

The clean SCADA table will use one row per turbine and ten-minute UTC timestamp.
Its required cross-year measurements include wind speed, actual power, default
potential power, data availability, available capacity, and recorded downtime
loss. Performance loss, curtailment loss, later-year performance ratios, and
static turbine attributes remain optional supporting evidence.

The clean Status table will retain start-only and valid closed events, required
status codes and messages, nullable event categories, source traceability,
interval-validity flags, and duplicate counts. Overlapping non-identical events
remain separate because several operational statuses can occur simultaneously.

Neither table uses blanket imputation. Missing measurements, incomplete
calendar coverage, malformed intervals, and duplicate source evidence are
handled explicitly.

## Running the Notebooks

The notebooks use Python 3.12 with pandas, NumPy, and Matplotlib.

1. Follow the download and directory instructions in
   [`data/README.md`](../data/README.md).
2. Select the project virtual environment as the Jupyter kernel.
3. Open a notebook from this directory.
4. Restart the kernel and run all cells from top to bottom.

The notebooks discover the project root automatically when launched from either
the repository root or the `notebooks/` directory. Raw and processed datasets
are excluded from Git because of their size.

## Scope and Limitations

- Default potential power is a reference estimate, not fault-free ground truth.
- A positive actual-versus-potential gap is not automatically a confirmed fault
  or confirmed recoverable loss.
- Vendor performance-loss fields are signed metrics and require cautious
  interpretation.
- The 2016 files do not contain measurements for 1–2 January.
- Some useful fields are available only in later years or contain substantial
  missingness.
- Status timing provides supporting operational evidence but does not prove
  causation by itself.
- The investigation example was selected manually; automated case detection is
  not implemented in these notebooks.

## What This Enables

The validated data contract can now be implemented as a tested, memory-aware
cleaning pipeline. That pipeline will create processed SCADA and Status tables,
support automatic underperformance-case detection, assemble evidence packages,
and provide grounded inputs to the GenAI investigation component.

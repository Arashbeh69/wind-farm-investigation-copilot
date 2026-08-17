# Project Data

This directory stores the local data used by the **Wind Farm Investigation
Copilot** project. Large raw and processed files are intentionally excluded from
Git; this README documents how to obtain and organize them.

## Data Source

The project uses the open [Kelmarsh Wind Farm dataset on
Zenodo](https://zenodo.org/records/8252025), published by Cubico Sustainable
Investments Ltd under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

The dataset contains ten-minute SCADA and status-event exports for six Senvion
MM92 wind turbines from 2016 through 2022. It also provides turbine static data,
signal mappings, site information, and additional meter data.

DOI: [10.5281/zenodo.8252025](https://doi.org/10.5281/zenodo.8252025)

## Files Used by This Project

Download the yearly SCADA archives:

- `Kelmarsh_SCADA_2016_3082.zip`
- `Kelmarsh_SCADA_2017_3083.zip`
- `Kelmarsh_SCADA_2018_3084.zip`
- `Kelmarsh_SCADA_2019_3085.zip`
- `Kelmarsh_SCADA_2020_3086.zip`
- `Kelmarsh_SCADA_2021_4456.zip`
- `Kelmarsh_SCADA_2022_4457.zip`

Also download:

- `Kelmarsh_WT_static.csv`
- `Kelmarsh_WT_dataSignalMapping.csv`

The Zenodo record also contains grid-meter, PMU, and KMZ files. These files are
not required to reproduce the analyses currently included in this repository.

## Expected Local Structure

After downloading and extracting the files, use this structure:

```text
data/
├── README.md
├── file_inventory.csv
├── raw/
│   ├── kelmarsh_2016/
│   ├── kelmarsh_2017/
│   ├── kelmarsh_2018/
│   ├── kelmarsh_2019/
│   ├── kelmarsh_2020/
│   ├── kelmarsh_2021/
│   ├── kelmarsh_2022/
│   └── metadata/
│       ├── Kelmarsh_WT_static.csv
│       └── Kelmarsh_WT_dataSignalMapping.csv
├── interim/
└── processed/
```

Each yearly directory should contain that year's extracted turbine SCADA and
status-event CSV files. The archives may also remain inside their corresponding
yearly directories for traceability.

## Data Availability in This Repository

The full raw and processed datasets are not included in the Git repository because of their size. The `data/raw/`, `data/interim/`, and `data/processed/` directories are excluded through `.gitignore`.

The repository contains only documentation and small metadata artifacts such as [`file_inventory.csv`](./file_inventory.csv). Use the source and directory instructions above to reproduce the local data setup.

## Validated Dataset Scope

- The project uses SCADA and Status-event data from all six Kelmarsh turbines for 2016–2022.
- Each yearly dataset contains six turbine SCADA files and six Status-event files.
- Turbine static metadata and signal mappings are stored locally under `data/raw/metadata/`.
- The 2016 exploratory notebook examines Turbine 1 in detail to establish the investigation workflow and initial cleaning requirements.
- The cross-year validation notebook verifies file completeness, schema changes, timestamp coverage, measurement availability, value ranges, and Status-event integrity across all 84 raw files.
- [`file_inventory.csv`](./file_inventory.csv) provides a tracked metadata-only inventory without publishing raw measurements or local absolute paths.
- The resulting data contract defines the required, optional, derived, and excluded fields for the future cleaning pipeline.

See [`../notebooks/README.md`](../notebooks/README.md) for notebook descriptions and analytical findings.

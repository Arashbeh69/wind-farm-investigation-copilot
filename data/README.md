# Project Data

This directory stores the local data used by the **Wind Farm Investigation
Copilot** project. Large raw and processed files are intentionally excluded from
Git; this README documents how to obtain and organize them.

## Data Source

The project uses the open [Kelmarsh Wind Farm dataset on
Zenodo](https://zenodo.org/records/8252025), published by Cubico Sustainable
Investments Ltd under the **CC BY 4.0** license.

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

The grid-meter, PMU, and KMZ files are available from the same record but are
outside the current project scope. They may be added later if they provide
useful investigation evidence.

## Expected Local Structure

After downloading and extracting the files, use this structure:

```text
data/
├── README.md
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

## Repository Policy

The following directories are ignored by Git:

- `data/raw/`
- `data/interim/`
- `data/processed/`

Only documentation, code, and small metadata summaries should be committed.
Never commit the full SCADA archives, extracted raw CSV files, or generated
processed datasets.

## Current Project Status

- The 2016 archive and its six SCADA and six status files are available locally.
- Phase 1 validated the 2016 schema and performed detailed EDA on Turbine 1.
- Phase 2 will acquire the 2017–2022 archives and validate schemas, timestamp
  coverage, missingness, units, and investigation fields across all turbines and
  years.

See [`../notebooks/README.md`](../notebooks/README.md) for the completed Phase 1
analysis and results.

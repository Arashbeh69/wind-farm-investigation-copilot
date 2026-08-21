import pandas as pd

from .discovery import SourceFileIdentity


_REQUIRED_SCADA_COLUMN_MAP = {
    "# Date and time": "timestamp",
    "Wind speed (m/s)": "wind_speed_ms",
    "Power (kW)": "actual_power_kw",
    "Potential power default PC (kW)": "potential_power_kw",
    "Data Availability": "data_available",
    "Available Capacity for Production (kW)": "available_capacity_kw",
    "Lost Production to Downtime (kWh)": "downtime_loss_kwh",
}

_OPTIONAL_SCADA_COLUMN_MAP = {
    "Lost Production to Performance (kWh)": "performance_loss_kwh",
    "Lost Production to Curtailment (Total) (kWh)": "curtailment_loss_kwh",
    "Investment Performance Ratio": "investment_performance_ratio",
    "Operating Performance Ratio": "operating_performance_ratio",
    "Potential Power Energy Budget (kW)": "potential_power_energy_budget_kw",
}

_SCADA_COLUMN_MAP = _REQUIRED_SCADA_COLUMN_MAP | _OPTIONAL_SCADA_COLUMN_MAP


def load_scada_file(source: SourceFileIdentity) -> pd.DataFrame:
    if source.file_type != "SCADA":
        raise ValueError(
            f"Expected a SCADA source, but '{source.source_file.name}' "
            f"has file type '{source.file_type}'."
        )

    scada_data = pd.read_csv(
        source.source_file,
        skiprows=9,
        usecols=lambda column: column in _SCADA_COLUMN_MAP,
    )

    required_columns = set(_REQUIRED_SCADA_COLUMN_MAP)
    loaded_columns = set(scada_data.columns)
    missing_required_columns = required_columns - loaded_columns
    if missing_required_columns:
        raise ValueError(
            f"SCADA file '{source.source_file.name}' is missing required columns: "
            f"{sorted(missing_required_columns)}"
        )

    scada_data = scada_data.rename(columns=_SCADA_COLUMN_MAP)
    scada_data["timestamp"] = pd.to_datetime(
        scada_data["timestamp"],
        errors="raise",
        utc=True,
    )

    scada_data["data_available"] = scada_data["data_available"].astype("boolean")
    scada_data["file_year"] = source.file_year
    scada_data["turbine_id"] = source.turbine_id
    scada_data["source_file"] = source.source_file.name
    return scada_data

from pathlib import Path

import pandas as pd
import pytest

from wind_farm_copilot.discovery import SourceFileIdentity
from wind_farm_copilot.scada import load_scada_file


def _write_test_scada_file(file_path: Path, scada_rows: pd.DataFrame) -> None:
    metadata_text = "# test metadata\n" * 9
    file_path.write_text(metadata_text, encoding="utf-8")
    scada_rows.to_csv(file_path, mode="a", index=False)


def test_loads_and_standardizes_scada_file(tmp_path: Path) -> None:
    scada_file = (
        tmp_path
        / "Turbine_Data_Kelmarsh_3_2021-01-01_-_2022-01-01_230.csv"
    )

    raw_rows = pd.DataFrame(
        {
            "# Date and time": [
                "2021-01-01 00:00:00",
                "2021-01-01 00:10:00",
            ],
            "Wind speed (m/s)": [5.0, 8.0],
            "Power (kW)": [200.0, 800.0],
            "Potential power default PC (kW)": [250.0, 900.0],
            "Data Availability": [1, 0],
            "Available Capacity for Production (kW)": [2050.0, 0.0],
            "Lost Production to Downtime (kWh)": [0.0, 100.0],
            "Lost Production to Performance (kWh)": [2.0, 0.0],
        }
    )

    _write_test_scada_file(scada_file, raw_rows)
    scada_source = SourceFileIdentity(
        source_file=scada_file,
        file_type="SCADA",
        file_year=2021,
        turbine_id=3,
    )
    loaded_scada = load_scada_file(scada_source)
    assert loaded_scada.shape == (2, 11)

    expected_columns = {
        "timestamp",
        "wind_speed_ms",
        "actual_power_kw",
        "potential_power_kw",
        "data_available",
        "available_capacity_kw",
        "downtime_loss_kwh",
        "performance_loss_kwh",
        "file_year",
        "turbine_id",
        "source_file",
    }

    assert set(loaded_scada.columns) == expected_columns
    assert loaded_scada.loc[0, "timestamp"] == pd.Timestamp(
        "2021-01-01 00:00:00",
        tz="UTC",
    )

    assert loaded_scada["data_available"].tolist() == [True, False]
    assert loaded_scada["performance_loss_kwh"].tolist() == [2.0, 0.0]
    assert loaded_scada["file_year"].eq(2021).all()
    assert loaded_scada["turbine_id"].eq(3).all()

    assert loaded_scada["source_file"].eq(scada_file.name).all()

    assert pd.api.types.is_datetime64_any_dtype(
        loaded_scada["timestamp"],
    )
    assert str(loaded_scada["timestamp"].dt.tz) == "UTC"

    assert pd.api.types.is_bool_dtype(
        loaded_scada["data_available"],
    )


def test_rejects_non_scada_source(tmp_path: Path) -> None:
    status_source = SourceFileIdentity(
        source_file=tmp_path / "Status_Kelmarsh_3_2021.csv",
        file_type="Status",
        file_year=2021,
        turbine_id=3,
    )

    with pytest.raises(ValueError, match="Expected a SCADA source"):
        load_scada_file(status_source)


def test_rejects_scada_file_missing_required_column(tmp_path: Path) -> None:
    scada_file = tmp_path / "Turbine_Data_Kelmarsh_3_2021.csv"
    incomplete_rows = pd.DataFrame(
        {
            "# Date and time": ["2021-01-01 00:00:00"],
            "Wind speed (m/s)": [5.0],
            "Potential power default PC (kW)": [250.0],
            "Data Availability": [1],
            "Available Capacity for Production (kW)": [2050.0],
            "Lost Production to Downtime (kWh)": [0.0],
        }
    )

    _write_test_scada_file(scada_file, incomplete_rows)

    scada_source = SourceFileIdentity(
        source_file=scada_file,
        file_type="SCADA",
        file_year=2021,
        turbine_id=3,
    )

    with pytest.raises(ValueError, match="missing required columns"):
        load_scada_file(scada_source)


def test_rejects_invalid_scada_timestamp(tmp_path: Path) -> None:
    scada_file = tmp_path / "Turbine_Data_Kelmarsh_3_2021.csv"
    invalid_timestamp_rows = pd.DataFrame(
        {
            "# Date and time": ["not-a-timestamp"],
            "Wind speed (m/s)": [5.0],
            "Power (kW)": [200.0],
            "Potential power default PC (kW)": [250.0],
            "Data Availability": [1],
            "Available Capacity for Production (kW)": [2050.0],
            "Lost Production to Downtime (kWh)": [0.0],
        }
    )

    _write_test_scada_file(scada_file, invalid_timestamp_rows)

    scada_source = SourceFileIdentity(
        source_file=scada_file,
        file_type="SCADA",
        file_year=2021,
        turbine_id=3,
    )
    with pytest.raises(ValueError):
        load_scada_file(scada_source)

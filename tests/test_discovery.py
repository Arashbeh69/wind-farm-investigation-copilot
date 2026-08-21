from pathlib import Path

import pytest

from wind_farm_copilot.discovery import discover_source_files
from wind_farm_copilot.discovery import parse_source_identity
from wind_farm_copilot.discovery import SourceFileIdentity


def test_empty_directory_returns_empty_list(tmp_path: Path) -> None:
    discovered_files = discover_source_files(tmp_path)
    assert discovered_files == []


def test_discovers_scada_and_status_files_in_nested_directory(tmp_path: Path) -> None:
    year_directory = tmp_path / "kelmarsh_2016"
    year_directory.mkdir()

    scada_file = year_directory / "Turbine_Data_Kelmarsh_1_2016.csv"
    scada_file.touch()

    status_file = year_directory / "Status_Kelmarsh_1_2016.csv"
    status_file.touch()

    discovered_files = discover_source_files(tmp_path)
    assert discovered_files == sorted([scada_file, status_file])


def test_parses_scada_and_status_identity() -> None:
    scada_file = Path("Turbine_Data_Kelmarsh_3_2021-01-01_-_2022-01-01_230.csv")
    status_file = Path("Status_Kelmarsh_1_2016-01-03_-_2017-01-01_228.csv")

    scada_identity = parse_source_identity(scada_file)
    status_identity = parse_source_identity(status_file)

    assert scada_identity == SourceFileIdentity(
        source_file=scada_file,
        file_type="SCADA",
        file_year=2021,
        turbine_id=3
    )
    assert status_identity == SourceFileIdentity(
        source_file=status_file,
        file_type="Status",
        file_year=2016,
        turbine_id=1
    )


def test_rejects_unrecognized_source_filename() -> None:
    invalid_file = Path("Wind_Data_Kelmarsh_3_2021-01-01_-_2022-01-01_230.csv")
    pytest.raises(ValueError, parse_source_identity, invalid_file)
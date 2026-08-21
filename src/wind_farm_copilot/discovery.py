import re
from dataclasses import dataclass
from pathlib import Path


_SOURCE_FILE_PATTERN = re.compile(
    r"^(?P<file_prefix>Turbine_Data|Status)_Kelmarsh_"
    r"(?P<turbine_id>\d+)_(?P<file_year>\d{4})-.*\.csv$"
)


@dataclass(frozen=True)
class SourceFileIdentity:
    source_file: Path
    file_type: str
    file_year: int
    turbine_id: int


def parse_source_identity(source_file: Path) -> SourceFileIdentity:
    match = _SOURCE_FILE_PATTERN.fullmatch(source_file.name)
    if match is None:
        raise ValueError(f"Unrecognized source filename: {source_file.name}")

    file_prefix = match.group("file_prefix")
    file_type = "SCADA" if file_prefix == "Turbine_Data" else "Status"

    file_year = int(match.group("file_year"))
    turbine_id = int(match.group("turbine_id"))

    return SourceFileIdentity(
        source_file=source_file,
        file_type=file_type,
        file_year=file_year,
        turbine_id=turbine_id,
    )


def discover_source_files(raw_data_dir: Path) -> list[Path]:
    scada_files = list(raw_data_dir.rglob("Turbine_Data_Kelmarsh_*.csv"))
    status_files = list(raw_data_dir.rglob("Status_Kelmarsh_*.csv"))
    source_files = scada_files + status_files
    return sorted(source_files)
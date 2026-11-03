"""Read uploaded price files and build download payloads."""

from io import BytesIO

import pandas as pd

SUPPORTED_PRICE_FILE_TYPES = ("csv", "xlsx")


class UnsupportedFileTypeError(ValueError):
    """Raised when an uploaded price file is neither CSV nor XLSX."""


def read_price_file(file, file_name: str) -> pd.DataFrame:
    """Read a CSV or Excel price file indexed by its ``Date`` column."""
    _, dot, extension = file_name.rpartition(".")
    extension = extension.lower() if dot else ""
    if extension == "csv":
        return pd.read_csv(file, index_col="Date")
    if extension == "xlsx":
        return pd.read_excel(file, index_col="Date")
    raise UnsupportedFileTypeError("You need to upload a csv or xlsx file.")


def dataframe_to_excel_bytes(data: pd.DataFrame) -> bytes:
    """Return ``data`` as the bytes of an .xlsx workbook with a Data sheet."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        data.to_excel(writer, sheet_name="Data")
    return buffer.getvalue()

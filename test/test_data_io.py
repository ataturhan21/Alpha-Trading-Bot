"""Offline regression checks for uploaded and downloaded price files."""

import unittest
from io import BytesIO, StringIO

import pandas as pd
from app.data_io import (
    UnsupportedFileTypeError,
    dataframe_to_excel_bytes,
    read_price_file,
)


class DataIoTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {"Close": [1.5, 2.5]},
            index=pd.Index(["2024-01-01", "2024-01-02"], name="Date"),
        )

    def test_excel_download_contains_the_data(self):
        payload = dataframe_to_excel_bytes(self.data)
        self.assertGreater(len(payload), 0)
        restored = pd.read_excel(
            BytesIO(payload), sheet_name="Data", index_col="Date"
        )
        self.assertEqual(restored["Close"].tolist(), [1.5, 2.5])

    def test_reads_csv_by_extension(self):
        file = StringIO("Date,Close\n2024-01-01,1.5\n")
        result = read_price_file(file, "AAPL.CSV")
        self.assertEqual(result.loc["2024-01-01", "Close"], 1.5)

    def test_reads_xlsx_by_extension(self):
        file = BytesIO(dataframe_to_excel_bytes(self.data))
        result = read_price_file(file, "AAPL-data.xlsx")
        self.assertEqual(result["Close"].tolist(), [1.5, 2.5])

    def test_rejects_unsupported_extensions(self):
        for name in ("AAPL.xlx", "AAPL.txt", "AAPL"):
            with self.subTest(name=name):
                with self.assertRaises(UnsupportedFileTypeError):
                    read_price_file(BytesIO(b""), name)


if __name__ == "__main__":
    unittest.main()

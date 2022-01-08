import pandas as pd

from data_source.data_source_interface import IDataSource


class CsvDataSource(IDataSource):

    def __init__(self, filename: str):
        self.filename = filename

    def load(self):
        self.data = pd.read_csv(self.filename)

    def get_dataframe(self) -> pd.DataFrame:
        return self.data

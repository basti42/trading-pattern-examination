import json
import pandas as pd
from data_source.data_source_interface import IDataSource


class ExampleJsonDataSource(IDataSource):

    def __init__(self, filename: str):
        self.filename = filename

    def load(self):
        with open(self.filename, "r") as input_file:
            json_data = json.loads(input_file.read())
        # create dataframe from the "Data" attribute of the json file
        self.data = pd.DataFrame(json_data["Data"],
                                 columns=["close", "high", "low", "open", "time", "volumefrom", "volumeto"],
                                 dtype="float64")
        # add human readable dates
        posix_time = pd.to_datetime(self.data["time"], unit="s")
        self.data.insert(0, "date", posix_time)

    def get_dataframe(self) -> pd.DataFrame:
        return self.data

import pandas as pd


class IDataSource:
    """
    However the data is stored, its needs to represented internally as a pandas dataframe
    of type float64 and needs to contain at least the following 4 columns:
    'open', 'high', 'low', 'close'
    """

    def load(self):
        raise NotImplementedError("load method needs to be implemented")

    def get_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError("get_dataframe methods needs to be implemented")

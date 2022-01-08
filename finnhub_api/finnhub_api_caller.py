from pathlib import Path

import finnhub
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from secrets import FINNHUB_API_KEY


class ApiCaller(finnhub.Client):

    def __init__(self, api_key: str = FINNHUB_API_KEY):
        super().__init__(api_key=api_key)
        self.output_directory = Path(Path(__file__).parent.resolve(), "api_results")

    def get_latest_candle(self, sym: str):
        yesterday = datetime.today() - timedelta(1)
        unix_time_yesterday = yesterday.strftime("%s")
        json_data = self.stock_candles(
            symbol=sym,
            resolution='D',
            _from=unix_time_yesterday,
            to=datetime.today().strftime("%s")
        )
        df = pd.DataFrame(json_data,
                          index=None,
                          columns=list(json_data.keys()))
        df.rename(columns={"c": "close", "h": "high", "o": "open", "l": "low",
                           "s": "status", "v": "volume"}, inplace=True)
        posix_time = pd.to_datetime(df["t"], unit='s')
        df.insert(0, "date", posix_time)

    def get_candles_for_symbol(self, sym: str, time_from, time_to):
        """ https://finnhub.io/docs/api/stock-candles """
        json_data = self.stock_candles(
            symbol=sym,
            resolution="D",
            _from=time_from,
            to=time_to
        )
        filename = f"{sym}_{datetime.utcfromtimestamp(time_from).strftime('%Y-%m-%d %H:%M:%S')}_" \
                   f"{datetime.utcfromtimestamp(time_to).strftime('%Y-%m-%d %H:%M:%S')}.csv"
        df = pd.DataFrame(json_data,
                          index=None,
                          columns=list(json_data.keys()))
        df.rename(columns={"c": "close", "h": "high", "o": "open", "l": "low",
                           "s": "status", "v": "volume"}, inplace=True)
        posix_time = pd.to_datetime(df["t"], unit='s')
        df.insert(0, "date", posix_time)

        # for plotting
        close_vals = df['close'].values
        open_vals = df['open'].values
        color_vals = np.ndarray(shape=(len(close_vals)), dtype="int")
        for i, (o, c) in enumerate(zip(open_vals, close_vals)):
            color_vals[i] = 1 if o < c else 0
        df['coloring'] = color_vals

        df.to_csv(path_or_buf=Path(self.output_directory, filename), index=False)


if __name__ == "__main__":

    caller = ApiCaller()
    caller.get_candles_for_symbol(sym="TSLA", time_from=1609455600, time_to=1640991599)
    caller.get_latest_candle(sym="TSLA")

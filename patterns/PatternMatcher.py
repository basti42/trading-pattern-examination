import numpy as np
import talib

from data_source.data_source_interface import IDataSource
from data_source.json_source import ExampleJsonDataSource

from patterns.pattern_rankings import overall_performance_ranking


class PatternMatcher:

    """
    Pattern Matching Class. Instantiated with a data source handler fitting the IDataSource interface.
    A ranking of patterns needs to be provided in the form of the default candle_rankings.
    TALib (Technical Analysis Library) documentation can be found here:
    https://ta-lib.org/function.html, https://github.com/mrjbq7/ta-lib
    """

    def __init__(self, data_source: IDataSource, rankings: dict = overall_performance_ranking):
        self.data_source = data_source
        self.data_source.load()
        self.data = self.data_source.get_dataframe().copy()
        self.rankings = rankings
        self.candle_pattern_names = talib.get_function_groups()["Pattern Recognition"]

    def find_patterns(self):
        """
        finds known patterns (see get_candle_pattern_names) in the candle data represented
        like so: (open, high, low, close)
        """
        _open = self.data["open"]
        _high = self.data["high"]
        _low = self.data["low"]
        _close = self.data["close"]
        for pattern in self.candle_pattern_names:
            self.data[pattern] = getattr(talib, pattern)(_open, _high, _low, _close)

    def rank_patterns(self):
        """
        Determines the "best" pattern for a candle based off the provided ranking dictionary
        """
        self.data["candlestick_pattern"] = np.nan
        self.data["candlestick_match_count"] = np.nan
        for index, row in self.data.iterrows():
            # first case: no pattern found:
            if len(row[self.candle_pattern_names]) - sum(row[self.candle_pattern_names] == 0) == 0:
                self.data.loc[index, "candlestick_pattern"] = "NO PATTERN"
                self.data.loc[index, "candlestick_match_count"] = 0
            # second case: only one pattern found
            elif len(row[self.candle_pattern_names]) - sum(row[self.candle_pattern_names] == 0) == 1:
                # bull pattern = 100 or 200
                if any(row[self.candle_pattern_names].values > 0):
                    mask = row[self.candle_pattern_names].values != 0
                    pattern = row[self.candle_pattern_names].keys().to_numpy()[mask].tolist()[0] + "_Bull"
                    self.data.loc[index, "candlestick_pattern"] = pattern
                    self.data.loc[index, "candlestick_match_count"] = 1
                # bear pattern = -100 or -200
                else:
                    mask = row[self.candle_pattern_names].values != 0
                    pattern = row[self.candle_pattern_names].keys().to_numpy()[mask].tolist()[0] + "_Bear"
                    self.data.loc[index, "candlestick_pattern"] = pattern
                    self.data.loc[index, "candlestick_match_count"] = 1
            # multiple patterns
            else:
                mask = row[self.candle_pattern_names].values != 0
                patterns = row[self.candle_pattern_names].keys().to_numpy()[mask].tolist()
                container = list()
                unknown_ranking_patterns = list()
                for pattern in patterns:
                    if row[pattern] > 0:
                        bull_pattern = pattern + "_Bull"
                        if bull_pattern not in self.rankings:
                            unknown_ranking_patterns.append(bull_pattern)
                            continue
                        container.append(bull_pattern)
                    else:
                        bear_pattern = pattern + "_Bear"
                        if bear_pattern not in self.rankings:
                            unknown_ranking_patterns.append(bear_pattern)
                            continue
                        container.append(bear_pattern)
                rank_list = [self.rankings[p] for p in container if p]
                if len(rank_list) == len(container) > 0:
                    rank_index_best = rank_list.index(min(rank_list))
                    self.data.loc[index, "candlestick_pattern"] = container[rank_index_best]
                    self.data.loc[index, "candidate_match_count"] = len(container)

                if unknown_ranking_patterns:
                    print(f"[i] Row {index+1}: Found {len(unknown_ranking_patterns)} patterns without ranking."
                          f" Skipping those: {unknown_ranking_patterns}")

    def get_candle_pattern_names(self) -> [str]:
        return self.candle_pattern_names

    def to_csv(self, output_filename: str = "pattern_matcher_out.csv"):
        self.data.to_csv(path_or_buf=output_filename, index=False)


if __name__ == "__main__":

    ds = ExampleJsonDataSource(filename="../examples/btc_eur.json")
    matcher = PatternMatcher(data_source=ds)

    matcher.find_patterns()

    matcher.rank_patterns()

    matcher.to_csv()
    print()

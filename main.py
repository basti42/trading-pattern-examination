from data_source.csv_source import CsvDataSource
from data_source.json_source import ExampleJsonDataSource

from patterns.PatternMatcher import PatternMatcher


if __name__ == "__main__":

    ds = CsvDataSource(filename="finnhub_api/api_results/TSLA_2020-12-31 23:00:00_2021-12-31 22:59:59.csv")
    matcher = PatternMatcher(data_source=ds)

    matcher.find_patterns()

    matcher.rank_patterns()

    matcher.to_csv(output_filename="__output/TSLA_csv_test_out.csv")
    print()
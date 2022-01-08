import panel as pn
import pandas as pd
from pathlib import Path

from plotting import plot_candles


def __find_files__() -> [Path]:
    parent_directory = Path(__file__).parent.parent.resolve()
    files = list()
    data_output_directory = Path(parent_directory, "__output")
    print(f">>  {data_output_directory}")
    for file in data_output_directory.iterdir():
        if str(file).endswith("_out.csv"):
            files.append(file)
    return files


def create_app() -> pn.Pane:
    LAYOUT = pn.template.MaterialTemplate(title="Candle Stick Show")
    LAYOUT.header_background = "#421C52"  # purple

    LAYOUT.main.sizing_mode = "stretch_width"
    out_files = __find_files__()
    data = pd.read_csv(out_files[0])
    dropdown = pn.widgets.Select(name="Select a file to examine", options=[str(f).split("/")[-1] for f in out_files])

    @pn.depends(
        dropdown.param.value,
        watch=True
    )
    def update_candlestick_plot(file_name):
        print(f">>  {file_name}")
        file_path = None
        for f in out_files:
            if str(f).endswith(file_name):
                file_path = f
                break

        if not file_path:
            print(f"Unable to find file")
            return

        d = pd.read_csv(file_path)

        LAYOUT.main.objects[1][0] = show_candlestick_plot(df=d, title=file_name)
        LAYOUT.main.objects[2][0] = show_candlestick_metrics(df=d, title=file_name)

    def show_candlestick_plot(df: pd.DataFrame, title: str):
        return plot_candles(df=df, title=title)

    def show_candlestick_metrics(df: pd.DataFrame, title: str):
        return pn.widgets.DataFrame(df[['date', 'candlestick_pattern', 'open', 'high', 'low', 'close']],
                                    name=title, height=300, frozen_columns=1,
                                    autosize_mode="none", width=950,
                                    widths={"date": 200, "candlestick_pattern": 300, "open": 100, "high": 100,
                                            "low": 100, "close": 100})

    LAYOUT.main.append(pn.Row(dropdown))
    LAYOUT.main.append(
        pn.Row(show_candlestick_plot(df=data, title=dropdown.value))
    )
    LAYOUT.main.append(
        pn.Row(show_candlestick_metrics(df=data, title=dropdown.value))
    )

    return LAYOUT


if __name__ == "__main__":
    servable = create_app()
    servable.show()

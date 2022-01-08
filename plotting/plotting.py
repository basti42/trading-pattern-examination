import holoviews as hv
import pandas as pd

hv.extension("bokeh")


def plot_candles(df: pd.DataFrame, title: str):

    hls = hv.Segments(df, ['date', 'low', 'date', 'high']).opts(responsive=True, line_width=1,
                                                                color='coloring', cmap=['red', 'green'])
    segments = hv.Segments(df, [hv.Dimension('date', label='date'),
                                hv.Dimension('open', label="price"),
                                "date",
                                "close"],
                           )
    # labels = hv.Labels({('date', 'open'): df, 'text': df['candlestick_pattern']}, ['date', 'open'], 'text')
    return segments.opts(
        responsive=True, height=500, xrotation=90,
        show_grid=True, line_width=3,
        title=title,
        color='coloring', cmap=["red", "green"],
    ) * hls
    # * labels.opts(yoffset=3, yrotation=90)

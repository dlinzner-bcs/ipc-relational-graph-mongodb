"""Core I/O module."""
import pandas as pd


def parse_edge_list(filepath, **kwargs):
    """Parse edge list."""
    df = pd.read_csv(filepath, **kwargs)
    labels = sorted(list(set(df.values[:, 0]) | set(df.values[:, 1])))
    return df, labels

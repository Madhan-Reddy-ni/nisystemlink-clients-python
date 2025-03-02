from typing import List, Optional
import pandas as pd

from nisystemlink.clients.testmonitor._test_monitor_client import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    ResultProjection
)


def get_results_dataframe(
    client: TestMonitorClient,
    query_filter: str,
    column_projection: Optional[List[ResultProjection]] = None,
) -> pd.DataFrame:
    """Fetches results of a specific product and normalizes them into a Pandas DataFrame.

    Args:
        client: The TestMonitorClient to fetch results data.
        query_filter: The filter to use when querying the results.
        column_projection: List of columns to retrieve from the queried results.

    Returns:
        A Pandas DataFrame containing the results.
    """
    results = client.get_results(query_filter=query_filter, column_projection=column_projection)
    return pd.DataFrame(results)

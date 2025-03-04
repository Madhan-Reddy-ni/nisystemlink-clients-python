from typing import List, Optional

import pandas as pd
from nisystemlink.clients.testmonitor._test_monitor_client import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    QueryResultsRequest,
    Result,
    ResultProjection,
)


def __query_results_batched(
    client: TestMonitorClient,
    query_filter: str,
    column_projection: Optional[List[ResultProjection]] = None,
) -> List[Result]:
    """Fetches results of a specific product in batches.

    Args:
        client: The TestMonitorClient to fetch results data.
        query_filter: The filter to use when querying the results.
        column_projection: List of columns to retrieve when querying the results.
            Fields you do not specify are excluded. Returns all fields if no value is specified.

    Returns:
        List[Results]: A list of results.
    """
    all_results: List[Result] = []
    query_request = QueryResultsRequest(
        filter=query_filter, projection=column_projection, take=1000
    )

    query_response = client.query_results(query_request)
    all_results.extend(query_response.results)

    while query_response.continuation_token:
        query_request.continuation_token = query_response.continuation_token
        query_response = client.query_results(query_request)
        all_results.extend(query_response.results)

    return all_results


def __normalize_results(results: List[Result]) -> pd.DataFrame:
    """Normalizes the results into a Pandas DataFrame.

    Args:
        results: The list of results to normalize.

    Returns:
        A Pandas DataFrame with the normalized queried results.
    """
    results_dict = [results.dict(exclude_unset=True) for results in results]
    normalized_results = pd.json_normalize(results_dict, sep=".")

    return normalized_results


def get_results_dataframe(
    client: TestMonitorClient,
    query_filter: str,
    column_projection: Optional[List[ResultProjection]] = None,
) -> pd.DataFrame:
    """Fetches results of a specific product and normalizes them into a Pandas DataFrame.

    Args:
        client: The TestMonitorClient to fetch results data.
        query_filter: The filter to use when querying the results.
        column_projection: List of columns to retrieve when querying the results.
            Fields you do not specify are excluded. Returns all fields if no value is specified.

    Returns:
        A Pandas DataFrame containing the results.
    """
    queried_results = __query_results_batched(client, query_filter, column_projection)

    results_dataframe = __normalize_results(queried_results)

    return results_dataframe

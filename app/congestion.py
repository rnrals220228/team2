"""Mock congestion rules that update graph edges by time and zone."""

from datetime import datetime

import networkx as nx


def time_based_congestion(base_congestion: float, zone: str, current_time: datetime) -> float:
    """Return congestion adjusted by mock zone and time rules."""

    congestion = base_congestion
    hour = current_time.hour
    is_weekend = current_time.weekday() >= 5

    if zone == "school_zone" and 7 <= hour <= 9:
        congestion *= 1.7
    elif zone == "market_zone" and is_weekend:
        congestion *= 1.6
    elif zone == "tourist_zone" and 13 <= hour <= 18:
        congestion *= 1.5

    return round(congestion, 2)


def apply_congestion(graph: nx.Graph, current_time: datetime) -> nx.Graph:
    """Copy a graph and update every edge's congestion for the given time."""

    updated = graph.copy()
    for _, _, data in updated.edges(data=True):
        base = float(data.get("base_congestion", data.get("congestion", 1.0)))
        zone = str(data.get("zone", "normal"))
        data["congestion"] = time_based_congestion(base, zone, current_time)
    return updated

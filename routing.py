"""A* route search with personalized pedestrian edge costs."""

import math
from dataclasses import dataclass

import networkx as nx

from app.graph import NodeId, nearest_node
from app.models import UserProfile
from app.user_profile import edge_is_accessible, user_preference_multiplier


@dataclass(frozen=True)
class RouteResult:
    """Internal route result used before serializing an API response."""

    node_ids: list[NodeId]
    coordinates: list[tuple[float, float]]
    total_distance: float
    total_cost: float
    estimated_time_minutes: float


def heuristic(graph: nx.Graph, node_a: NodeId, node_b: NodeId) -> float:
    """Estimate remaining distance using Euclidean distance."""

    ax, ay = graph.nodes[node_a]["pos"]
    bx, by = graph.nodes[node_b]["pos"]
    return math.dist((ax, ay), (bx, by))


def edge_cost(edge_data: dict, user: UserProfile) -> float:
    """Calculate personalized traversal cost for one edge."""

    if not edge_is_accessible(edge_data, user):
        return math.inf

    distance = float(edge_data["distance"])
    congestion = float(edge_data["congestion"])
    preference = user_preference_multiplier(edge_data, user)
    return distance * congestion * preference


def find_route(
    graph: nx.Graph,
    start_coordinate: tuple[float, float],
    end_coordinate: tuple[float, float],
    user: UserProfile,
) -> RouteResult:
    """Find the best personalized path between two coordinates with A*."""

    start_node = nearest_node(graph, start_coordinate)
    end_node = nearest_node(graph, end_coordinate)

    def weight(_: NodeId, __: NodeId, data: dict) -> float:
        """NetworkX-compatible dynamic edge weight function."""

        return edge_cost(data, user)

    path = nx.astar_path(
        graph,
        start_node,
        end_node,
        heuristic=lambda a, b: heuristic(graph, a, b),
        weight=weight,
    )

    total_distance = 0.0
    total_cost = 0.0
    for node_a, node_b in zip(path, path[1:]):
        data = graph.edges[node_a, node_b]
        total_distance += float(data["distance"])
        total_cost += edge_cost(data, user)

    coordinates = [graph.nodes[node]["pos"] for node in path]
    walking_speed_m_per_minute = 80.0
    distance_unit_meters = 50.0
    estimated_time = total_distance * distance_unit_meters / walking_speed_m_per_minute

    return RouteResult(
        node_ids=path,
        coordinates=coordinates,
        total_distance=round(total_distance, 2),
        total_cost=round(total_cost, 2),
        estimated_time_minutes=round(estimated_time, 2),
    )

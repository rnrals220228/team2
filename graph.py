"""Mock pedestrian map graph generation."""

import networkx as nx

NodeId = str


def _node_id(x: int, y: int) -> NodeId:
    """Build a stable node id for a grid coordinate."""

    return f"{x},{y}"


def create_mock_graph(width: int = 6, height: int = 6) -> nx.Graph:
    """Create a small 2D pedestrian graph with rich edge attributes."""

    graph = nx.Graph()

    for x in range(width):
        for y in range(height):
            graph.add_node(_node_id(x, y), pos=(float(x), float(y)))

    for x in range(width):
        for y in range(height):
            if x + 1 < width:
                _add_mock_edge(graph, x, y, x + 1, y)
            if y + 1 < height:
                _add_mock_edge(graph, x, y, x, y + 1)

    return graph


def _add_mock_edge(graph: nx.Graph, x1: int, y1: int, x2: int, y2: int) -> None:
    """Add one edge with deterministic mock pedestrian attributes."""

    zone = _zone_for_edge(x1, y1, x2, y2)
    stair = (x1 == 2 and x2 == 3 and y1 in {1, 2, 3}) or (y1 == 4 and y2 == 5 and x1 == 4)
    braille = not ((x1 in {1, 4} and y1 in {2, 3}) or (x2 in {1, 4} and y2 in {2, 3}))
    slope = round(((x1 + x2 + y1 + y2) % 5) / 5, 2)
    base_congestion = 1.0 + (((x1 * 3 + y1 * 2 + x2 + y2) % 4) * 0.2)

    graph.add_edge(
        _node_id(x1, y1),
        _node_id(x2, y2),
        distance=1.0,
        base_congestion=round(base_congestion, 2),
        congestion=round(base_congestion, 2),
        stair=stair,
        braille=braille,
        slope=slope,
        zone=zone,
    )


def _zone_for_edge(x1: int, y1: int, x2: int, y2: int) -> str:
    """Assign a mock congestion zone from edge location."""

    avg_x = (x1 + x2) / 2
    avg_y = (y1 + y2) / 2

    if avg_y <= 1:
        return "school_zone"
    if avg_x >= 4:
        return "market_zone"
    if avg_y >= 4:
        return "tourist_zone"
    return "normal"


def nearest_node(graph: nx.Graph, coordinate: tuple[float, float]) -> NodeId:
    """Find the graph node nearest to an arbitrary coordinate."""

    x, y = coordinate
    return min(
        graph.nodes,
        key=lambda node: (graph.nodes[node]["pos"][0] - x) ** 2 + (graph.nodes[node]["pos"][1] - y) ** 2,
    )

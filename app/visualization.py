"""Route visualization with Folium."""

from pathlib import Path

import folium
import networkx as nx


def visualize_route(graph: nx.Graph, path: list[str], output_path: str = "data/route.html") -> str:
    """Draw all graph edges in gray and the selected route in red."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    pos = nx.get_node_attributes(graph, "pos")
    center = _to_lat_lon(pos[path[0]]) if path else (37.5665, 126.9780)
    route_map = folium.Map(location=center, zoom_start=16)

    for node_a, node_b, data in graph.edges(data=True):
        folium.PolyLine(
            [_to_lat_lon(pos[node_a]), _to_lat_lon(pos[node_b])],
            color="#9e9e9e",
            weight=3,
            opacity=0.65,
            tooltip=(
                f"distance={data['distance']}, congestion={data['congestion']}, "
                f"stair={data['stair']}, braille={data['braille']}, slope={data['slope']}"
            ),
        ).add_to(route_map)

    route_points = [_to_lat_lon(pos[node]) for node in path]
    folium.PolyLine(route_points, color="#d62728", weight=7, opacity=0.95).add_to(route_map)

    for index, node in enumerate(path):
        folium.CircleMarker(
            location=_to_lat_lon(pos[node]),
            radius=5,
            color="#d62728",
            fill=True,
            fill_color="#d62728",
            tooltip=f"{index}: {node}",
        ).add_to(route_map)

    route_map.save(output)
    return str(output)


def _to_lat_lon(point: tuple[float, float]) -> tuple[float, float]:
    """Convert mock grid coordinates to map-like latitude and longitude."""

    x, y = point
    return 37.5665 + y * 0.001, 126.9780 + x * 0.001

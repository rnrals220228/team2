"""FastAPI entry point for the pedestrian AI routing prototype."""

from datetime import datetime

import networkx as nx
from fastapi import FastAPI, HTTPException

from app.congestion import apply_congestion
from app.graph import create_mock_graph
from app.models import RouteRequest, RouteResponse, UserProfile
from app.routing import find_route
from app.visualization import visualize_route

app = FastAPI(title="Pedestrian AI Routing Prototype")
BASE_GRAPH = create_mock_graph()


@app.get("/")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""

    return {"status": "ok", "service": "pedestrian-ai-routing"}


@app.post("/route", response_model=RouteResponse)
def calculate_route(request: RouteRequest) -> RouteResponse:
    """Calculate a personalized route from request coordinates and user profile."""

    graph = apply_congestion(BASE_GRAPH, request.current_time)

    try:
        result = find_route(graph, request.start, request.end, request.user)
    except nx.NetworkXNoPath as exc:
        raise HTTPException(status_code=404, detail="No accessible route found for this user.") from exc

    visualization_path = visualize_route(graph, result.node_ids)

    return RouteResponse(
        path=result.coordinates,
        node_ids=result.node_ids,
        estimated_time_minutes=result.estimated_time_minutes,
        total_distance=result.total_distance,
        total_cost=result.total_cost,
        visualization_path=visualization_path,
    )


def run_sample() -> None:
    """Run one mock route calculation when executing this file directly."""

    sample_request = RouteRequest(
        start=(0.0, 0.0),
        end=(5.0, 5.0),
        user=UserProfile(
            visual_impairment=False,
            panic_disorder=True,
            stairs_preference=-0.8,
            slope_preference=-0.5,
        ),
        current_time=datetime(2026, 5, 30, 14, 0),
    )
    response = calculate_route(sample_request)

    print("Sample personalized route")
    print(f"nodes: {response.node_ids}")
    print(f"path: {response.path}")
    print(f"estimated_time_minutes: {response.estimated_time_minutes}")
    print(f"total_distance: {response.total_distance}")
    print(f"total_cost: {response.total_cost}")
    print(f"visualization_path: {response.visualization_path}")


if __name__ == "__main__":
    run_sample()

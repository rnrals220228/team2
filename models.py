"""Pydantic request and response models for the routing API."""

from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel, Field


Coordinate: TypeAlias = tuple[float, float]


class UserProfile(BaseModel):
    """Pedestrian characteristics used to personalize edge costs."""

    visual_impairment: bool = Field(default=False)
    panic_disorder: bool = Field(default=False)
    stairs_preference: float = Field(default=0.0, ge=-1.0, le=1.0)
    slope_preference: float = Field(default=0.0, ge=-1.0, le=1.0)


class RouteRequest(BaseModel):
    """Input payload for POST /route."""

    start: Coordinate
    end: Coordinate
    user: UserProfile
    current_time: datetime


class RouteResponse(BaseModel):
    """Output payload with the selected path and summary metrics."""

    path: list[Coordinate]
    node_ids: list[str]
    estimated_time_minutes: float
    total_distance: float
    total_cost: float
    visualization_path: str

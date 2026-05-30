"""Cost adjustments based on user characteristics."""

from app.models import UserProfile


def edge_is_accessible(edge_data: dict, user: UserProfile) -> bool:
    """Return whether a user may use an edge at all."""

    if user.visual_impairment and not edge_data.get("braille", False):
        return False
    return True


def user_preference_multiplier(edge_data: dict, user: UserProfile) -> float:
    """Calculate a multiplicative cost adjustment for user preferences."""

    multiplier = 1.0

    if user.panic_disorder:
        congestion = float(edge_data.get("congestion", 1.0))
        if congestion >= 1.5:
            multiplier *= 1.0 + (congestion - 1.0) * 1.2

    if edge_data.get("stair", False) and user.stairs_preference < 0:
        multiplier *= 1.0 + abs(user.stairs_preference) * 2.5

    slope = float(edge_data.get("slope", 0.0))
    if user.slope_preference < 0:
        multiplier *= 1.0 + slope * abs(user.slope_preference) * 2.0

    return multiplier

"""
Thruster upgrade mappings.
"""

from mappings.registry import MappingCategory


THRUSTER_PAIRS = {
    # Ion
    "LargeBlockSmallThrust": "LargeBlockLargeThrust",
    "SmallBlockSmallThrust": "SmallBlockLargeThrust",
    # Hydrogen
    "LargeBlockSmallHydrogenThrust": "LargeBlockLargeHydrogenThrust",
    "SmallBlockSmallHydrogenThrust": "SmallBlockLargeHydrogenThrust",
    # Atmospheric
    "LargeBlockSmallAtmosphericThrust": "LargeBlockLargeAtmosphericThrust",
    "SmallBlockSmallAtmosphericThrust": "SmallBlockLargeAtmosphericThrust",
}


def get_category() -> MappingCategory:
    return MappingCategory(
        name="thrusters",
        description="Tier upgrades for ion, hydrogen, and atmospheric thrusters.",
        pairs=THRUSTER_PAIRS,
        grid_sizes=("Large", "Small"),
        enabled_by_default=False,
        tags=("propulsion", "upgrade"),
    )


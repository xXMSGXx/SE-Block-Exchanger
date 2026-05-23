"""
DLC to base game (vanilla) replacement mappings.
Helps players eliminate DLC requirements from downloaded blueprints.
"""

from mappings.registry import MappingCategory

DLC_TO_BASE_PAIRS = {
    # ============================================================
    # THRUSTERS (Industrial & Sci-Fi DLCs to Vanilla counterparts)
    # ============================================================
    # Sci-Fi Ion Thrusters
    "LargeBlockSmallThrustSciFi": "LargeBlockSmallThrust",
    "LargeBlockLargeThrustSciFi": "LargeBlockLargeThrust",
    "SmallBlockSmallThrustSciFi": "SmallBlockSmallThrust",
    "SmallBlockLargeThrustSciFi": "SmallBlockLargeThrust",
    
    # Sci-Fi Atmospheric Thrusters
    "LargeBlockSmallAtmosphericThrustSciFi": "LargeBlockSmallAtmosphericThrust",
    "LargeBlockLargeAtmosphericThrustSciFi": "LargeBlockLargeAtmosphericThrust",
    "SmallBlockSmallAtmosphericThrustSciFi": "SmallBlockSmallAtmosphericThrust",
    "SmallBlockLargeAtmosphericThrustSciFi": "SmallBlockLargeAtmosphericThrust",
    
    # Sci-Fi Hydrogen Thrusters
    "LargeBlockSmallHydrogenThrustSciFi": "LargeBlockSmallHydrogenThrust",
    "LargeBlockLargeHydrogenThrustSciFi": "LargeBlockLargeHydrogenThrust",
    "SmallBlockSmallHydrogenThrustSciFi": "SmallBlockSmallHydrogenThrust",
    "SmallBlockLargeHydrogenThrustSciFi": "SmallBlockLargeHydrogenThrust",
    
    # Industrial Thrusters (Hydrogen / Ion)
    "LargeBlockSmallHydrogenThrustIndustrial": "LargeBlockSmallHydrogenThrust",
    "LargeBlockLargeHydrogenThrustIndustrial": "LargeBlockLargeHydrogenThrust",
    "SmallBlockSmallHydrogenThrustIndustrial": "SmallBlockSmallHydrogenThrust",
    "SmallBlockLargeHydrogenThrustIndustrial": "SmallBlockLargeHydrogenThrust",
    
    "LargeBlockSmallThrustIndustrial": "LargeBlockSmallThrust",
    "LargeBlockLargeThrustIndustrial": "LargeBlockLargeThrust",
    "SmallBlockSmallThrustIndustrial": "SmallBlockSmallThrust",
    "SmallBlockLargeThrustIndustrial": "SmallBlockLargeThrust",
    
    # ============================================================
    # COCKPITS & CONTROLS (Decorative, Wasteland, Warfare DLCs)
    # ============================================================
    "IndustrialCockpit": "LargeBlockCockpit",
    "IndustrialCockpitSmall": "Cockpit",
    "BuggyCockpit": "Cockpit",
    "CabCockpit": "Cockpit",
    "RoverCockpit": "Cockpit",
    "WastelandCockpit": "Cockpit",
    "OpenCockpitLarge": "LargeBlockCockpit",
    "OpenCockpitSmall": "Cockpit",
    "SubattachedCockpit": "Cockpit",
    "TacticalMap": "ControlPanel",
    
    # ============================================================
    # INDUSTRIAL & PRODUCTION BLOCKS
    # ============================================================
    "LargeIndustrialAssembler": "LargeAssembler",
    "LargeIndustrialRefinery": "LargeRefinery",
    "IndustrialSeparator": "LargeBlockSmallContainer",
    "SmallIndustrialContainer": "SmallBlockSmallContainer",
    "LargeIndustrialContainer": "LargeBlockLargeContainer",
    "IndustrialCargo1": "LargeBlockSmallContainer",
    "IndustrialCargo2": "LargeBlockLargeContainer",
    
    # ============================================================
    # COMBAT/WEAPONS RESKINS
    # ============================================================
    "GatlingTurretReskin": "LargeGatlingTurret",
    "MissileTurretReskin": "LargeMissileTurret",
    "LargeBlockInteriorTurretWarfare2": "LargeInteriorTurret",
    "SmallBlockGatlingTurretWarfare2": "SmallGatlingTurret",
    "SmallBlockGatlingGunWarfare2": "SmallGatlingGun",
    
    # ============================================================
    # SE2 TRANSITION PREP/DECORATIVE BLOCKS
    # ============================================================
    "StoreBlockSingle": "StoreBlock",
    "VendingMachineSingle": "VendingMachine",
    "AtmosphericThrusterDusted": "LargeBlockSmallAtmosphericThrust",
}

def get_category() -> MappingCategory:
    return MappingCategory(
        name="dlc_substitution",
        description="Replaces paid DLC blocks with standard, base-game (Vanilla) alternatives.",
        pairs=DLC_TO_BASE_PAIRS,
        grid_sizes=("Large", "Small"),
        enabled_by_default=False,
        tags=("utility", "vanilla", "dlc"),
    )

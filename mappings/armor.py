"""
Armor block mappings.
"""

from mappings.registry import MappingCategory


ARMOR_PAIRS = {
    # ============================================================
    # LARGE GRID - Standard shapes
    # ============================================================
    "LargeBlockArmorBlock": "LargeHeavyBlockArmorBlock",
    "LargeBlockArmorSlope": "LargeHeavyBlockArmorSlope",
    "LargeBlockArmorCorner": "LargeHeavyBlockArmorCorner",
    "LargeBlockArmorCornerInv": "LargeHeavyBlockArmorCornerInv",
    # Round armor
    "LargeRoundArmor_Slope": "LargeHeavyRoundArmor_Slope",
    "LargeRoundArmor_Corner": "LargeHeavyRoundArmor_Corner",
    "LargeRoundArmor_CornerInv": "LargeHeavyRoundArmor_CornerInv",
    # 2x1 slopes and corners
    "LargeBlockArmorSlope2Base": "LargeHeavyBlockArmorSlope2Base",
    "LargeBlockArmorSlope2Tip": "LargeHeavyBlockArmorSlope2Tip",
    "LargeBlockArmorCorner2Base": "LargeHeavyBlockArmorCorner2Base",
    "LargeBlockArmorCorner2Tip": "LargeHeavyBlockArmorCorner2Tip",
    "LargeBlockArmorInvCorner2Base": "LargeHeavyBlockArmorInvCorner2Base",
    "LargeBlockArmorInvCorner2Tip": "LargeHeavyBlockArmorInvCorner2Tip",
    # Half blocks
    "LargeHalfArmorBlock": "LargeHeavyHalfArmorBlock",
    "LargeHalfSlopeArmorBlock": "LargeHeavyHalfSlopeArmorBlock",
    # Panels
    "LargeArmorPanelLight": "LargeArmorPanelHeavy",
    # Sloped corners
    "LargeArmorSlopedCorner": "LargeHeavyArmorSlopedCorner",
    "LargeArmorSlopedCornerTip": "LargeHeavyArmorSlopedCornerTip",
    "LargeArmorSlopedCornerBase": "LargeHeavyArmorSlopedCornerBase",
    # ============================================================
    # LARGE GRID - Extended shapes (Decorative / Warfare DLC)
    # ============================================================
    # Half slope corners
    "LargeBlockArmorHalfSlopeCorner": "LargeHeavyBlockArmorHalfSlopeCorner",
    "LargeBlockArmorHalfSlopeCornerInverted": "LargeHeavyBlockArmorHalfSlopeCornerInverted",
    # Half corners
    "LargeBlockArmorHalfCorner": "LargeHeavyBlockArmorHalfCorner",
    # Half slope inverted
    "LargeBlockArmorHalfSlopedCorner": "LargeHeavyBlockArmorHalfSlopedCorner",
    "LargeBlockArmorHalfSlopedCornerBase": "LargeHeavyBlockArmorHalfSlopedCornerBase",
    # Slope transitions
    "LargeBlockArmorSlopeTransition": "LargeHeavyBlockArmorSlopeTransition",
    "LargeBlockArmorSlopeTransitionBase": "LargeHeavyBlockArmorSlopeTransitionBase",
    "LargeBlockArmorSlopeTransitionTip": "LargeHeavyBlockArmorSlopeTransitionTip",
    "LargeBlockArmorSlopeTransitionMirrored": "LargeHeavyBlockArmorSlopeTransitionMirrored",
    "LargeBlockArmorSlopeTransitionBaseMirrored": "LargeHeavyBlockArmorSlopeTransitionBaseMirrored",
    "LargeBlockArmorSlopeTransitionTipMirrored": "LargeHeavyBlockArmorSlopeTransitionTipMirrored",
    # Quarter / corner combos
    "LargeArmorQuarterBlock": "LargeHeavyArmorQuarterBlock",
    "LargeBlockArmorRoundedSlope": "LargeHeavyBlockArmorRoundedSlope",
    "LargeBlockArmorRoundedCorner": "LargeHeavyBlockArmorRoundedCorner",
    # Armor panels (additional shapes)
    "LargeArmorPanelLightSlope": "LargeArmorPanelHeavySlope",
    "LargeArmorPanelLightHalfSlope": "LargeArmorPanelHeavyHalfSlope",
    # ============================================================
    # SMALL GRID - Standard shapes
    # ============================================================
    "SmallBlockArmorBlock": "SmallHeavyBlockArmorBlock",
    "SmallBlockArmorSlope": "SmallHeavyBlockArmorSlope",
    "SmallBlockArmorCorner": "SmallHeavyBlockArmorCorner",
    "SmallBlockArmorCornerInv": "SmallHeavyBlockArmorCornerInv",
    # Round armor
    "SmallRoundArmor_Slope": "SmallHeavyRoundArmor_Slope",
    "SmallRoundArmor_Corner": "SmallHeavyRoundArmor_Corner",
    "SmallRoundArmor_CornerInv": "SmallHeavyRoundArmor_CornerInv",
    # 2x1 slopes and corners
    "SmallBlockArmorSlope2Base": "SmallHeavyBlockArmorSlope2Base",
    "SmallBlockArmorSlope2Tip": "SmallHeavyBlockArmorSlope2Tip",
    "SmallBlockArmorCorner2Base": "SmallHeavyBlockArmorCorner2Base",
    "SmallBlockArmorCorner2Tip": "SmallHeavyBlockArmorCorner2Tip",
    "SmallBlockArmorInvCorner2Base": "SmallHeavyBlockArmorInvCorner2Base",
    "SmallBlockArmorInvCorner2Tip": "SmallHeavyBlockArmorInvCorner2Tip",
    # Half blocks
    "SmallHalfArmorBlock": "SmallHeavyHalfArmorBlock",
    "SmallHalfSlopeArmorBlock": "SmallHeavyHalfSlopeArmorBlock",
    # Panels
    "SmallArmorPanelLight": "SmallArmorPanelHeavy",
    # Sloped corners
    "SmallArmorSlopedCorner": "SmallHeavyArmorSlopedCorner",
    "SmallArmorSlopedCornerTip": "SmallHeavyArmorSlopedCornerTip",
    "SmallArmorSlopedCornerBase": "SmallHeavyArmorSlopedCornerBase",
    # ============================================================
    # SMALL GRID - Extended shapes (Decorative / Warfare DLC)
    # ============================================================
    # Half slope corners
    "SmallBlockArmorHalfSlopeCorner": "SmallHeavyBlockArmorHalfSlopeCorner",
    "SmallBlockArmorHalfSlopeCornerInverted": "SmallHeavyBlockArmorHalfSlopeCornerInverted",
    # Half corners
    "SmallBlockArmorHalfCorner": "SmallHeavyBlockArmorHalfCorner",
    # Half slope inverted
    "SmallBlockArmorHalfSlopedCorner": "SmallHeavyBlockArmorHalfSlopedCorner",
    "SmallBlockArmorHalfSlopedCornerBase": "SmallHeavyBlockArmorHalfSlopedCornerBase",
    # Slope transitions
    "SmallBlockArmorSlopeTransition": "SmallHeavyBlockArmorSlopeTransition",
    "SmallBlockArmorSlopeTransitionBase": "SmallHeavyBlockArmorSlopeTransitionBase",
    "SmallBlockArmorSlopeTransitionTip": "SmallHeavyBlockArmorSlopeTransitionTip",
    "SmallBlockArmorSlopeTransitionMirrored": "SmallHeavyBlockArmorSlopeTransitionMirrored",
    "SmallBlockArmorSlopeTransitionBaseMirrored": "SmallHeavyBlockArmorSlopeTransitionBaseMirrored",
    "SmallBlockArmorSlopeTransitionTipMirrored": "SmallHeavyBlockArmorSlopeTransitionTipMirrored",
    # Quarter / corner combos
    "SmallArmorQuarterBlock": "SmallHeavyArmorQuarterBlock",
    "SmallBlockArmorRoundedSlope": "SmallHeavyBlockArmorRoundedSlope",
    "SmallBlockArmorRoundedCorner": "SmallHeavyBlockArmorRoundedCorner",
    # Armor panels (additional shapes)
    "SmallArmorPanelLightSlope": "SmallArmorPanelHeavySlope",
    "SmallArmorPanelLightHalfSlope": "SmallArmorPanelHeavyHalfSlope",
}


def get_category() -> MappingCategory:
    return MappingCategory(
        name="armor",
        description="Vanilla armor conversions between light and heavy variants.",
        pairs=ARMOR_PAIRS,
        grid_sizes=("Large", "Small"),
    )


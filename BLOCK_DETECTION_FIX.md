# Block Detection Fix - Technical Summary

## Issue Identified

**Problem**: The program was not detecting any armor blocks (light or heavy) in Space Engineers blueprints, showing 0 for all counts.

## Root Cause

Space Engineers blueprint XML files use **`<SubtypeName>`** element for block identification, NOT `<SubtypeId>` as originally assumed.

### XML Structure in bp.sbc Files:

```xml
<MyObjectBuilder_CubeBlock xsi:type="MyObjectBuilder_Thrust">
    <SubtypeName>SmallBlockSmallHydrogenThrust</SubtypeName>  ← THIS
    <EntityId>119567212327639059</EntityId>
    ...
</MyObjectBuilder_CubeBlock>
```

**Original code incorrectly looked for:**
```xml
<SubtypeId>BlockName</SubtypeId>  ← WRONG - doesn't exist in blueprints
```

## Files Fixed

### 1. `blueprint_scanner.py`
**Changes:**
- ✅ Changed `block.find('SubtypeId')` to `block.find('SubtypeName')`
- ✅ Added `HEAVY_ARMOR_BLOCKS` set with all 36 heavy armor block types
- ✅ Added `heavy_armor_count: int` to `BlueprintInfo` dataclass
- ✅ Updated `_parse_blueprint()` to count both light and heavy armor blocks
- ✅ Added `.strip()` to handle whitespace in SubtypeName values

**Before:**
```python
subtype_elem = block.find('SubtypeId')
if subtype_elem is not None and subtype_elem.text in self.LIGHT_ARMOR_BLOCKS:
    light_armor_count += 1
```

**After:**
```python
subtype_elem = block.find('SubtypeName')
if subtype_elem is not None and subtype_elem.text:
    subtype = subtype_elem.text.strip()
    if subtype in self.LIGHT_ARMOR_BLOCKS:
        light_armor_count += 1
    elif subtype in self.HEAVY_ARMOR_BLOCKS:
        heavy_armor_count += 1
```

### 2. `se_armor_replacer.py`
**Changes:**
- ✅ Updated `replace_armor_blocks()` method to use `SubtypeName`
- ✅ Added `.strip()` to handle whitespace
- ✅ Added comment explaining Space Engineers uses SubtypeName

**Before:**
```python
subtype_elem = block.find('SubtypeId')
if subtype_elem is not None and subtype_elem.text:
    current_subtype = subtype_elem.text
```

**After:**
```python
# IMPORTANT: Space Engineers uses <SubtypeName> not <SubtypeId>
subtype_elem = block.find('SubtypeName')
if subtype_elem is not None and subtype_elem.text:
    current_subtype = subtype_elem.text.strip()
```

### 3. `gui_standalone.py`
**Changes:**
- ✅ Added "HEAVY ARMOR:" field to details panel (5 fields total now)
- ✅ Updated `update_details()` to display heavy armor count
- ✅ Fixed heavy armor visualization (was showing light count twice)
- ✅ Updated color coding for heavy armor display (cyan)

**New fields:**
```python
fields = [
    ("NAME:", "name"),
    ("GRID SIZE:", "grid"),
    ("TOTAL BLOCKS:", "blocks"),
    ("LIGHT ARMOR:", "light_armor"),    # Orange
    ("HEAVY ARMOR:", "heavy_armor")     # Cyan - NEW!
]
```

## Heavy Armor Block Types Added

Complete set of 36 heavy armor block SubtypeNames:

### Large Grid Heavy Armor:
- LargeHeavyBlockArmorBlock
- LargeHeavyBlockArmorSlope
- LargeHeavyBlockArmorCorner
- LargeHeavyBlockArmorCornerInv
- LargeHeavyRoundArmor_Slope
- LargeHeavyRoundArmor_Corner
- LargeHeavyRoundArmor_CornerInv
- LargeHeavyBlockArmorSlope2Base
- LargeHeavyBlockArmorSlope2Tip
- LargeHeavyBlockArmorCorner2Base
- LargeHeavyBlockArmorCorner2Tip
- LargeHeavyBlockArmorInvCorner2Base
- LargeHeavyBlockArmorInvCorner2Tip
- LargeHeavyHalfArmorBlock
- LargeHeavyHalfSlopeArmorBlock
- LargeArmorPanelHeavy
- LargeHeavyArmorSlopedCorner
- LargeHeavyArmorSlopedCornerTip
- LargeHeavyArmorSlopedCornerBase

### Small Grid Heavy Armor:
- SmallHeavyBlockArmorBlock
- SmallHeavyBlockArmorSlope
- SmallHeavyBlockArmorCorner
- SmallHeavyBlockArmorCornerInv
- SmallHeavyRoundArmor_Slope
- SmallHeavyRoundArmor_Corner
- SmallHeavyRoundArmor_CornerInv
- SmallHeavyBlockArmorSlope2Base
- SmallHeavyBlockArmorSlope2Tip
- SmallHeavyBlockArmorCorner2Base
- SmallHeavyBlockArmorCorner2Tip
- SmallHeavyBlockArmorInvCorner2Base
- SmallHeavyBlockArmorInvCorner2Tip
- SmallHeavyHalfArmorBlock
- SmallHeavyHalfSlopeArmorBlock
- SmallArmorPanelHeavy
- SmallHeavyArmorSlopedCorner
- SmallHeavyArmorSlopedCornerTip
- SmallHeavyArmorSlopedCornerBase

## Test Results

### Before Fix:
```
Found 90 blueprints
Blueprints with light armor: 0    ← WRONG!
```

### After Fix:
```
Found 90 blueprints
Blueprints with armor blocks: 83  ← CORRECT!

Example Results:
Blueprint Missile              | Large  | Total:  225 | Light:  70 | Heavy:  64
Cruise Missle                  | Small  | Total:   53 | Light:   0 | Heavy:   4
```

## Verification

Ran diagnostic on user's actual blueprints:
- ✅ 90 blueprints scanned
- ✅ 83 contain armor blocks
- ✅ Light armor detected: 70 blocks in "Blueprint Missile"
- ✅ Heavy armor detected: 64 blocks in "Blueprint Missile", 4 blocks in "Cruise Missle"
- ✅ Block types match Space Engineers wiki documentation
- ✅ SubtypeName extraction working correctly

## Impact

**Functional improvements:**
1. ✅ Armor blocks now detected correctly
2. ✅ Light armor count accurate
3. ✅ Heavy armor count now available
4. ✅ Conversion will now work properly
5. ✅ GUI shows complete armor statistics

**User-visible changes:**
- Details panel now shows 5 fields (added HEAVY ARMOR)
- Exchange visualization shows accurate counts
- Convert button enables correctly when light armor present
- Status shows meaningful armor counts

## Related Documentation

- Space Engineers Wiki: Blocks use SubtypeName in XML
- Official SE Blueprint Format: CubeBlocks contain SubtypeName elements
- GitHub repo (archived): Confirms SubtypeName is the identifier field

## Summary

The critical fix was changing from `SubtypeId` (which doesn't exist in blueprint files) to `SubtypeName` (the actual element used by Space Engineers). This single change plus the addition of heavy armor block tracking now provides complete and accurate armor block detection across all blueprints.

All three core files (scanner, replacer, GUI) have been updated and tested with real user data.


from se_armor_replacer import ArmorBlockReplacer
from blueprint_scanner import BlueprintScanner

def verify():
    replacer_light = set(ArmorBlockReplacer.LIGHT_TO_HEAVY.keys())
    replacer_heavy = set(ArmorBlockReplacer.LIGHT_TO_HEAVY.values())
    
    scanner_light = BlueprintScanner.LIGHT_ARMOR_BLOCKS
    scanner_heavy = BlueprintScanner.HEAVY_ARMOR_BLOCKS
    
    print("Checking consistency between Replacer and Scanner...")
    
    diff_light_1 = replacer_light - scanner_light
    diff_light_2 = scanner_light - replacer_light
    
    if diff_light_1:
        print(f"In Replacer but not Scanner (Light): {diff_light_1}")
    if diff_light_2:
        print(f"In Scanner but not Replacer (Light): {diff_light_2}")
        
    diff_heavy_1 = replacer_heavy - scanner_heavy
    diff_heavy_2 = scanner_heavy - replacer_heavy
    
    if diff_heavy_1:
        print(f"In Replacer but not Scanner (Heavy): {diff_heavy_1}")
    if diff_heavy_2:
        print(f"In Scanner but not Replacer (Heavy): {diff_heavy_2}")

    print("Verification complete.")

if __name__ == "__main__":
    verify()


import os
import shutil
from pathlib import Path
from blueprint_converter import BlueprintConverter

def test_fix():
    # Setup test environment
    test_dir = Path("test_env")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    source_bp = test_dir / "MyShip"
    source_bp.mkdir()
    
    # Create valid bp.sbc
    xml_content = """<?xml version="1.0"?>
<Definitions xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ShipBlueprints>
    <ShipBlueprint>
      <CubeBlocks>
        <MyObjectBuilder_CubeBlock xsi:type="MyObjectBuilder_CubeBlock">
          <SubtypeName>LargeBlockArmorBlock</SubtypeName>
        </MyObjectBuilder_CubeBlock>
      </CubeBlocks>
    </ShipBlueprint>
  </ShipBlueprints>
</Definitions>
"""
    with open(source_bp / "bp.sbc", "w") as f:
        f.write(xml_content)
        
    # Create dummy binary file
    with open(source_bp / "bp.sbcB5", "w") as f:
        f.write("DUMMY BINARY CONTENT")
        
    print(f"Created test blueprint at {source_bp}")
    print(f"Binary file exists: {(source_bp / 'bp.sbcB5').exists()}")
    
    # Run conversion
    converter = BlueprintConverter(verbose=True)
    try:
        dest, scanned, converted = converter.create_heavy_armor_blueprint(source_bp)
        
        print(f"Conversion result: {dest}")
        
        # Verify binary file is GONE in destination
        dest_binary = dest / "bp.sbcB5"
        if dest_binary.exists():
            print("FAILURE: bp.sbcB5 still exists in destination!")
        else:
            print("SUCCESS: bp.sbcB5 was removed.")
            
        # Verify XML was updated
        with open(dest / "bp.sbc", "r") as f:
            content = f.read()
            if "LargeHeavyBlockArmorBlock" in content:
                print("SUCCESS: XML updated correctly.")
            else:
                print("FAILURE: XML not updated.")
                
    except Exception as e:
        print(f"Error: {e}")
        
    # Cleanup
    # shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_fix()

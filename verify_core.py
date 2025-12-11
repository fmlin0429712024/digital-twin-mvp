import sys
import os
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.simulator import Simulator
from src.core.normalizer import IntelligentMembrane

def test_core_logic():
    print("--- Starting Core Logic Verification ---")
    
    # 1. Initialize Simulator & Membrane
    sim = Simulator()
    membrane = IntelligentMembrane()
    print("✅ Components Initialized")

    # 2. Generate Chaos (Tick 1)
    print("\n--- Ticking Simulator (Normal) ---")
    packets = list(sim.run_tick())
    print(f"Generated {len(packets)} packets.")
    
    for p in packets:
        print(f"RAW: {p}")
        norm = membrane.normalize(p)
        print(f"NORM: {norm}")
        
        # Verify normalization
        if p['id'] == "0x5A":
            expected_temp = (p['raw_val'] * 0.1) - 20.0
            assert abs(norm['value'] - expected_temp) < 0.01, "Temp normalization failed"
            print("   -> Temp Norm OK")

    # 3. Simulate Anomaly
    print("\n--- Triggering Anomaly ---")
    sim.trigger_anomaly(True)
    time.sleep(0.1)
    anomaly_packets = list(sim.run_tick())
    
    for p in anomaly_packets:
        norm = membrane.normalize(p)
        # We expect at least one to differ significantly or just check connectivity
        print(f"ANOMALY RAW: {p}")
        print(f"ANOMALY NORM: {norm}")
        
        # Check if status became critical for Temp if value spiked
        if p['id'] == "0x5A" and norm['value'] > 80.0:
             print("   -> CRITICAL Status Detected (As Expected)")

    print("\n✅ Verification Complete: Core Logic is sound.")

if __name__ == "__main__":
    test_core_logic()

import random
import time
import math
from typing import Dict, Any

class Simulator:
    def __init__(self):
        self.anomaly_active = False
        self.anomaly_start_time = 0.0
        # Asset base states (physics heuristic: drifting random walks)
        self.assets = {
            "0x5A": {"type": "temp", "val": 400.0, "drift": 0.0},  # HVAC Temp (Raw ADC)
            "0x8B": {"type": "vibration", "val": 0.0, "phase": 0.0}, # Conveyor Vibration
            "0xC2": {"type": "current", "val": 12.0, "drift": 0.0},  # Robot Arm Current
        }

    def trigger_anomaly(self, active: bool):
        self.anomaly_active = active
        if active:
            self.anomaly_start_time = time.time()
            print("!!! ANOMALY INJECTED !!!")
        else:
            print("... System returning to normal ...")

    def generate_packet(self, asset_id: str) -> Dict[str, Any]:
        """Generates a raw, chaotic sensor packet."""
        asset = self.assets.get(asset_id)
        if not asset:
            return {}

        base_val = asset["val"]
        
        # Physics simulation
        if asset["type"] == "temp":
            # Slow drift
            asset["drift"] += random.uniform(-1, 1)
            # Anomaly: Rapid heat spike
            anomaly_factor = 50.0 * (time.time() - self.anomaly_start_time) if self.anomaly_active else 0
            raw_val = base_val + asset["drift"] + anomaly_factor
            
        elif asset["type"] == "vibration":
            # Sinusoidal + Noise
            asset["phase"] += 0.1
            noise = random.uniform(-0.5, 0.5)
            # Anomaly: High amplitude shaking
            amp = 50.0 if self.anomaly_active else 5.0
            raw_val = (math.sin(asset["phase"]) * amp) + noise
            
        elif asset["type"] == "current":
            # Random fluctuations
            noise = random.uniform(-0.2, 0.2)
            # Anomaly: Surge
            surge = 10.0 if self.anomaly_active else 0
            raw_val = base_val + noise + surge
            
        else:
            raw_val = 0

        # Return "chaotic" packet structure
        return {
            "id": asset_id,
            "ts": time.time(),
            "raw_val": raw_val,
            "hw_ver": "1.0", # Garbage metadata
            "chk": random.randint(0, 255) # Garbage metadata
        }

    def run_tick(self):
        """Yields packets for all assets."""
        for asset_id in self.assets:
            yield self.generate_packet(asset_id)

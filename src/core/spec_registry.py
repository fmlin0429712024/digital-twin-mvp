from typing import Dict, Any

class SpecRegistry:
    def __init__(self):
        # The "Spec Kit" - Metadata Registry
        # 0x5A -> HVAC Temp Sensor logic
        # 0x8B -> Conveyor Motor Vibration logic
        # 0xC2 -> Robot Arm Health logic
        self.registry = {
            "0x5A": {
                "name": "HVAC Unit #1 - Exhaust Temp",
                "type": "temperature",
                "unit": "°C",
                "normalization_factor": 0.1, # Raw 400 -> 40.0 C
                "offset": -20.0, # Calibration
                "safe_range": [15.0, 80.0],
                "ui_component": "gauge",
                "icon": "🌡️"
            },
            "0x8B": {
                "name": "Main Conveyor Belt - Vibration",
                "type": "vibration",
                "unit": "mm/s",
                "normalization_factor": 1.0, 
                "offset": 0.0,
                "safe_range": [-10.0, 10.0],
                "ui_component": "chart",
                "icon": "📉"
            },
            "0xC2": {
                "name": "Robotic Arm - Servo Current",
                "type": "electrical",
                "unit": "Amps",
                "normalization_factor": 1.0,
                "offset": 0.0,
                "safe_range": [10.0, 20.0],
                "ui_component": "metric_card",
                "icon": "⚡"
            }
        }

    def get_spec(self, sensor_id: str) -> Dict[str, Any]:
        """Finds the spec for a given sensor ID."""
        return self.registry.get(sensor_id, {
            "name": f"Unknown Asset ({sensor_id})",
            "type": "unknown",
            "unit": "raw",
            "normalization_factor": 1.0,
            "offset": 0.0,
            "safe_range": [0, 999999],
            "ui_component": "text"
        })

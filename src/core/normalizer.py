from typing import Dict, Any
from src.core.spec_registry import SpecRegistry

class IntelligentMembrane:
    def __init__(self):
        self.specs = SpecRegistry()

    def normalize(self, raw_packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms Chaos (Raw Packet) -> Order (Normalized Data)
        using the Spec Registry.
        """
        sensor_id = raw_packet.get("id")
        if not sensor_id:
            return None

        spec = self.specs.get_spec(sensor_id)
        
        # Apply normalization spec
        raw_val = raw_packet.get("raw_val", 0)
        norm_val = (raw_val * spec["normalization_factor"]) + spec["offset"]
        
        # Check Health
        is_critical = False
        if norm_val < spec["safe_range"][0] or norm_val > spec["safe_range"][1]:
            is_critical = True

        return {
            "id": sensor_id,
            "timestamp": raw_packet.get("ts"),
            "display_name": spec["name"],
            "value": round(norm_val, 2),
            "unit": spec["unit"],
            "status": "CRITICAL" if is_critical else "HEALTHY",
            "spec_type": spec["type"],
            "ui_config": {
                "component": spec["ui_component"],
                "icon": spec["icon"],
                "min": spec["safe_range"][0],
                "max": spec["safe_range"][1]
            }
        }

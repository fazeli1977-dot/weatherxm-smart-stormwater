from enum import Enum
from typing import Literal, Optional, List
from pydantic import BaseModel, Field

class FloodRiskLevel(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class WeatherObservation(BaseModel):
    station_id: str
    name: str
    data_source: Literal["live_api", "simulated"] = "simulated"
    precipitation_rate_mm_h: float = Field(ge=0.0, description="Precipitation rate in mm/hour")
    precipitation_accumulated_24h_mm: float = Field(default=0.0, ge=0.0)
    temperature_c: float
    wind_speed_m_s: float = Field(ge=0.0)
    battery_percentage: Optional[int] = Field(default=100, ge=0, le=100)

class CatchmentParameters(BaseModel):
    catchment_id: str
    area_hectares: float = Field(gt=0, description="Catchment area in hectares")
    runoff_coefficient: float = Field(ge=0.05, le=1.0, description="Rational runoff coefficient (C)")
    stormwater_network_capacity_m3_s: float = Field(gt=0, description="Conduit/network maximum flow capacity")

class RunoffAssessment(BaseModel):
    catchment_id: str
    rainfall_intensity_mm_h: float
    peak_discharge_m3_s: float
    network_capacity_m3_s: float
    capacity_saturation_pct: float
    risk_level: FloodRiskLevel
    recommended_action: str

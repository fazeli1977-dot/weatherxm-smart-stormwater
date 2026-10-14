from weatherxm_smart_stormwater.models import CatchmentParameters, RunoffAssessment, FloodRiskLevel

class HydrologyEngine:
    """
    Hydrologic evaluation engine using Rational Method:
    Q = 0.00278 * C * I * A
    Where:
        Q = Peak runoff (m^3/s)
        C = Runoff coefficient (dimensionless, 0.05 - 1.0)
        I = Rainfall intensity (mm/h)
        A = Drainage area (hectares)
    """

    @staticmethod
    def calculate_peak_discharge(c: float, intensity_mm_h: float, area_ha: float) -> float:
        discharge = 0.00278 * c * intensity_mm_h * area_ha
        return round(discharge, 4)

    @classmethod
    def evaluate_catchment(
        cls,
        catchment: CatchmentParameters,
        precipitation_rate_mm_h: float
    ) -> RunoffAssessment:
        peak_q = cls.calculate_peak_discharge(
            c=catchment.runoff_coefficient,
            intensity_mm_h=precipitation_rate_mm_h,
            area_ha=catchment.area_hectares
        )

        saturation = (peak_q / catchment.stormwater_network_capacity_m3_s) * 100.0

        if saturation >= 100.0:
            level = FloodRiskLevel.CRITICAL
            action = "EMERGENCY: Network surcharge imminent. Deploy detention gates & municipal flood alerts."
        elif saturation >= 75.0:
            level = FloodRiskLevel.WARNING
            action = "HIGH: Stormwater conduits near capacity. Stage emergency pumping units."
        elif saturation >= 50.0:
            level = FloodRiskLevel.WATCH
            action = "MODERATE: Accelerated runoff detected. Inspect retention inlet screens."
        else:
            level = FloodRiskLevel.NORMAL
            action = "OPTIMAL: Urban drainage operating within standard conveyance limits."

        return RunoffAssessment(
            catchment_id=catchment.catchment_id,
            rainfall_intensity_mm_h=precipitation_rate_mm_h,
            peak_discharge_m3_s=peak_q,
            network_capacity_m3_s=catchment.stormwater_network_capacity_m3_s,
            capacity_saturation_pct=round(saturation, 2),
            risk_level=level,
            recommended_action=action
        )

import asyncio
import os
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from weatherxm_smart_stormwater.models import CatchmentParameters, FloodRiskLevel
from weatherxm_smart_stormwater.hydrology import HydrologyEngine
from weatherxm_smart_stormwater.client import WeatherXMClient

app = typer.Typer(help="WeatherXM Urban Stormwater & Flood Resilience CLI")
console = Console()

@app.command()
def evaluate(
    station_id: str = typer.Option("wxm-berlin-01", help="WeatherXM Station / Cell ID"),
    area: float = typer.Option(45.0, help="Catchment Area in hectares"),
    runoff_c: float = typer.Option(0.75, help="Catchment Runoff Coefficient (0.1 to 0.95)"),
    capacity: float = typer.Option(3.5, help="Stormwater conduit design capacity in m3/s")
):
    """
    Evaluate storm runoff impact on urban drainage conduits using WeatherXM DePIN data.
    """
    console.print(Panel.fit("[bold cyan]WeatherXM Smart Stormwater Infrastructure[/bold cyan]\n[dim]DePIN-Driven Hydrologic Risk Analysis[/dim]", border_style="cyan"))

    client = WeatherXMClient(api_key=os.getenv("WEATHERXM_API_KEY"))
    obs = asyncio.run(client.get_station_observation(station_id=station_id))

    catchment = CatchmentParameters(
        catchment_id=f"Catchment-{station_id}",
        area_hectares=area,
        runoff_coefficient=runoff_c,
        stormwater_network_capacity_m3_s=capacity
    )

    assessment = HydrologyEngine.evaluate_catchment(catchment, obs.precipitation_rate_mm_h)

    # Station Data Table
    table_station = Table(title="WeatherXM Station Observation", header_style="bold magenta")
    table_station.add_column("Property", style="dim")
    table_station.add_column("Value", style="bold")
    table_station.add_row("Station Name / ID", f"{obs.name} ({obs.station_id})")
    table_station.add_row(
        "Data Source",
        "Live API" if obs.data_source == "live_api" else "Simulated demo",
    )
    table_station.add_row("Precipitation Rate", f"{obs.precipitation_rate_mm_h:.1f} mm/h")
    table_station.add_row("24h Accumulation", f"{obs.precipitation_accumulated_24h_mm:.1f} mm")
    table_station.add_row("Temperature / Wind", f"{obs.temperature_c:.1f} °C | {obs.wind_speed_m_s:.1f} m/s")
    table_station.add_row("Hardware Health", f"{obs.battery_percentage}% battery")
    console.print(table_station)

    # Hydrology Results Table
    risk_color = {
        FloodRiskLevel.NORMAL: "green",
        FloodRiskLevel.WATCH: "yellow",
        FloodRiskLevel.WARNING: "dark_orange",
        FloodRiskLevel.CRITICAL: "bold red"
    }[assessment.risk_level]

    table_hydro = Table(title="Hydraulic Network Assessment", header_style="bold blue")
    table_hydro.add_column("Metric", style="dim")
    table_hydro.add_column("Value", style="bold")
    table_hydro.add_row("Drainage Area (A)", f"{area} ha")
    table_hydro.add_row("Runoff Coefficient (C)", f"{runoff_c}")
    table_hydro.add_row("Peak Discharge (Q)", f"{assessment.peak_discharge_m3_s} m³/s")
    table_hydro.add_row("Network Capacity", f"{assessment.network_capacity_m3_s} m³/s")
    table_hydro.add_row("Saturation Level", f"{assessment.capacity_saturation_pct:.1f}%")
    table_hydro.add_row("Risk Level", f"[{risk_color}]{assessment.risk_level.value}[/{risk_color}]")
    console.print(table_hydro)

    console.print(Panel(f"[{risk_color}]{assessment.recommended_action}[/{risk_color}]", title="Actionable Hydraulic Advisory", border_style=risk_color))

def main():
    app()


if __name__ == "__main__":
    main()

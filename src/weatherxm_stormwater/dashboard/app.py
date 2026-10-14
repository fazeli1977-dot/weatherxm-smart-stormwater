import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="WeatherXM Stormwater Live Dashboard",
    page_icon="🌧️",
    layout="wide",
)

st.title("🌧️ WeatherXM Smart Stormwater Infrastructure")
st.markdown("**Real-time DePIN-powered Hydrologic Risk & Drainage Monitoring**")

# Sidebar Controls
st.sidebar.header("Station Configuration")
station_id = st.sidebar.text_input("Station ID", value="wxm-station-01")
area_ha = st.sidebar.slider("Catchment Area (ha)", min_value=1.0, max_value=200.0, value=45.0, step=1.0)
runoff_c = st.sidebar.slider("Runoff Coefficient (C)", min_value=0.1, max_value=0.95, value=0.75, step=0.05)
capacity = st.sidebar.slider("Drainage Capacity (m³/s)", min_value=0.5, max_value=10.0, value=3.5, step=0.1)

# Metrics Calculation
simulated_intensity = 34.5  # mm/h
discharge = (runoff_c * simulated_intensity * area_ha) / 360.0
saturation_pct = (discharge / capacity) * 100.0

if saturation_pct >= 100:
    risk_level = "CRITICAL / OVERFLOW"
elif saturation_pct >= 80:
    risk_level = "WARNING"
else:
    risk_level = "NORMAL"

# Top Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Station Status", "ONLINE", "DePIN Synced")
col2.metric("Precipitation Rate", f"{simulated_intensity:.1f} mm/h", "Peak 15m")
col3.metric("Computed Discharge (Q)", f"{discharge:.2f} m³/s", f"{saturation_pct:.1f}% Capacity")
col4.metric("Risk Advisory", risk_level)

st.markdown("---")

# Main Charts
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("📊 Hydraulic Capacity Saturation")
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=saturation_pct,
        title={'text': "Saturation Level (%)"},
        gauge={
            'axis': {'range': [0, 150]},
            'bar': {'color': "#1e3d59"},
            'steps': [
                {'range': [0, 80], 'color': "#17b978"},
                {'range': [80, 100], 'color': "#ffb03b"},
                {'range': [100, 150], 'color': "#e84a5f"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))
    gauge_fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(gauge_fig, use_container_width=True)

with right_col:
    st.subheader("📈 Hydrograph Simulation (24h Window)")
    time_points = [f"{h:02d}:00" for h in range(24)]
    base_flow = np.maximum(0, np.sin(np.linspace(0, np.pi, 24)) * discharge * 1.05 + np.random.normal(0, 0.05, 24))
    
    hydro_fig = go.Figure()
    hydro_fig.add_trace(go.Scatter(x=time_points, y=base_flow, mode='lines+markers', name='Discharge (Q)', line=dict(color='#0881a3', width=3)))
    hydro_fig.add_hline(y=capacity, line_dash="dash", line_color="red", annotation_text="Max Capacity", annotation_position="top left")
    hydro_fig.update_layout(
        xaxis_title="Timeline",
        yaxis_title="Discharge Rate (m³/s)",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(hydro_fig, use_container_width=True)

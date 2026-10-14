# WeatherXM Smart Stormwater Infrastructure 🌧️⚡

[![CI](https://github.com/naomi197/weatherxm-smart-stormwater/actions/workflows/ci.yml/badge.svg)](https://github.com/naomi197/weatherxm-smart-stormwater/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![DePIN](https://img.shields.io/badge/DePIN-WeatherXM-orange.svg)](https://weatherxm.com/)

**WeatherXM Smart Stormwater** is a DePIN-integrated civil-infrastructure tool designed to evaluate real-time urban flash flood risk and conduit conveyance capacity using hyper-local weather station observations.

By integrating hyper-local DePIN precipitation data directly into hydraulic engineering equations, municipal authorities and smart city networks can deploy proactive detention strategies before stormwater infrastructure experiences surcharge.

---

## 🏛️ Engineering Foundation: The Rational Method

The core engine models peak urban stormwater runoff using the **Rational Equation**:

$$Q = 0.00278 \times C \times I \times A$$

Where:
- **$Q$**: Peak runoff discharge rate ($\text{m}^3/\text{s}$)
- **$C$**: Dimensionless runoff coefficient based on land use ($0.05 \le C \le 1.0$)
- **$I$**: Rainfall intensity measured real-time by WeatherXM stations ($\text{mm}/\text{h}$)
- **$A$**: Contributing urban drainage catchment area ($\text{hectares}$)

### Dynamic Saturation & Advisory Tiers

$$\text{Saturation (\%)} = \left(\frac{Q}{Q_{\text{network design capacity}}}\right) \times 100$$

- **NORMAL (< 50%)**: Conduits operating within nominal capacity.
- **WATCH (50% – 74%)**: Accelerated runoff; inspection advisories triggered.
- **WARNING (75% – 99%)**: Elevated surcharge risk; emergency pumping staging recommended.
- **CRITICAL ($\ge$ 100%)**: Hydraulic capacity exceeded; detention gate actions deployed.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)

### Installation
```powershell
git clone https://github.com/naomi197/weatherxm-smart-stormwater.git
cd weatherxm-smart-stormwater
uv sync

### CLI Usage
Run evaluation with hyper-local parameters:
powershell
uv run wxm-stormwater evaluate --station-id "wxm-station-01" --area 45.0 --runoff-c 0.75 --capacity 3.5

### Running Tests & Coverage
powershell
uv run pytest --cov=weatherxm_smart_stormwater tests/

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

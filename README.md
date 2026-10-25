# WeatherXM Smart Stormwater Infrastructure 🌧️⚡
[![CI](https://github.com/fazeli1977-dot/weatherxm-smart-stormwater/actions/workflows/ci.yml/badge.svg)](https://github.com/fazeli1977-dot/weatherxm-smart-stormwater/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/fazeli1977-dot/weatherxm-smart-stormwater?color=blue&logo=github)](https://github.com/fazeli1977-dot/weatherxm-smart-stormwater/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![DePIN: WeatherXM](https://img.shields.io/badge/DePIN-WeatherXM-00D26A.svg)](https://weatherxm.com)
[![Coverage: 93%](https://img.shields.io/badge/Coverage-93%25-brightgreen.svg)]()

**WeatherXM Smart Stormwater** is an enterprise-grade, DePIN-integrated civil infrastructure platform bridging hyper-local physical weather station networks with municipal hydraulic drainage modeling to predict conduit surcharge and mitigate urban flash floods.

## 🖥️ Supervisory Dashboard Preview

![WeatherXM Smart Stormwater Dashboard](docs/screenshots/dashboard.png)

> 🚀 **Local Dashboard Entrypoint:** `http://localhost:8501`

---

## 🚀 Quickstart & Installation


```bash
git clone https://github.com/fazeli1977-dot/weatherxm-smart-stormwater.git
cd weatherxm-smart-stormwater
uv sync --all-groups
uv run wxm-stormwater-dashboard

```

Set `WEATHERXM_API_KEY` to use authenticated WeatherXM data with the CLI; without
it, the CLI uses its built-in demo observation. For example, in PowerShell:

```powershell
$env:WEATHERXM_API_KEY = "your-api-key"
uv run wxm-stormwater evaluate
```

The dashboard currently uses simulated weather and hydrograph data.

---

## 👥 Authors & Maintainers

- **Alireza Sani** ([@fazeli1977-dot](https://github.com/fazeli1977-dot)) — Lead Architect & Infrastructure Engineer

## 📄 License

Distributed under the [MIT License](LICENSE).

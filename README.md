# sysmon

A lightweight terminal system monitor written in Python.

Shows live CPU, RAM, disk and battery usage plus the top processes,
and logs readings to a CSV file for later analysis.

## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Usage

    python sysmon.py

Press Ctrl+C to stop. Readings are saved to sysmon_log.csv every 5 seconds.

## Roadmap

- [x] v1: live display
- [x] v2: CSV logging
- [ ] v3: threshold alerts and command-line options
- [ ] v4: run as a systemd service

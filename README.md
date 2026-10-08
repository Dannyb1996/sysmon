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
- [x] v3: threshold alerts and command-line options
- [x] v4: run as a systemd service

## Run as a background service (systemd user service)

    mkdir -p ~/.config/systemd/user ~/.local/share/sysmon
    cp sysmon.service ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable --now sysmon.service

The service uses the project's virtualenv and expects the repo at ~/projects/sysmon.
It logs to ~/.local/share/sysmon/sysmon_log.csv every 30 seconds and writes
to the journal only when an alert changes state:

    journalctl --user -u sysmon.service

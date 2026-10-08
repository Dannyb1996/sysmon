import argparse
import csv
import os
import time
from datetime import datetime

import psutil

RED = "\033[91m"
RESET = "\033[0m"


def parse_args():
    p = argparse.ArgumentParser(description="Lightweight terminal system monitor.")
    p.add_argument("--interval", type=float, default=1.0,
                   help="screen refresh in seconds (default 1)")
    p.add_argument("--log-every", type=float, default=5.0,
                   help="seconds between log rows (default 5)")
    p.add_argument("--log-file", default="sysmon_log.csv",
                   help="CSV log path (default sysmon_log.csv)")
    p.add_argument("--no-log", action="store_true", help="disable CSV logging")
    p.add_argument("--cpu-alert", type=float, default=90,
                   help="CPU alert threshold in %% (default 90)")
    p.add_argument("--ram-alert", type=float, default=90,
                   help="RAM alert threshold in %% (default 90)")
    p.add_argument("--disk-alert", type=float, default=90,
                   help="disk alert threshold in %% (default 90)")
    return p.parse_args()


def bar(percent, threshold, width=20):
    filled = int(width * percent / 100)
    text = "█" * filled + "░" * (width - filled)
    return f"{RED}{text}{RESET}" if percent >= threshold else text


def top_processes(n=5):
    procs = [p.info for p in psutil.process_iter(["name", "cpu_percent", "memory_percent"])]
    procs.sort(key=lambda p: p["cpu_percent"] or 0, reverse=True)
    return procs[:n]


def log_row(path, cpu, mem, disk, batt, alerts):
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "cpu_percent", "ram_percent",
                             "disk_percent", "battery_percent", "alerts"])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            cpu, mem.percent, disk.percent,
            round(batt.percent, 1) if batt else "",
            ";".join(alerts),
        ])


def main():
    args = parse_args()
    for p in psutil.process_iter():          # prime per-process CPU counters
        p.cpu_percent(None)
    last_log = 0.0
    try:
        while True:
            cpu = psutil.cpu_percent(interval=args.interval)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            batt = psutil.sensors_battery()

            alerts = []
            if cpu >= args.cpu_alert:
                alerts.append("CPU")
            if mem.percent >= args.ram_alert:
                alerts.append("RAM")
            if disk.percent >= args.disk_alert:
                alerts.append("DISK")

            if not args.no_log and time.time() - last_log >= args.log_every - args.interval / 2:
                log_row(args.log_file, cpu, mem, disk, batt, alerts)
                last_log = time.time()

            print("\033[H\033[J", end="")    # clear screen
            print("=== SYSMON v3 ===")
            print(f"CPU  {bar(cpu, args.cpu_alert)} {cpu:5.1f}%")
            print(f"RAM  {bar(mem.percent, args.ram_alert)} {mem.percent:5.1f}%  ({mem.used/1e9:.1f}/{mem.total/1e9:.1f} GB)")
            print(f"DISK {bar(disk.percent, args.disk_alert)} {disk.percent:5.1f}%  ({disk.used/1e9:.0f}/{disk.total/1e9:.0f} GB)")
            if batt:
                state = "charging" if batt.power_plugged else "on battery"
                print(f"BATT {bar(batt.percent, 101)} {batt.percent:5.1f}%  ({state})")
            if alerts:
                print(f"\n{RED}ALERT: {', '.join(alerts)} above threshold{RESET}")
            print("\nTop processes (CPU%):")
            for p in top_processes():
                print(f"  {(p['name'] or '?')[:25]:25} {(p['cpu_percent'] or 0):5.1f}%  {(p['memory_percent'] or 0):4.1f}% RAM")
            footer = "logging off" if args.no_log else f"logging to {args.log_file} every {args.log_every:g}s"
            print(f"\n{footer}  |  Ctrl+C to stop")
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()

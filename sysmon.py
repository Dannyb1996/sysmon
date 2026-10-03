import time
import psutil

def bar(percent, width=20):
    filled = int(width * percent / 100)
    return "█" * filled + "░" * (width - filled)

def top_processes(n=5):
    procs = [p.info for p in psutil.process_iter(["name", "cpu_percent", "memory_percent"])]
    procs.sort(key=lambda p: p["cpu_percent"] or 0, reverse=True)
    return procs[:n]

def main():
    for p in psutil.process_iter():          # prime per-process CPU counters
        p.cpu_percent(None)
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            batt = psutil.sensors_battery()

            print("\033[H\033[J", end="")    # clear screen
            print("=== SYSMON ===")
            print(f"CPU  {bar(cpu)} {cpu:5.1f}%")
            print(f"RAM  {bar(mem.percent)} {mem.percent:5.1f}%  ({mem.used/1e9:.1f}/{mem.total/1e9:.1f} GB)")
            print(f"DISK {bar(disk.percent)} {disk.percent:5.1f}%  ({disk.used/1e9:.0f}/{disk.total/1e9:.0f} GB)")
            if batt:
                state = "charging" if batt.power_plugged else "on battery"
                print(f"BATT {bar(batt.percent)} {batt.percent:5.1f}%  ({state})")
            print("\nTop processes (CPU%):")
            for p in top_processes():
                print(f"  {(p['name'] or '?')[:25]:25} {(p['cpu_percent'] or 0):5.1f}%  {(p['memory_percent'] or 0):4.1f}% RAM")
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()

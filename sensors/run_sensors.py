import subprocess, sys

sensors = [
    ("temperature_sensor.py", "2"),
    ("humidity_sensor.py",    "2"),
    ("co2_sensor.py",         "3"),
    ("motion_sensor.py",      "1"),
    ("gas_sensor.py",         "3"),
]

processes = []
for script, interval in sensors:
    p = subprocess.Popen(
        [sys.executable, script, "--interval", interval],
        cwd="."
    )
    processes.append(p)

print(f"Launched {len(processes)} sensors. Ctrl+C to stop all.")
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    for p in processes:
        p.terminate()
    print("All sensors stopped.")
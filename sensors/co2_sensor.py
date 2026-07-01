from base_sensor import BaseSensor
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Seconds between readings")
    args = parser.parse_args()
    BaseSensor("CO2", "co", "ppm").run(args.interval)
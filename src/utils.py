from datetime import timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def to_readable_time(minutes):
    delta = timedelta(minutes=minutes)
    return str(delta).split('.')[0]

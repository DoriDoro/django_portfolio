import json
import logging

from pathlib import Path

logger = logging.getLogger(__name__)


def _read_json_file(json_path) -> any:
    path = Path(json_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        logger.exception(f"File '{path}' not found.")
        raise FileNotFoundError(f"File '{path}' not found.") from exc
    except json.JSONDecodeError as exc:
        logger.exception(f"Invalid JSON in file: '{path}'.")
        raise ValueError(f"Invalid JSON in file: '{path}'.") from exc
    except OSError as exc:
        logger.exception(f"Could not read file: '{path}'.")
        raise OSError(f"Could not read file: '{path}'.") from exc


def read_json_file(*, json_path: str) -> any:
    if not json_path:
        raise ValueError("'json_path' is required.")

    return _read_json_file(json_path)

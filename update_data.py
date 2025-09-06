#!/usr/bin/env python3
"""Thin wrapper to the refactored updater.

Keeps CI and existing scripts stable while delegating to
`refactored_update_data.py` as the single source of truth.
"""

from refactored_update_data import main as _main


if __name__ == "__main__":
    _main()


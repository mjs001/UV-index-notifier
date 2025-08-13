#!/usr/bin/env python3
"""
Run script for UV Index Notifier
Usage: python run.py [environment]
Environments: development, production, testing
"""

import os
import sys
from app import app


def main():
    # Get environment from command line argument or default to development
    env = sys.argv[1] if len(sys.argv) > 1 else "development"

    # Set environment variable
    os.environ["FLASK_ENV"] = env

    print(f"Starting UV Index Notifier in {env} mode...")

    # Import and run the app
    from app import app

    app.run()


if __name__ == "__main__":
    main()

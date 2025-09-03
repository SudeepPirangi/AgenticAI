#!/usr/bin/env python
import warnings

from datetime import datetime

from route_map.crew import RouteMap

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        "profession": "AI Engineer",
    }

    try:
        RouteMap().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

"""Representation of a knowledge unit."""
import json


class KnowledgeUnit:
    """Definition of a knowledge unit."""

    def __init__(self, **parameters):
        """Initialize the knowledge unit."""
        self.parameters = parameters

    def to_dict(self):
        """Knowledge unit to dictionary."""
        return self.parameters

    def __str__(self):
        """Knowledge unit to string."""
        raise json.dumps(self.parameters)

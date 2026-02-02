"""
SHawn-Brain: Digital Central Nervous System (D-CNS)
Level 1-4 neural architecture
"""

from .brain_core import brainstem
from .neocortex import neocortex_connector

__all__ = ['brainstem', 'neocortex_connector']

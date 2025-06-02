"""
Modul agents untuk implementasi agen-agen dalam simulasi
"""

from .base_agent import BaseAgent, HerbivoreAgent, CarnivoreAgent, ElkAgent, SpeciesType
from .config_helper import get_herbivore_config, get_carnivore_config, get_elk_config
"""
Helper untuk mengakses konfigurasi dengan fallback
Mengatasi masalah circular import dan missing config
"""

def get_herbivore_config():
    """
    Get herbivore configuration with automatic fallback
    """
    try:
        from data.config_fixed import HERBIVORE_CONFIG
        return HERBIVORE_CONFIG
    except ImportError:
        try:
            from data.config_fixed import HERBIVORE_CONFIG
            return HERBIVORE_CONFIG
        except ImportError:
            # Fallback default config
            return {
                'species_name': 'Kelinci',
                'initial_population': 50,
                'reproduction_rate': 0.003,
                'mortality_rate': 0.002,
                'consumption_rate': 15.0,
                'mobility': 1,
                'initial_energy': 100.0,
                'reproduction_threshold': 75.0,
                'metabolic_cost': 4.0,
                'min_temp': 5.0,
                'max_temp': 30.0,
                'min_humidity': 40.0,
                'max_humidity': 80.0,
                'max_age': 730,
                'foraging_efficiency': 0.85
            }

def get_carnivore_config():
    """
    Get carnivore configuration with automatic fallback
    """
    try:
        from data.config_fixed import CARNIVORE_CONFIG
        return CARNIVORE_CONFIG
    except ImportError:
        try:
            from data.config_fixed import CARNIVORE_CONFIG
            return CARNIVORE_CONFIG
        except ImportError:
            # Fallback default config
            return {
                'species_name': 'Serigala',
                'initial_population': 15,
                'reproduction_rate': 0.0012,
                'mortality_rate': 0.0006,
                'mobility': 3,
                'initial_energy': 120.0,
                'reproduction_threshold': 85.0,
                'metabolic_cost': 3.0,
                'min_temp': -30.0,
                'max_temp': 25.0,
                'min_humidity': 20.0,
                'max_humidity': 85.0,
                'max_age': 2190,
                'predation_rate': 0.15,
                'conversion_efficiency': 0.75,
                'hunt_range': 2,
                'energy_per_kill': 40.0,
                'hunting_cost': 4.0,
                'pack_hunting_bonus': 1.8,
                'starvation_tolerance': 15,
                'hunt_cooldown': 0.3,
            }
def get_elk_config():
    """
    Get elk configuration - berdasarkan data Yellowstone
    """
    try:
        from data.config_fixed import ELK_CONFIG
        return ELK_CONFIG
    except ImportError:
        try:
            from data.config_fixed import ELK_CONFIG
            return ELK_CONFIG
        except ImportError:
            # Fallback default config untuk elk
            return {
                'species_name': 'Elk',
                'initial_population': 20,      # Lebih banyak dari serigala tapi kurang dari kelinci
                'reproduction_rate': 0.002,    # Lebih rendah dari kelinci
                'mortality_rate': 0.001,       # Lebih rendah karena ukuran besar
                'consumption_rate': 25.0,      # Lebih banyak dari kelinci
                'mobility': 2,                 # Sama dengan kelinci
                'initial_energy': 150.0,       # Lebih besar dari kelinci
                'reproduction_threshold': 120.0, # Lebih tinggi
                'metabolic_cost': 6.0,         # Lebih tinggi dari kelinci
                'min_temp': -10.0,             # Lebih tahan dingin
                'max_temp': 25.0,
                'min_humidity': 30.0,
                'max_humidity': 85.0,
                'max_age': 1095,               # 3 tahun
                'foraging_efficiency': 0.9,    # Lebih efisien
                'herd_size': 5,                # Hidup berkelompok
                'defense_strength': 0.4        # Bisa melawan predator
            }
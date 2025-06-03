"""
Enhanced Helper untuk mengakses konfigurasi dengan CSV/JSON support dan fallback
Mengatasi masalah circular import dan missing config
Mendukung loading dari file eksternal (CSV/JSON) dengan fallback otomatis
"""

import json
import csv
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config_from_csv(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load konfigurasi dari file CSV
    Format: parameter,value,data_type
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        config = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                param_name = row['parameter'].strip()
                param_value = row['value'].strip()
                param_type = row.get('data_type', 'str').strip()
                
                # Type conversion
                try:
                    if param_type == 'float':
                        config[param_name] = float(param_value)
                    elif param_type == 'int':
                        config[param_name] = int(param_value)
                    elif param_type == 'bool':
                        config[param_name] = param_value.lower() in ['true', '1', 'yes', 'on']
                    else:
                        config[param_name] = str(param_value)
                except ValueError:
                    logger.warning(f"⚠️  Cannot convert {param_name}={param_value} to {param_type}, using string")
                    config[param_name] = str(param_value)
        
        # logger.info(f"✅ Loaded config from CSV: {file_path}")
        return config
        
    except Exception as e:
        logger.error(f"❌ Error loading CSV {file_path}: {e}")
        return None

def load_config_from_json(file_path: str, config_key: str = None) -> Optional[Dict[str, Any]]:
    """
    Load konfigurasi dari file JSON
    config_key: jika JSON berisi multiple configs, specify key (e.g., 'herbivore')
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if config_key:
            config = data.get(config_key)
            if config is None:
                logger.warning(f"⚠️  Key '{config_key}' not found in {file_path}")
                return None
        else:
            config = data
        
        # logger.info(f"✅ Loaded config from JSON: {file_path}")
        return config
        
    except Exception as e:
        logger.error(f"❌ Error loading JSON {file_path}: {e}")
        return None

def validate_config(config: Dict[str, Any], required_params: list) -> bool:
    """
    Validasi bahwa config memiliki parameter yang dibutuhkan
    """
    missing = [param for param in required_params if param not in config]
    if missing:
        logger.warning(f"⚠️  Missing required parameters: {missing}")
        return False
    return True

def get_herbivore_config(boost_reproduction: bool = False):
    """
    Get herbivore configuration with automatic fallback
    Prioritas: CSV -> JSON -> config_fixed.py -> hardcoded default
    """
    # Define required parameters
    required_params = [
        'species_name', 'initial_population', 'reproduction_rate', 'mortality_rate',
        'consumption_rate', 'mobility', 'initial_energy', 'reproduction_threshold',
        'metabolic_cost', 'min_temp', 'max_temp', 'min_humidity', 'max_humidity',
        'max_age', 'foraging_efficiency'
    ]
    
    # Coba load dari CSV
    csv_config = load_config_from_csv('data/herbivore_data.csv')
    if csv_config and validate_config(csv_config, required_params):
        config = csv_config
        # logger.info("📊 Using herbivore config from CSV")
    else:
        # Coba load dari JSON
        json_config = load_config_from_json('data/species_config.json', 'herbivore')
        if json_config and validate_config(json_config, required_params):
            config = json_config
            # logger.info("📄 Using herbivore config from JSON")
        else:
            # Fallback ke config_fixed.py
            try:
                from data.config_fixed import HERBIVORE_CONFIG
                config = HERBIVORE_CONFIG.copy()
                # logger.info("⚙️  Using herbivore config from config_fixed.py")
            except ImportError:
                # Ultimate fallback - hardcoded default
                config = {
                    'species_name': 'Kelinci',
                    'initial_population': 50,
                    'reproduction_rate': 0.3,
                    'mortality_rate': 0.002,
                    'consumption_rate': 15.0,
                    'mobility': 1,
                    'initial_energy': 100.0,
                    'reproduction_threshold': 50.0,
                    'metabolic_cost': 4.0,
                    'min_temp': 5.0,
                    'max_temp': 30.0,
                    'min_humidity': 40.0,
                    'max_humidity': 80.0,
                    'max_age': 730,
                    'foraging_efficiency': 0.85
                }
                logger.info("🔧 Using hardcoded herbivore default config")
    
    # Apply reproduction boost if requested
    if boost_reproduction:
        config = apply_reproduction_boost(config, 'herbivore')
        logger.info("🚀 Applied reproduction boost to herbivore config")
    
    return config

def get_carnivore_config(boost_reproduction: bool = False):
    """
    Get carnivore configuration with automatic fallback
    Prioritas: CSV -> JSON -> config_fixed.py -> hardcoded default
    """
    # Define required parameters
    required_params = [
        'species_name', 'initial_population', 'reproduction_rate', 'mortality_rate',
        'mobility', 'initial_energy', 'reproduction_threshold', 'metabolic_cost',
        'min_temp', 'max_temp', 'min_humidity', 'max_humidity', 'max_age',
        'predation_rate', 'conversion_efficiency', 'hunt_range', 'energy_per_kill',
        'hunting_cost'
    ]
    
    # Coba load dari CSV
    csv_config = load_config_from_csv('data/carnivore_data.csv')
    if csv_config and validate_config(csv_config, required_params):
        config = csv_config
        # logger.info("📊 Using carnivore config from CSV")
    else:
        # Coba load dari JSON
        json_config = load_config_from_json('data/species_config.json', 'carnivore')
        if json_config and validate_config(json_config, required_params):
            config = json_config
            # logger.info("📄 Using carnivore config from JSON")
        else:
            # Fallback ke config_fixed.py
            try:
                from data.config_fixed import CARNIVORE_CONFIG
                config = CARNIVORE_CONFIG.copy()
                # logger.info("⚙️  Using carnivore config from config_fixed.py")
            except ImportError:
                # Ultimate fallback - hardcoded default
                config = {
                    'species_name': 'Serigala',
                    'initial_population': 15,
                    'reproduction_rate': 0.12,
                    'mortality_rate': 0.0006,
                    'mobility': 3,
                    'initial_energy': 120.0,
                    'reproduction_threshold': 75.0,
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
                logger.info("🔧 Using hardcoded carnivore default config")
    
    # Apply reproduction boost if requested
    if boost_reproduction:
        config = apply_reproduction_boost(config, 'carnivore')
        logger.info("🚀 Applied reproduction boost to carnivore config")
    
    return config

def get_elk_config(boost_reproduction: bool = False):
    """
    Get elk configuration with automatic fallback
    Prioritas: CSV -> JSON -> config_fixed.py -> hardcoded default
    """
    # Define required parameters
    required_params = [
        'species_name', 'initial_population', 'reproduction_rate', 'mortality_rate',
        'consumption_rate', 'mobility', 'initial_energy', 'reproduction_threshold',
        'metabolic_cost', 'min_temp', 'max_temp', 'min_humidity', 'max_humidity',
        'max_age', 'foraging_efficiency'
    ]
    
    # Coba load dari CSV
    csv_config = load_config_from_csv('data/elk_data.csv')
    if csv_config and validate_config(csv_config, required_params):
        config = csv_config
        # logger.info("📊 Using elk config from CSV")
    else:
        # Coba load dari JSON
        json_config = load_config_from_json('data/species_config.json', 'elk')
        if json_config and validate_config(json_config, required_params):
            config = json_config
            # logger.info("📄 Using elk config from JSON")
        else:
            # Fallback ke config_fixed.py
            try:
                from data.config_fixed import ELK_CONFIG
                config = ELK_CONFIG.copy()
                # logger.info("⚙️  Using elk config from config_fixed.py")
            except ImportError:
                # Ultimate fallback - hardcoded default
                config = {
                    'species_name': 'Elk',
                    'initial_population': 20,
                    'reproduction_rate': 0.2,
                    'mortality_rate': 0.001,
                    'consumption_rate': 25.0,
                    'mobility': 2,
                    'initial_energy': 150.0,
                    'reproduction_threshold': 100.0,
                    'metabolic_cost': 6.0,
                    'min_temp': -10.0,
                    'max_temp': 25.0,
                    'min_humidity': 30.0,
                    'max_humidity': 85.0,
                    'max_age': 1095,
                    'foraging_efficiency': 0.9,
                    'herd_size': 5,
                    'defense_strength': 0.4
                }
                logger.info("🔧 Using hardcoded elk default config")
    
    # Apply reproduction boost if requested
    if boost_reproduction:
        config = apply_reproduction_boost(config, 'elk')
        logger.info("🚀 Applied reproduction boost to elk config")
    
    return config

def get_environment_config():
    """
    Get environment configuration with automatic fallback
    Prioritas: JSON -> config_fixed.py -> hardcoded default
    """
    # Coba load dari JSON
    json_config = load_config_from_json('data/environment_config.json')
    if json_config:
        # logger.info("📄 Using environment config from JSON")
        return json_config
    
    # Fallback ke config_fixed.py
    try:
        from data.config_fixed import ENVIRONMENT_CONFIG
        logger.info("⚙️  Using environment config from config_fixed.py")
        return ENVIRONMENT_CONFIG.copy()
    except ImportError:
        # Ultimate fallback - hardcoded default
        logger.info("🔧 Using hardcoded environment default config")
        return {
            'base_temperature': 20.0,
            'base_humidity': 65.0,
            'food_regeneration_rate': 3.5,
            'max_food_per_cell': 120.0,
            'water_per_cell': 100.0,
            'seasonal_amplitude': 8.0,
            'seasonal_frequency': 0.017,
            'food_quality_variation': 0.2,
            'water_depletion_rate': 0.1
        }

def get_simulation_config():
    """
    Get simulation configuration with automatic fallback
    Prioritas: JSON -> config_fixed.py -> hardcoded default
    """
    # Coba load dari JSON
    json_config = load_config_from_json('data/simulation_config.json')
    if json_config:
        logger.info("📄 Using simulation config from JSON")
        return json_config
    
    # Fallback ke config_fixed.py
    try:
        from data.config_fixed import SIMULATION_CONFIG
        logger.info("⚙️  Using simulation config from config_fixed.py")
        return SIMULATION_CONFIG.copy()
    except ImportError:
        # Ultimate fallback - hardcoded default
        logger.info("🔧 Using hardcoded simulation default config")
        return {
            'grid_width': 50,
            'grid_height': 50,
            'max_steps': 250,
            'carrying_capacity': 200,
            'show_progress_every': 25,
            'save_data': True
        }

def apply_reproduction_boost(config: Dict[str, Any], species_type: str) -> Dict[str, Any]:
    """
    Apply reproduction boost ke config
    """
    boosted_config = config.copy()
    
    if species_type == 'herbivore':
        # Boost herbivore reproduction
        boosted_config['reproduction_rate'] = config.get('reproduction_rate', 0.3) * 1.5  # +50%
        boosted_config['reproduction_threshold'] = config.get('reproduction_threshold', 75.0) * 0.8  # -20%
        boosted_config['consumption_rate'] = config.get('consumption_rate', 15.0) * 1.2  # +20%
        boosted_config['metabolic_cost'] = config.get('metabolic_cost', 4.0) * 0.8  # -20%
        
    elif species_type == 'carnivore':
        # Boost carnivore reproduction
        boosted_config['reproduction_rate'] = config.get('reproduction_rate', 0.12) * 1.5  # +50%
        boosted_config['reproduction_threshold'] = config.get('reproduction_threshold', 85.0) * 0.85  # -15%
        boosted_config['predation_rate'] = config.get('predation_rate', 0.15) * 1.25  # +25%
        boosted_config['energy_per_kill'] = config.get('energy_per_kill', 40.0) * 1.2  # +20%
        boosted_config['hunting_cost'] = config.get('hunting_cost', 4.0) * 0.8  # -20%
        
    elif species_type == 'elk':
        # Boost elk reproduction
        boosted_config['reproduction_rate'] = config.get('reproduction_rate', 0.2) * 1.4  # +40%
        boosted_config['reproduction_threshold'] = config.get('reproduction_threshold', 120.0) * 0.85  # -15%
        boosted_config['consumption_rate'] = config.get('consumption_rate', 25.0) * 1.15  # +15%
        boosted_config['metabolic_cost'] = config.get('metabolic_cost', 6.0) * 0.85  # -15%
    
    return boosted_config

def create_template_files():
    """
    Buat template files CSV dan JSON untuk user
    """
    logger.info("📝 Creating template files...")
    
    # Buat directory data jika belum ada
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Template CSV untuk herbivore
    herbivore_csv = """parameter,value,data_type,description
species_name,Kelinci_Custom,str,Nama spesies
initial_population,60,int,Populasi awal
reproduction_rate,0.35,float,Tingkat reproduksi per hari
mortality_rate,0.02,float,Tingkat mortalitas per hari
consumption_rate,16.0,float,Konsumsi makanan per hari
mobility,1,int,Jarak bergerak per hari
initial_energy,110.0,float,Energi awal
reproduction_threshold,65.0,float,Energi minimum untuk reproduksi
metabolic_cost,3.5,float,Biaya metabolik per hari
min_temp,3.0,float,Suhu minimum toleransi
max_temp,32.0,float,Suhu maksimum toleransi
min_humidity,35.0,float,Kelembaban minimum toleransi
max_humidity,85.0,float,Kelembaban maksimum toleransi
max_age,750,int,Usia maksimum (hari)
foraging_efficiency,0.88,float,Efisiensi mencari makan"""
    
    # Template JSON untuk semua spesies
    species_json = {
        "herbivore": {
            "species_name": "Kelinci_JSON",
            "initial_population": 65,
            "reproduction_rate": 0.32,
            "mortality_rate": 0.018,
            "consumption_rate": 17.0,
            "mobility": 1,
            "initial_energy": 105.0,
            "reproduction_threshold": 62.0,
            "metabolic_cost": 3.2,
            "min_temp": 4.0,
            "max_temp": 31.0,
            "min_humidity": 38.0,
            "max_humidity": 82.0,
            "max_age": 720,
            "foraging_efficiency": 0.87
        },
        "carnivore": {
            "species_name": "Serigala_JSON",
            "initial_population": 18,
            "reproduction_rate": 0.15,
            "mortality_rate": 0.0008,
            "mobility": 4,
            "initial_energy": 130.0,
            "reproduction_threshold": 80.0,
            "metabolic_cost": 3.5,
            "min_temp": -32.0,
            "max_temp": 27.0,
            "min_humidity": 18.0,
            "max_humidity": 88.0,
            "max_age": 2200,
            "predation_rate": 0.18,
            "conversion_efficiency": 0.78,
            "hunt_range": 3,
            "energy_per_kill": 45.0,
            "hunting_cost": 3.5,
            "pack_hunting_bonus": 1.9,
            "starvation_tolerance": 16,
            "hunt_cooldown": 0.5
        },
        "elk": {
            "species_name": "Elk_JSON",
            "initial_population": 25,
            "reproduction_rate": 0.25,
            "mortality_rate": 0.0012,
            "consumption_rate": 27.0,
            "mobility": 2,
            "initial_energy": 160.0,
            "reproduction_threshold": 110.0,
            "metabolic_cost": 6.5,
            "min_temp": -12.0,
            "max_temp": 28.0,
            "min_humidity": 28.0,
            "max_humidity": 88.0,
            "max_age": 1100,
            "foraging_efficiency": 0.92,
            "herd_size": 6,
            "defense_strength": 0.45
        }
    }
    
    # Environment config template
    environment_json = {
        "base_temperature": 18.0,
        "base_humidity": 68.0,
        "food_regeneration_rate": 4.0,
        "max_food_per_cell": 130.0,
        "water_per_cell": 110.0,
        "seasonal_amplitude": 9.0,
        "seasonal_frequency": 0.018,
        "food_quality_variation": 0.25,
        "water_depletion_rate": 0.12
    }
    
    # Simulation config template
    simulation_json = {
        "grid_width": 60,
        "grid_height": 60,
        "max_steps": 300,
        "carrying_capacity": 250,
        "show_progress_every": 30,
        "save_data": True
    }
    
    try:
        # Save CSV template
        with open(data_dir / 'herbivore_data.csv', 'w', encoding='utf-8') as f:
            f.write(herbivore_csv)
        logger.info("✅ Created herbivore_data.csv template")
        
        # Save JSON templates
        with open(data_dir / 'species_config.json', 'w', encoding='utf-8') as f:
            json.dump(species_json, f, indent=2, ensure_ascii=False)
        logger.info("✅ Created species_config.json template")
        
        with open(data_dir / 'environment_config.json', 'w', encoding='utf-8') as f:
            json.dump(environment_json, f, indent=2, ensure_ascii=False)
        logger.info("✅ Created environment_config.json template")
        
        with open(data_dir / 'simulation_config.json', 'w', encoding='utf-8') as f:
            json.dump(simulation_json, f, indent=2, ensure_ascii=False)
        logger.info("✅ Created simulation_config.json template")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating template files: {e}")
        return False

def check_data_availability():
    """
    Cek ketersediaan file data dan tampilkan status
    """
    logger.info("🔍 Checking data file availability...")
    
    files_to_check = [
        ('data/herbivore_data.csv', 'Herbivore CSV'),
        ('data/carnivore_data.csv', 'Carnivore CSV'),
        ('data/elk_data.csv', 'Elk CSV'),
        ('data/species_config.json', 'Species JSON'),
        ('data/environment_config.json', 'Environment JSON'),
        ('data/simulation_config.json', 'Simulation JSON')
    ]
    
    status = {}
    for file_path, description in files_to_check:
        exists = os.path.exists(file_path)
        status[description] = exists
        icon = "✅" if exists else "❌"
        logger.info(f"   {icon} {description}: {file_path}")
    
    # Check fallback availability
    try:
        from data.config_fixed import HERBIVORE_CONFIG
        fallback_available = True
        logger.info("   ✅ config_fixed.py fallback available")
    except ImportError:
        fallback_available = False
        logger.info("   ❌ config_fixed.py fallback not available")
    
    status['fallback_available'] = fallback_available
    
    # Recommendations
    if not any(status.values()):
        logger.info("💡 No external data found. Run create_template_files() to get started")
    elif not all(status.values()):
        logger.info("💡 Some data files missing. Check templates in data/ directory")
    else:
        logger.info("✅ All data sources available!")
    
    return status

# Demo/test function
if __name__ == "__main__":
    print("🔧 ENHANCED CONFIG HELPER - DEMO")
    print("=" * 50)
    
    # Check current data availability
    print("\n📊 Checking data availability...")
    status = check_data_availability()
    
    # Create templates if needed
    if not any(status.values()):
        print("\n📝 Creating template files...")
        create_template_files()
    
    # Test loading configs
    print("\n🐾 Testing config loading...")
    
    try:
        herbivore_config = get_herbivore_config()
        print(f"   🐰 Herbivore: {herbivore_config['species_name']} (pop: {herbivore_config['initial_population']})")
    except Exception as e:
        print(f"   ❌ Herbivore config error: {e}")
    
    try:
        carnivore_config = get_carnivore_config(boost_reproduction=True)
        print(f"   🐺 Carnivore: {carnivore_config['species_name']} (pop: {carnivore_config['initial_population']}) [BOOSTED]")
    except Exception as e:
        print(f"   ❌ Carnivore config error: {e}")
    
    try:
        elk_config = get_elk_config()
        print(f"   🦌 Elk: {elk_config['species_name']} (pop: {elk_config['initial_population']})")
    except Exception as e:
        print(f"   ❌ Elk config error: {e}")
    
    print("\n✅ Demo complete!")
    print("💡 Edit files in data/ directory to customize parameters")
    print("💡 System will automatically use external files if available")
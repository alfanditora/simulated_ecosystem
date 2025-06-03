"""
Konfigurasi parameter simulasi ekosistem - VERSI DIPERBAIKI
Berdasarkan analisis kepunahan dini dan data biologis yang lebih akurat
"""

# Parameter Simulasi Umum
SIMULATION_CONFIG = {
    'grid_width': 50,
    'grid_height': 50,
    'max_steps': 50,
    'carrying_capacity': 200,
    'show_progress_every': 25,  # Lebih sering untuk monitoring
    'save_data': True
}
# =====================================================================================
# PARAMETER ELK - BERDASARKAN DATA YELLOWSTONE
# =====================================================================================

ELK_CONFIG = {
    'species_name': 'Elk',
    'initial_population': 40,              # Berdasarkan ratio Yellowstone: 95 wolves : 7000-12000 elk
    
    # Parameter biologis elk
    'reproduction_rate': 0.4,            # Lebih rendah dari kelinci
    'mortality_rate': 0.01,               # Rendah karena ukuran besar
    'consumption_rate': 25.0,              # 60% lebih banyak dari kelinci
    'mobility': 2,                         # Sama dengan kelinci
    'initial_energy': 150.0,               # 50% lebih besar
    'reproduction_threshold': 100.0,       # Lebih tinggi
    'metabolic_cost': 6.0,                 # 50% lebih tinggi dari kelinci
    
    # Toleransi lingkungan - lebih hardy
    'min_temp': -15.0,                     # Lebih tahan dingin
    'max_temp': 25.0,
    'min_humidity': 25.0,
    'max_humidity': 85.0,
    'max_age': 1095,                       # 3 tahun
    
    # Parameter khusus elk
    'foraging_efficiency': 0.9,            # Lebih efisien dari kelinci
    'herd_size': 5,                        # Hidup berkelompok
    'defense_strength': 0.4,               # Bisa melawan predator (40% reduction)
    'flee_distance': 4,                    # Jarak flee dari predator
}

# =====================================================================================
# PARAMETER HERBIVORA - SUDAH CUKUP BAIK
# =====================================================================================

HERBIVORE_CONFIG = {
    'species_name': 'Kelinci',
    'initial_population': 60,
    
    # Parameter reproduksi dan mortalitas (sudah dikalibrasi dengan baik)
    'reproduction_rate': 0.3,           # 0.3% per hari - realistic
    'mortality_rate': 0.02,              # Sedikit dinaikkan karena predasi
    'consumption_rate': 15.0,             # Kebutuhan makanan harian
    'mobility': 1,                        # Pergerakan harian
    'initial_energy': 100.0,
    'reproduction_threshold': 60.0,       # Sedikit dikurangi
    'metabolic_cost': 3.0,                # Sedikit dikurangi
    
    # Toleransi lingkungan
    'min_temp': 5.0,
    'max_temp': 30.0,
    'min_humidity': 40.0,
    'max_humidity': 80.0,
    'max_age': 730,                       # 2 tahun
    
    # Parameter tambahan
    'foraging_efficiency': 0.85,          # Sedikit dinaikkan
}

# =====================================================================================
# PARAMETER KARNIVORA - DIPERBAIKI BERDASARKAN DATA YELLOWSTONE
# =====================================================================================

CARNIVORE_CONFIG = {
    'species_name': 'Serigala',
    'initial_population': 50,              # Dikurangi sedikit untuk stabilitas awal
    
    # PARAMETER UTAMA YANG DIPERBAIKI
    'reproduction_rate': 0.5,          # Sedikit dinaikkan untuk kompensasi
    'mortality_rate': 0.0006,             # Dikurangi dari 0.0004
    'mobility': 4,                        # Tetap
    'initial_energy': 250.0,              # Dinaikkan untuk buffer
    'reproduction_threshold': 65.0,       # Dinaikkan
    'metabolic_cost': 3.0,                # ⭐ DIPERBAIKI: 8.0 → 3.0
    
    # Toleransi lingkungan
    'min_temp': -30.0,                    # Lebih toleran
    'max_temp': 25.0,
    'min_humidity': 20.0,
    'max_humidity': 85.0,
    'max_age': 2190,                      # 6 tahun
    
    # PARAMETER PREDASI YANG DIPERBAIKI
    'predation_rate': 0.25,               # ⭐ DIPERBAIKI: 0.3 → 0.15 (solo hunting)
    'conversion_efficiency': 0.85,        # ⭐ DIPERBAIKI: 0.6 → 0.75 (lebih efisien)
    'hunt_range': 8,
    'energy_per_kill': 50.0,              # ⭐ DIPERBAIKI: 60.0 → 40.0 (lebih realistis)
    'hunting_cost': 1.0,                  # ⭐ DIPERBAIKI: 10.0 → 4.0
    
    # PARAMETER BARU UNTUK STABILITAS
    'pack_hunting_bonus': 1.8,            # Bonus jika ada karnivora lain nearby
    'starvation_tolerance': 15,           # Bisa bertahan 12 hari tanpa makan
    'hunt_cooldown': 1,                   # Istirahat 1 hari setelah berburu sukses
    'territorial_range': 8,               # Range teritorial
}

# =====================================================================================
# PARAMETER LINGKUNGAN - SEDIKIT DIPERBAIKI
# =====================================================================================

ENVIRONMENT_CONFIG = {
    'base_temperature': 20.0,             # Sedikit dikurangi untuk kondisi lebih dingin
    'base_humidity': 65.0,                # Sedikit dinaikkan
    'food_regeneration_rate': 3.5,        # Sedikit dinaikkan untuk support populasi
    'max_food_per_cell': 120.0,           # Dinaikkan untuk carrying capacity
    'water_per_cell': 100.0,
    'seasonal_amplitude': 8.0,            # Dinaikkan untuk variasi musiman
    'seasonal_frequency': 0.017,          # 2π/365 untuk siklus tahunan
    
    # Parameter baru
    'food_quality_variation': 0.2,        # 20% variasi kualitas makanan
    'water_depletion_rate': 0.1,          # Air berkurang karena konsumsi
}

# =====================================================================================
# VALIDASI PARAMETER BERDASARKAN DATA BIOLOGIS
# =====================================================================================

BIOLOGICAL_VALIDATION = {
    'energy_balance_carnivore': {
        'daily_energy_gain_expected': 0.15 * 40.0 * 0.75,     # 4.5 unit/hari
        'daily_energy_loss_expected': 3.0 + 4.0,              # 7.0 unit/hari  
        'net_balance': -2.5,                                   # Deficit kecil
        'buffer_from_initial_energy': 120.0,                  # 48 hari buffer
        'pack_hunting_compensation': 1.8,                     # Bonus pack
        'starvation_tolerance_days': 12,                      # Safety net
        'conclusion': 'Sustainable dengan pack hunting dan occasional success'
    },
    
    'yellowstone_comparison': {
        'wolf_daily_food_kg': 2.5,
        'rabbit_weight_kg': 2.0,
        'wolves_per_rabbit_per_day': 1.25,                    # 2.5/2.0
        'simulation_energy_ratio': 40.0/120.0,                # 0.33
        'hunting_success_real': 0.10,                         # 10% pack hunting
        'hunting_success_simulation': 0.15,                   # 15% solo (reasonable)
        'validation_status': 'Within acceptable range'
    },
    
    'population_dynamics_expected': {
        'herbivore_stable_range': (40, 80),
        'carnivore_stable_range': (5, 15),
        'predator_prey_ratio_target': (0.1, 0.3),
        'extinction_risk_days': 50,                           # Harapan survive > 50 hari
        'stability_threshold_steps': 150,                     # Stabil dalam 150 hari
    }
}

# =====================================================================================
# INFORMASI PERBAIKAN
# =====================================================================================

IMPROVEMENT_LOG = {
    'version': '2.0_fixed',
    'date': '2024-12-19',
    'issues_fixed': [
        'Metabolic cost terlalu tinggi (8.0 → 3.0)',
        'Hunting cost terlalu tinggi (10.0 → 4.0)', 
        'Predation rate terlalu tinggi untuk solo hunting (0.3 → 0.15)',
        'Energy per kill terlalu tinggi (60.0 → 40.0)',
        'Conversion efficiency terlalu rendah (0.6 → 0.75)',
        'Tidak ada pack hunting mechanism',
        'Tidak ada starvation tolerance'
    ],
    'new_features': [
        'Pack hunting bonus (1.8x)',
        'Starvation tolerance (12 hari)',
        'Hunt cooldown mechanism',
        'Territorial behavior',
        'Food quality variation',
        'Water depletion'
    ],
    'data_sources_validation': [
        'Yellowstone Wolf Project (hunting success rates)',
        'GBIF energy metabolism data',
        'Animal Diversity Web behavioral data',
        'Trophic cascade studies (Ripple & Beschta)',
        'Wolf-prey ratio studies (Peterson & Ciucci)'
    ]
}

def print_improvement_summary():
    """
    Print ringkasan perbaikan parameter
    """
    print("🔧 RINGKASAN PERBAIKAN PARAMETER v2.0")
    print("=" * 60)
    
    print("❌ MASALAH YANG DIPERBAIKI:")
    for issue in IMPROVEMENT_LOG['issues_fixed']:
        print(f"   • {issue}")
    
    print("\n✅ FITUR BARU:")
    for feature in IMPROVEMENT_LOG['new_features']:
        print(f"   • {feature}")
    
    print(f"\n📊 PREDIKSI HASIL:")
    validation = BIOLOGICAL_VALIDATION['energy_balance_carnivore']
    print(f"   • Energy gain: {validation['daily_energy_gain_expected']:.1f} unit/hari")
    print(f"   • Energy loss: {validation['daily_energy_loss_expected']:.1f} unit/hari")
    print(f"   • Net balance: {validation['net_balance']:.1f} unit/hari")
    print(f"   • Survival buffer: {validation['buffer_from_initial_energy']/abs(validation['net_balance']):.0f} hari")
    print(f"   • Conclusion: {validation['conclusion']}")
    
    dynamics = BIOLOGICAL_VALIDATION['population_dynamics_expected']
    print(f"\n🎯 TARGET POPULASI:")
    print(f"   • Herbivora stabil: {dynamics['herbivore_stable_range']}")
    print(f"   • Karnivora stabil: {dynamics['carnivore_stable_range']}")
    print(f"   • Rasio target: {dynamics['predator_prey_ratio_target']}")
    print(f"   • Survival target: >{dynamics['extinction_risk_days']} hari")

if __name__ == "__main__":
    print_improvement_summary()
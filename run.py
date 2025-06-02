"""
File utama untuk menjalankan simulasi ekosistem - VERSI DIPERBAIKI
"""

# ⭐ IMPORT KONFIGURASI YANG DIPERBAIKI
try:
    from data.config_fixed import SIMULATION_CONFIG, print_improvement_summary
    USE_FIXED_CONFIG = True
    print("🔧 Menggunakan konfigurasi yang diperbaiki (v2.0)")
except ImportError:
    from data.config import SIMULATION_CONFIG  
    USE_FIXED_CONFIG = False
    print("⚠️  Menggunakan konfigurasi default")

from models.ecosystem import EcosystemSimulation
from visualization.plots import create_plots

def main():
    """
    Fungsi utama untuk menjalankan simulasi
    """
    print("🌱 SIMULASI EKOSISTEM - AGENT BASED MODEL v2.0")
    print("=" * 60)
    # print("📋 Implementasi rumus dari PDF (DIPERBAIKI):")
    # print("   • Reproduksi: dN/dt = rN(1-N/K)")
    # print("   • Kematian: P_mati = d + f_lingkungan + f_kelaparan")
    # print("   • Predasi: Model Lotka-Volterra (dengan pack hunting)")
    # print("   • Lingkungan: T(t) = T0 + A*sin(ωt)")
    
    # if USE_FIXED_CONFIG:
    #     print("\n🔧 PERBAIKAN v2.0:")
    #     print("   ✅ Metabolic cost dikurangi (8.0 → 3.0)")
    #     print("   ✅ Hunting cost dikurangi (10.0 → 4.0)")
    #     print("   ✅ Predation rate disesuaikan (0.3 → 0.15)")
    #     print("   ✅ Pack hunting bonus (+80%)")
    #     print("   ✅ Starvation tolerance (12 hari)")
    #     print("   ✅ Energy balance diperbaiki")
    
    # print("=" * 60)
    
    # Show improvement summary if available
    # if USE_FIXED_CONFIG:
    #     print("\n📊 RINGKASAN PERBAIKAN:")
    #     try:
    #         print_improvement_summary()
    #     except:
    #         pass
    #     print("-" * 60)
    
    # Pilihan mode visualisasi
    print("\n🎨 Pilihan mode visualisasi:")
    print("1. Simulasi normal (tanpa real-time visualization)")
    print("2. Simulasi dengan real-time visualization") 
    print("3. Debug mode (extra monitoring)")
    
    try:
        choice = input("\nPilih mode (1, 2, atau 3): ").strip()
        realtime_vis = (choice == "2")
        debug_mode = (choice == "3")
    except KeyboardInterrupt:
        print("\n❌ Simulasi dibatalkan")
        return
    
    # Inisialisasi simulasi
    print("\n🔧 Inisialisasi simulasi...")
    sim = EcosystemSimulation(
        width=SIMULATION_CONFIG['grid_width'],
        height=SIMULATION_CONFIG['grid_height']
    )
    
    # Setup spesies
    print("🦎 Setup spesies...")
    sim.setup_species()
    
    print(f"\n📊 Konfigurasi simulasi:")
    print(f"   • Grid: {SIMULATION_CONFIG['grid_width']}x{SIMULATION_CONFIG['grid_height']}")
    print(f"   • Langkah maksimum: {SIMULATION_CONFIG['max_steps']}")
    print(f"   • Carrying capacity: {SIMULATION_CONFIG['carrying_capacity']}")
    print(f"   • Progress setiap: {SIMULATION_CONFIG['show_progress_every']} langkah")
    print(f"   • Real-time visualization: {'✅ Ya' if realtime_vis else '❌ Tidak'}")
    print(f"   • Debug mode: {'✅ Ya' if debug_mode else '❌ Tidak'}")
    print(f"   • Parameter version: {'v2.0 (Fixed)' if USE_FIXED_CONFIG else 'v1.0 (Original)'}")
    print("-" * 60)
    
    # Jalankan simulasi
    print("\n🚀 Menjalankan simulasi...")
    if realtime_vis:
        print("🎬 Window real-time visualization akan terbuka...")
        print("💡 Tip: Posisikan window agar terlihat selama simulasi")
    
    if debug_mode:
        print("🐛 Debug mode: Monitoring extra untuk troubleshooting")
    
    # ⭐ PERBAIKAN: Monitoring lebih ketat untuk deteksi masalah dini
    sim.run(steps=SIMULATION_CONFIG['max_steps'], realtime_vis=realtime_vis)
    
    # Tampilkan hasil
    print("\n📈 Analisis hasil...")
    sim.show_results()
    
    # ⭐ ANALISIS TAMBAHAN untuk validasi perbaikan
    if USE_FIXED_CONFIG:
        print("\n🔍 VALIDASI PERBAIKAN:")
        stats = sim.get_statistics()
        if "error" not in stats:
            final_herbs = stats.get('final_herbivores', 0)
            final_carns = stats.get('final_carnivores', 0) 
            total_steps = stats.get('total_steps', 0)
            
            print(f"   📊 Survival test: {total_steps} hari")
            if total_steps >= 50 and final_carns > 0:
                print("   ✅ SUKSES: Karnivora survive >50 hari!")
            elif final_carns > 0:
                print(f"   ⚠️  PARTIAL: Karnivora survive {total_steps} hari")
            else:
                print("   ❌ GAGAL: Karnivora masih punah")
            
            if final_herbs > 0 and final_carns > 0:
                ratio = final_carns / final_herbs
                print(f"   📈 Rasio akhir: {ratio:.3f}")
                if 0.1 <= ratio <= 0.3:
                    print("   ✅ OPTIMAL: Rasio dalam range biologis")
                else:
                    print("   ⚠️  SUBOPTIMAL: Rasio di luar range")
    
    # Buat visualisasi
    # print("\n🎨 Membuat visualisasi...")
    # try:
    #     stats = sim.get_statistics()
    #     if "error" not in stats:
    #         create_plots(stats)
    #     else:
    #         print(f"⚠️  Visualisasi dilewati: {stats['error']}")
    # except Exception as e:
    #     print(f"❌ Error visualisasi: {e}")
    #     print("💡 Pastikan matplotlib terinstall: pip install matplotlib")
    
    # print("\n" + "=" * 60)
    # print("✅ SIMULASI SELESAI!")
    # print("📊 Cek grafik yang muncul untuk analisis detail")
    # if USE_FIXED_CONFIG:
    #     print("🔧 Menggunakan parameter yang diperbaiki berdasarkan data biologis")
    # print("🔄 Jalankan ulang untuk simulasi dengan seed berbeda")
    # print("=" * 60)

if __name__ == "__main__":
    main()
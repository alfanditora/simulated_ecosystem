"""
Kelas untuk visualisasi dan analisis hasil simulasi ekosistem
Implementasi grafik berdasarkan metrik evaluasi dari PDF
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List

class EcosystemPlotter:
    """
    Kelas untuk membuat visualisasi hasil simulasi ekosistem
    """
    
    def __init__(self, statistics: Dict[str, Any]):
        self.stats = statistics
        self.population_history = statistics.get('population_history', {})
        
        # Setup matplotlib style
        plt.style.use('default')
        self.colors = {
            'herbivore': '#2E8B57',  # Sea Green
            'carnivore': '#CD5C5C',  # Indian Red
            'environment': '#4682B4', # Steel Blue
            'ratio': '#9370DB'       # Medium Purple
        }
    
    def plot_population_dynamics(self):
        """
        Plot dinamika populasi predator-mangsa (Lotka-Volterra)
        """
        if not self.population_history:
            print("❌ Tidak ada data populasi untuk diplot")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Populasi vs Waktu
        time_steps = range(len(self.population_history['herbivore']))
        
        ax1.plot(time_steps, self.population_history['herbivore'], 
                color=self.colors['herbivore'], linewidth=2, label='🐰 Herbivora (Kelinci)')
        ax1.plot(time_steps, self.population_history['carnivore'], 
                color=self.colors['carnivore'], linewidth=2, label='🐺 Karnivora (Serigala)')
        
        ax1.set_xlabel('Langkah Waktu')
        ax1.set_ylabel('Populasi')
        ax1.set_title('Dinamika Populasi Predator-Mangsa (Model Lotka-Volterra)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Phase Plot (Predator vs Prey)
        ax2.plot(self.population_history['herbivore'], self.population_history['carnivore'], 
                color=self.colors['ratio'], linewidth=1.5, alpha=0.7)
        ax2.scatter(self.population_history['herbivore'][0], self.population_history['carnivore'][0], 
                   color='green', s=100, marker='o', label='Start', zorder=5)
        ax2.scatter(self.population_history['herbivore'][-1], self.population_history['carnivore'][-1], 
                   color='red', s=100, marker='X', label='End', zorder=5)
        
        ax2.set_xlabel('Populasi Herbivora')
        ax2.set_ylabel('Populasi Karnivora')
        ax2.set_title('Phase Plot Lotka-Volterra')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_ecosystem_metrics(self):
        """
        Plot metrik evaluasi ekosistem dari PDF
        """
        if not self.population_history:
            print("❌ Tidak ada data untuk metrik")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Stabilitas Populasi (Standard Deviation)
        window_size = 50
        herb_rolling_std = self._calculate_rolling_std(self.population_history['herbivore'], window_size)
        carn_rolling_std = self._calculate_rolling_std(self.population_history['carnivore'], window_size)
        
        time_steps = range(window_size, len(herb_rolling_std) + window_size)
        ax1.plot(time_steps, herb_rolling_std, color=self.colors['herbivore'], 
                label='Herbivora', linewidth=2)
        ax1.plot(time_steps, carn_rolling_std, color=self.colors['carnivore'], 
                label='Karnivora', linewidth=2)
        ax1.set_xlabel('Langkah Waktu')
        ax1.set_ylabel('Standard Deviation')
        ax1.set_title('Stabilitas Populasi (Rolling Std Dev)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Rasio Predator:Mangsa
        ratios = []
        for i in range(len(self.population_history['herbivore'])):
            herb_pop = self.population_history['herbivore'][i]
            carn_pop = self.population_history['carnivore'][i]
            ratio = carn_pop / max(1, herb_pop)  # Hindari division by zero
            ratios.append(ratio)
        
        ax2.plot(range(len(ratios)), ratios, color=self.colors['ratio'], linewidth=2)
        ax2.axhline(y=np.mean(ratios), color='red', linestyle='--', alpha=0.7, 
                   label=f'Rata-rata: {np.mean(ratios):.3f}')
        ax2.set_xlabel('Langkah Waktu')
        ax2.set_ylabel('Rasio Predator/Mangsa')
        ax2.set_title('Keseimbangan Ekosistem')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Histogram Distribusi Populasi
        ax3.hist(self.population_history['herbivore'], bins=20, alpha=0.7, 
                color=self.colors['herbivore'], label='Herbivora', density=True)
        ax3.hist(self.population_history['carnivore'], bins=20, alpha=0.7, 
                color=self.colors['carnivore'], label='Karnivora', density=True)
        ax3.set_xlabel('Populasi')
        ax3.set_ylabel('Density')
        ax3.set_title('Distribusi Populasi')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Kondisi Lingkungan
        if 'total_food' in self.population_history and 'avg_temperature' in self.population_history:
            ax4_twin = ax4.twinx()
            
            # Plot makanan
            ax4.plot(range(len(self.population_history['total_food'])), 
                    self.population_history['total_food'], 
                    color=self.colors['environment'], linewidth=2, label='Total Makanan')
            ax4.set_xlabel('Langkah Waktu')
            ax4.set_ylabel('Total Makanan', color=self.colors['environment'])
            ax4.tick_params(axis='y', labelcolor=self.colors['environment'])
            
            # Plot suhu
            ax4_twin.plot(range(len(self.population_history['avg_temperature'])), 
                         self.population_history['avg_temperature'], 
                         color='orange', linewidth=2, label='Suhu Rata-rata')
            ax4_twin.set_ylabel('Suhu (°C)', color='orange')
            ax4_twin.tick_params(axis='y', labelcolor='orange')
            
            ax4.set_title('Kondisi Lingkungan')
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'Data lingkungan\ntidak tersedia', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Kondisi Lingkungan')
        
        plt.tight_layout()
        plt.show()
    
    def plot_summary_analysis(self):
        """
        Plot ringkasan analisis dengan interpretasi
        """
        if 'error' in self.stats:
            print(f"❌ {self.stats['error']}")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Populasi Akhir (Bar Chart)
        species = ['Herbivora', 'Karnivora']
        final_pops = [self.stats['final_herbivores'], self.stats['final_carnivores']]
        colors = [self.colors['herbivore'], self.colors['carnivore']]
        
        bars = ax1.bar(species, final_pops, color=colors, alpha=0.7)
        ax1.set_ylabel('Populasi Akhir')
        ax1.set_title('Populasi Akhir Simulasi')
        
        # Tambah nilai di atas bar
        for bar, value in zip(bars, final_pops):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{value:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Stabilitas (Bar Chart)
        stability_metrics = ['Herbivora Stability', 'Karnivora Stability']
        stability_values = [self.stats['herbivore_stability'], self.stats['carnivore_stability']]
        
        bars2 = ax2.bar(stability_metrics, stability_values, color=colors, alpha=0.7)
        ax2.set_ylabel('Standard Deviation')
        ax2.set_title('Stabilitas Populasi')
        ax2.tick_params(axis='x', rotation=45)
        
        # Interpretasi stabilitas
        for bar, value in zip(bars2, stability_values):
            interpretation = "Stabil" if value < 10 else "Cukup Stabil" if value < 20 else "Tidak Stabil"
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{value:.1f}\n({interpretation})', ha='center', va='bottom', fontsize=9)
        
        # 3. Timeline Populasi (Simple)
        time_steps = range(len(self.population_history['herbivore']))
        ax3.plot(time_steps, self.population_history['herbivore'], 
                color=self.colors['herbivore'], linewidth=2, label='Herbivora')
        ax3.plot(time_steps, self.population_history['carnivore'], 
                color=self.colors['carnivore'], linewidth=2, label='Karnivora')
        ax3.set_xlabel('Langkah Waktu')
        ax3.set_ylabel('Populasi')
        ax3.set_title('Timeline Populasi')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Statistik Ringkasan (Text)
        ax4.axis('off')
        
        # Evaluasi ekosistem
        herb_stable = self.stats['herbivore_stability'] < 10
        carn_stable = self.stats['carnivore_stability'] < 5
        
        if herb_stable and carn_stable:
            ecosystem_status = "✅ STABIL"
            status_color = 'green'
        elif self.stats['herbivore_stability'] < 20 and self.stats['carnivore_stability'] < 10:
            ecosystem_status = "⚠️ CUKUP STABIL"
            status_color = 'orange'
        else:
            ecosystem_status = "❌ TIDAK STABIL"
            status_color = 'red'
        
        summary_text = f"""
📊 RINGKASAN ANALISIS EKOSISTEM

⏱️ Total Simulasi: {self.stats['total_steps']} langkah

🐰 Herbivora Akhir: {self.stats['final_herbivores']:.0f}
🐺 Karnivora Akhir: {self.stats['final_carnivores']:.0f}

📈 Stabilitas Herbivora: {self.stats['herbivore_stability']:.2f}
📈 Stabilitas Karnivora: {self.stats['carnivore_stability']:.2f}

⚖️ Rasio Predator:Mangsa: {self.stats['predator_prey_ratio']:.3f}

🏆 Status Ekosistem: {ecosystem_status}
        """
        
        ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def _calculate_rolling_std(self, data: List[float], window_size: int) -> List[float]:
        """
        Hitung rolling standard deviation
        """
        rolling_std = []
        for i in range(window_size, len(data)):
            window_data = data[i-window_size:i]
            rolling_std.append(np.std(window_data))
        return rolling_std
    
    def plot_all(self):
        """
        Plot semua visualisasi sekaligus
        """
        print("📊 Membuat visualisasi hasil simulasi...")
        print("-" * 50)
        
        try:
            print("1. Plot Dinamika Populasi...")
            self.plot_population_dynamics()
            
            print("2. Plot Metrik Ekosistem...")
            self.plot_ecosystem_metrics()
            
            print("3. Plot Analisis Ringkasan...")
            self.plot_summary_analysis()
            
            print("✅ Semua visualisasi selesai!")
            
        except Exception as e:
            print(f"❌ Error dalam membuat plot: {e}")
            print("🔍 Pastikan data simulasi lengkap dan matplotlib terinstall")

def create_plots(statistics: Dict[str, Any]):
    """
    Fungsi helper untuk membuat semua plot
    """
    plotter = EcosystemPlotter(statistics)
    plotter.plot_all()
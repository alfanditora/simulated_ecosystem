"""
Real-time visualization untuk simulasi ekosistem
Menampilkan animasi live saat simulasi berjalan
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import numpy as np
from typing import Dict, Any, List
from collections import deque

class RealTimeVisualizer:
    """
    Kelas untuk visualisasi real-time simulasi ekosistem
    """
    
    def __init__(self, width: int, height: int, max_history: int = 200):
        self.width = width
        self.height = height
        self.max_history = max_history
        
        # Data history untuk plotting
        self.time_history = deque(maxlen=max_history)
        self.herbivore_history = deque(maxlen=max_history)
        self.carnivore_history = deque(maxlen=max_history)
        self.temperature_history = deque(maxlen=max_history)
        self.food_history = deque(maxlen=max_history)
        
        # Setup figure dengan subplots
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('🌱 Real-Time Ecosystem Simulation', fontsize=16, fontweight='bold')
        
        # Layout: 2x3 grid
        self.ax_spatial = plt.subplot2grid((2, 3), (0, 0), colspan=2)  # Spatial view
        self.ax_population = plt.subplot2grid((2, 3), (0, 2))          # Population trend
        self.ax_environment = plt.subplot2grid((2, 3), (1, 0))         # Environment
        self.ax_phase = plt.subplot2grid((2, 3), (1, 1))               # Phase plot
        self.ax_stats = plt.subplot2grid((2, 3), (1, 2))               # Statistics
        
        # Setup axes
        self._setup_axes()
        
        # Colors
        self.colors = {
            'herbivore': '#2E8B57',  # Sea Green
            'carnivore': '#CD5C5C',  # Indian Red
            'food_high': '#90EE90',  # Light Green
            'food_medium': '#FFFF99', # Light Yellow
            'food_low': '#FFB6C1',   # Light Pink
            'empty': '#F5F5DC'       # Beige
        }
        
        print("🎬 Real-time visualizer initialized")
    
    def _setup_axes(self):
        """Setup semua axes untuk plotting"""
        
        # 1. Spatial view (ecosystem map)
        self.ax_spatial.set_xlim(0, self.width)
        self.ax_spatial.set_ylim(0, self.height)
        self.ax_spatial.set_aspect('equal')
        self.ax_spatial.set_title('🗺️ Ecosystem Map')
        self.ax_spatial.set_xlabel('X Position')
        self.ax_spatial.set_ylabel('Y Position')
        
        # 2. Population trends
        self.ax_population.set_title('📈 Population Dynamics')
        self.ax_population.set_xlabel('Time Steps')
        self.ax_population.set_ylabel('Population')
        self.ax_population.grid(True, alpha=0.3)
        
        # 3. Environment conditions
        self.ax_environment.set_title('🌡️ Environment')
        self.ax_environment.set_xlabel('Time Steps')
        self.ax_environment.set_ylabel('Temperature (°C)')
        self.ax_environment.grid(True, alpha=0.3)
        
        # 4. Phase plot
        self.ax_phase.set_title('🔄 Phase Plot (Lotka-Volterra)')
        self.ax_phase.set_xlabel('Herbivore Population')
        self.ax_phase.set_ylabel('Carnivore Population')
        self.ax_phase.grid(True, alpha=0.3)
        
        # 5. Statistics text
        self.ax_stats.axis('off')
        self.ax_stats.set_title('📊 Live Statistics')
    
    def update_data(self, simulation_step: int, agents: List, environment, env_stats: Dict):
        """
        Update data untuk visualisasi real-time
        
        Args:
            simulation_step: Langkah simulasi saat ini
            agents: List semua agen
            environment: Environment object
            env_stats: Statistik lingkungan
        """
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent
        
        # Hitung populasi
        herbivore_count = len([a for a in agents if a.alive and isinstance(a, HerbivoreAgent)])
        carnivore_count = len([a for a in agents if a.alive and isinstance(a, CarnivoreAgent)])
        
        # Update history
        self.time_history.append(simulation_step)
        self.herbivore_history.append(herbivore_count)
        self.carnivore_history.append(carnivore_count)
        self.temperature_history.append(env_stats['avg_temperature'])
        self.food_history.append(env_stats['total_food'])
        
        # Update all plots
        self._update_spatial_view(agents, environment)
        self._update_population_plot()
        self._update_environment_plot()
        self._update_phase_plot()
        self._update_statistics(simulation_step, herbivore_count, carnivore_count, env_stats)
        
        # Refresh display
        plt.pause(0.001)  # Small pause to allow GUI update
    
    def _update_spatial_view(self, agents: List, environment):
        """Update spatial view dengan posisi agen dan kondisi lingkungan"""
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent
        
        self.ax_spatial.clear()
        self.ax_spatial.set_xlim(0, self.width)
        self.ax_spatial.set_ylim(0, self.height)
        self.ax_spatial.set_aspect('equal')
        self.ax_spatial.set_title('🗺️ Ecosystem Map')
        
        # Plot food density sebagai background
        food_matrix = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                cell = environment.get_cell(x, y)
                food_matrix[x, y] = cell.food
        
        # Show food as background heatmap
        im = self.ax_spatial.imshow(food_matrix.T, 
                                   extent=[0, self.width, 0, self.height],
                                   origin='lower', cmap='YlOrBr', alpha=0.6, aspect='auto')
        
        # Plot agents
        herbivore_x = [a.x + 0.5 for a in agents if a.alive and isinstance(a, HerbivoreAgent)]
        herbivore_y = [a.y + 0.5 for a in agents if a.alive and isinstance(a, HerbivoreAgent)]
        carnivore_x = [a.x + 0.5 for a in agents if a.alive and isinstance(a, CarnivoreAgent)]
        carnivore_y = [a.y + 0.5 for a in agents if a.alive and isinstance(a, CarnivoreAgent)]
        
        # Plot herbivores as green circles
        if herbivore_x:
            self.ax_spatial.scatter(herbivore_x, herbivore_y, 
                                  c=self.colors['herbivore'], s=30, 
                                  marker='o', label='🐰 Herbivora', alpha=0.8)
        
        # Plot carnivores as red triangles
        if carnivore_x:
            self.ax_spatial.scatter(carnivore_x, carnivore_y, 
                                  c=self.colors['carnivore'], s=50, 
                                  marker='^', label='🐺 Karnivora', alpha=0.8)
        
        self.ax_spatial.legend(loc='upper right')
        self.ax_spatial.set_xlabel('X Position')
        self.ax_spatial.set_ylabel('Y Position')
    
    def _update_population_plot(self):
        """Update plot dinamika populasi"""
        self.ax_population.clear()
        
        if len(self.time_history) > 1:
            self.ax_population.plot(list(self.time_history), list(self.herbivore_history), 
                                  color=self.colors['herbivore'], linewidth=2, 
                                  label='🐰 Herbivora', marker='o', markersize=3)
            self.ax_population.plot(list(self.time_history), list(self.carnivore_history), 
                                  color=self.colors['carnivore'], linewidth=2, 
                                  label='🐺 Karnivora', marker='^', markersize=3)
        
        self.ax_population.set_title('📈 Population Dynamics')
        self.ax_population.set_xlabel('Time Steps')
        self.ax_population.set_ylabel('Population')
        self.ax_population.legend()
        self.ax_population.grid(True, alpha=0.3)
    
    def _update_environment_plot(self):
        """Update plot kondisi lingkungan"""
        self.ax_environment.clear()
        
        if len(self.time_history) > 1:
            # Temperature line
            ax_temp = self.ax_environment
            ax_temp.plot(list(self.time_history), list(self.temperature_history), 
                        color='red', linewidth=2, label='Temperature')
            ax_temp.set_ylabel('Temperature (°C)', color='red')
            ax_temp.tick_params(axis='y', labelcolor='red')
            
            # Food line (secondary y-axis)
            ax_food = ax_temp.twinx()
            ax_food.plot(list(self.time_history), list(self.food_history), 
                        color='green', linewidth=2, label='Total Food')
            ax_food.set_ylabel('Total Food', color='green')
            ax_food.tick_params(axis='y', labelcolor='green')
        
        self.ax_environment.set_title('🌡️ Environment Conditions')
        self.ax_environment.set_xlabel('Time Steps')
        self.ax_environment.grid(True, alpha=0.3)
    
    def _update_phase_plot(self):
        """Update phase plot Lotka-Volterra"""
        self.ax_phase.clear()
        
        if len(self.herbivore_history) > 5:
            # Plot trajectory
            self.ax_phase.plot(list(self.herbivore_history), list(self.carnivore_history), 
                             color='purple', linewidth=1.5, alpha=0.7)
            
            # Mark start and current position
            if len(self.herbivore_history) > 0:
                # Start point
                self.ax_phase.scatter(self.herbivore_history[0], self.carnivore_history[0], 
                                    color='green', s=100, marker='o', 
                                    label='Start', zorder=5)
                
                # Current point
                self.ax_phase.scatter(self.herbivore_history[-1], self.carnivore_history[-1], 
                                    color='red', s=100, marker='X', 
                                    label='Current', zorder=5)
        
        self.ax_phase.set_title('🔄 Phase Plot (Lotka-Volterra)')
        self.ax_phase.set_xlabel('Herbivore Population')
        self.ax_phase.set_ylabel('Carnivore Population')
        self.ax_phase.legend()
        self.ax_phase.grid(True, alpha=0.3)
    
    def _update_statistics(self, step: int, herb_count: int, carn_count: int, env_stats: Dict):
        """Update statistics text"""
        self.ax_stats.clear()
        self.ax_stats.axis('off')
        
        # Calculate ratios and trends
        ratio = carn_count / max(1, herb_count)
        
        # Trend calculation (simple)
        trend_herb = "→"
        trend_carn = "→"
        if len(self.herbivore_history) >= 2:
            if self.herbivore_history[-1] > self.herbivore_history[-2]:
                trend_herb = "↗"
            elif self.herbivore_history[-1] < self.herbivore_history[-2]:
                trend_herb = "↘"
        
        if len(self.carnivore_history) >= 2:
            if self.carnivore_history[-1] > self.carnivore_history[-2]:
                trend_carn = "↗"
            elif self.carnivore_history[-1] < self.carnivore_history[-2]:
                trend_carn = "↘"
        
        # Create statistics text
        stats_text = f"""
📊 LIVE STATISTICS

⏱️ Step: {step}

🐰 Herbivora: {herb_count} {trend_herb}
🐺 Karnivora: {carn_count} {trend_carn}

⚖️ Ratio P:M: {ratio:.3f}

🌡️ Temperature: {env_stats['avg_temperature']:.1f}°C
🍃 Total Food: {env_stats['total_food']:.0f}
💧 Avg Humidity: {env_stats['avg_humidity']:.1f}%

📈 Food Density: {env_stats['food_density']:.1f}

🎯 Status: {'🟢 Stable' if 0.1 <= ratio <= 0.3 else '🟡 Unstable'}
        """
        
        self.ax_stats.text(0.05, 0.95, stats_text, 
                          transform=self.ax_stats.transAxes,
                          fontsize=10, fontfamily='monospace',
                          verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    def show(self):
        """Tampilkan window visualisasi"""
        plt.tight_layout()
        plt.show(block=False)
        print("🎬 Real-time visualization window opened")
    
    def close(self):
        """Tutup visualisasi"""
        plt.close(self.fig)
        print("🎬 Real-time visualization closed")

def create_realtime_visualizer(width: int, height: int) -> RealTimeVisualizer:
    """
    Factory function untuk membuat real-time visualizer
    """
    return RealTimeVisualizer(width, height)
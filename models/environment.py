"""
Kelas untuk mengelola lingkungan simulasi
Implementasi rumus perubahan lingkungan: T(t) = T0 + A*sin(wt)
"""

import random
import math
from dataclasses import dataclass
from typing import List
from data.config_fixed import ENVIRONMENT_CONFIG

@dataclass
class EnvironmentCell:
    """
    Representasi satu sel dalam grid lingkungan
    """
    x: int
    y: int
    temperature: float
    humidity: float
    food: float      # Makanan untuk herbivora
    water: float     # Sumber air
    
    def __post_init__(self):
        """Validasi nilai dalam batas wajar"""
        self.temperature = max(-20, min(50, self.temperature))
        self.humidity = max(0, min(100, self.humidity))
        self.food = max(0, min(ENVIRONMENT_CONFIG['max_food_per_cell'], self.food))
        self.water = max(0, min(100, self.water))

class Environment:
    """
    Kelas utama untuk mengelola lingkungan simulasi
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.time_step = 0
        
        # Parameter lingkungan dari config
        self.base_temperature = ENVIRONMENT_CONFIG['base_temperature']
        self.base_humidity = ENVIRONMENT_CONFIG['base_humidity']
        
        # Inisialisasi grid lingkungan
        self.grid = self._create_initial_grid()
        
        print(f"🌍 Environment dibuat: {width}x{height} grid")
    
    def _create_initial_grid(self) -> List[List[EnvironmentCell]]:
        """
        Buat grid lingkungan awal dengan variasi acak
        """
        grid = []
        
        for x in range(self.width):
            row = []
            for y in range(self.height):
                # Variasi suhu dan kelembaban di sekitar nilai dasar
                temp = self.base_temperature + random.uniform(-3, 3)
                humidity = self.base_humidity + random.uniform(-10, 10)
                
                # Makanan awal acak
                food = random.uniform(30, 70)
                
                # Air tersedia penuh
                water = ENVIRONMENT_CONFIG['water_per_cell']
                
                cell = EnvironmentCell(x, y, temp, humidity, food, water)
                row.append(cell)
            
            grid.append(row)
        
        return grid
    
    def update(self):
        """
        Update kondisi lingkungan setiap time step
        Implementasi rumus musiman: T(t) = T0 + A * sin(ωt)
        """
        self.time_step += 1
        
        # Parameter musiman dari config
        amplitude = ENVIRONMENT_CONFIG['seasonal_amplitude']
        frequency = ENVIRONMENT_CONFIG['seasonal_frequency']
        
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                
                # Update suhu musiman: T(t) = T0 + A * sin(ωt)
                seasonal_temp = (self.base_temperature + 
                               amplitude * math.sin(frequency * self.time_step))
                
                # Tambah variasi acak kecil
                cell.temperature = seasonal_temp + random.uniform(-1.5, 1.5)
                
                # Update kelembaban dengan pola berbeda
                seasonal_humidity = (self.base_humidity + 
                                   amplitude * 0.8 * math.cos(frequency * self.time_step))
                cell.humidity = seasonal_humidity + random.uniform(-5, 5)
                
                # Pastikan dalam batas
                cell.humidity = max(0, min(100, cell.humidity))
                
                # Regenerasi makanan
                self._regenerate_food(cell)
    
    def _regenerate_food(self, cell: EnvironmentCell):
        """
        Regenerasi makanan berdasarkan kondisi lingkungan
        """
        base_regen = ENVIRONMENT_CONFIG['food_regeneration_rate']
        
        # Faktor suhu optimal (25°C)
        optimal_temp = 25.0
        temp_factor = max(0.3, 1.0 - abs(cell.temperature - optimal_temp) / 15.0)
        
        # Faktor kelembaban optimal (60%)
        optimal_humidity = 60.0
        humidity_factor = max(0.3, 1.0 - abs(cell.humidity - optimal_humidity) / 30.0)
        
        # Regenerasi dengan faktor lingkungan
        regeneration = base_regen * temp_factor * humidity_factor
        
        # Tambah variasi acak
        regeneration += random.uniform(-0.5, 1.0)
        
        # Update makanan (tidak melebihi maksimum)
        cell.food = min(ENVIRONMENT_CONFIG['max_food_per_cell'], 
                       cell.food + max(0, regeneration))
    
    def get_cell(self, x: int, y: int) -> EnvironmentCell:
        """
        Ambil sel pada koordinat tertentu
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        else:
            # Return sel default jika di luar batas
            return EnvironmentCell(x, y, self.base_temperature, 
                                 self.base_humidity, 0, 0)
    
    def get_stats(self) -> dict:
        """
        Hitung statistik lingkungan keseluruhan
        """
        total_food = 0
        total_temp = 0
        total_humidity = 0
        cell_count = self.width * self.height
        
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                total_food += cell.food
                total_temp += cell.temperature
                total_humidity += cell.humidity
        
        return {
            'time_step': self.time_step,
            'total_food': total_food,
            'avg_temperature': total_temp / cell_count,
            'avg_humidity': total_humidity / cell_count,
            'food_density': total_food / cell_count
        }
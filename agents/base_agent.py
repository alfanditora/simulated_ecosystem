"""
Implementasi agen-agen dalam simulasi ekosistem - VERSI BERSIH
Berdasarkan rumus-rumus dari PDF: reproduksi, kematian, predasi, mobilitas
Diperbaiki: Menghilangkan semua karakter Unicode dan syntax errors
"""

import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enum import Enum

class SpeciesType(Enum):
    HERBIVORE = "herbivore"
    CARNIVORE = "carnivore"
    LARGE_HERBIVORE = "large_herbivore"  # Untuk elk

class BaseAgent(ABC):
    """
    Kelas dasar untuk semua agen dalam simulasi
    """
    
    def __init__(self, agent_id: str, species_name: str, species_type: SpeciesType,
                 x: int, y: int, config: dict):
        
        # Identifikasi
        self.agent_id = agent_id
        self.species_name = species_name
        self.species_type = species_type
        
        # Posisi
        self.x = x
        self.y = y
        
        # Parameter biologis dari config
        self.reproduction_rate = config['reproduction_rate']
        self.mortality_rate = config['mortality_rate']
        self.mobility = config['mobility']
        self.metabolic_cost = config['metabolic_cost']
        
        # Toleransi lingkungan
        self.min_temp = config['min_temp']
        self.max_temp = config['max_temp']
        self.min_humidity = config['min_humidity']
        self.max_humidity = config['max_humidity']
        
        # Status agen
        self.energy = config['initial_energy']
        self.age = 0
        self.alive = True
        self.reproduction_threshold = config['reproduction_threshold']
        self.max_age = config['max_age']
        
        # Tracking
        self.total_offspring = 0
    
    def calculate_mortality_probability(self, environment_cell) -> float:
        """
        Implementasi rumus kematian dari PDF:
        P_mati = d + f_lingkungan + f_kelaparan
        """
        # Mortalitas dasar (d)
        base_mortality = self.mortality_rate
        
        # Faktor lingkungan (f_lingkungan)
        f_lingkungan = 0.0
        if (environment_cell.temperature < self.min_temp or 
            environment_cell.temperature > self.max_temp):
            f_lingkungan += 0.1
            
        if (environment_cell.humidity < self.min_humidity or 
            environment_cell.humidity > self.max_humidity):
            f_lingkungan += 0.05
        
        # Faktor kelaparan (f_kelaparan)
        f_kelaparan = 0.0
        if self.energy <= 0:
            f_kelaparan = 0.2
        elif self.energy < 30:
            f_kelaparan = 0.1
        
        # Faktor usia
        age_penalty = 0.0
        if self.age > self.max_age * 0.8:
            age_penalty = 0.02 * (self.age - self.max_age * 0.8)
        
        total_probability = base_mortality + f_lingkungan + f_kelaparan + age_penalty
        return min(1.0, total_probability)
    
    def can_reproduce(self, current_population: int, carrying_capacity: int) -> bool:
        """
        Implementasi model pertumbuhan logistik:
        Probabilitas reproduksi = r * (1 - N/K) jika energi > threshold
        """
        if self.energy < self.reproduction_threshold or not self.alive:
            return False
        
        if carrying_capacity <= 0:
            return False
        
        # Faktor carrying capacity: (1 - N/K)
        capacity_factor = max(0, 1 - (current_population / carrying_capacity))
        
        # Probabilitas reproduksi
        reproduction_prob = self.reproduction_rate * capacity_factor
        
        return random.random() < reproduction_prob
    
    @abstractmethod
    def find_optimal_position(self, environment, grid_bounds: Tuple[int, int]) -> Tuple[int, int]:
        """Cari posisi terbaik untuk bergerak"""
        pass
    
    @abstractmethod
    def update(self, environment, all_agents: List['BaseAgent']) -> None:
        """Update agen untuk satu time step"""
        pass
    
    def move_to(self, new_x: int, new_y: int, grid_bounds: Tuple[int, int]):
        """Pindahkan agen ke posisi baru"""
        max_x, max_y = grid_bounds
        self.x = max(0, min(max_x - 1, new_x))
        self.y = max(0, min(max_y - 1, new_y))
    
    def age_one_step(self):
        """Tambah usia dan kurangi energi metabolik"""
        self.age += 1
        self.energy = max(0, self.energy - self.metabolic_cost)
    
    def die(self):
        """Tandai agen sebagai mati"""
        self.alive = False
    
    def __str__(self):
        return f"{self.species_name}({self.agent_id}) at ({self.x},{self.y}) - Energy: {self.energy:.1f}"


class HerbivoreAgent(BaseAgent):
    """
    Agen herbivora (pemakan tumbuhan)
    Implementasi rumus konsumsi makanan dari PDF
    """
    
    def __init__(self, agent_id: str, x: int, y: int, config: dict = None):
        if config is None:
            from .config_helper import get_herbivore_config
            config = get_herbivore_config()
        
        super().__init__(agent_id, config['species_name'], SpeciesType.HERBIVORE, x, y, config)
        self.consumption_rate = config['consumption_rate']
        self.foraging_efficiency = config.get('foraging_efficiency', 0.8)
    
    def find_optimal_position(self, environment, grid_bounds: Tuple[int, int]) -> Tuple[int, int]:
        """
        Implementasi mobilitas agen dari PDF:
        Move to = arg max [Makanan(x,y) - Jarak(x,y)]
        """
        max_x, max_y = grid_bounds
        best_score = float('-inf')
        best_position = (self.x, self.y)
        
        # Cek semua posisi dalam radius mobilitas
        for dx in range(-self.mobility, self.mobility + 1):
            for dy in range(-self.mobility, self.mobility + 1):
                new_x = max(0, min(max_x - 1, self.x + dx))
                new_y = max(0, min(max_y - 1, self.y + dy))
                
                cell = environment.get_cell(new_x, new_y)
                distance = abs(dx) + abs(dy)  # Manhattan distance
                
                # Heuristik: makanan - biaya jarak
                score = cell.food * 2.0 - distance * 1.0
                
                # Bonus untuk kondisi lingkungan yang sesuai
                if (self.min_temp <= cell.temperature <= self.max_temp and
                    self.min_humidity <= cell.humidity <= self.max_humidity):
                    score += 10.0
                
                if score > best_score:
                    best_score = score
                    best_position = (new_x, new_y)
        
        return best_position
    
    def forage(self, environment_cell) -> float:
        """
        Implementasi rumus konsumsi makanan:
        Energi_baru = Energi_lama + Asupan Makanan - Kebutuhan Energi
        """
        available_food = environment_cell.food
        
        if available_food <= 0:
            return 0.0
        
        # Konsumsi berdasarkan efisiensi dan kebutuhan
        desired_consumption = min(self.consumption_rate, available_food)
        actual_consumption = desired_consumption * self.foraging_efficiency
        
        # Faktor lingkungan mempengaruhi efisiensi
        if (self.min_temp <= environment_cell.temperature <= self.max_temp and
            self.min_humidity <= environment_cell.humidity <= self.max_humidity):
            actual_consumption *= 1.2  # Bonus kondisi ideal
        else:
            actual_consumption *= 0.7  # Penalti kondisi buruk
        
        # Pastikan tidak melebihi yang tersedia
        actual_consumption = min(actual_consumption, available_food)
        
        # Kurangi makanan dari lingkungan
        environment_cell.food -= actual_consumption
        
        return actual_consumption
    
    def update(self, environment, all_agents: List['BaseAgent']) -> None:
        """
        Update herbivora untuk satu time step
        """
        if not self.alive:
            return
        
        # 1. Tambah usia
        self.age_one_step()
        
        # 2. Cari posisi optimal dan pindah
        grid_bounds = (environment.width, environment.height)
        optimal_pos = self.find_optimal_position(environment, grid_bounds)
        self.move_to(optimal_pos[0], optimal_pos[1], grid_bounds)
        
        # 3. Makan
        current_cell = environment.get_cell(self.x, self.y)
        food_consumed = self.forage(current_cell)
        self.energy += food_consumed
        
        # 4. Cek kematian
        mortality_prob = self.calculate_mortality_probability(current_cell)
        if random.random() < mortality_prob:
            self.die()
    
    def create_offspring(self, offspring_id: str) -> 'HerbivoreAgent':
        """Buat keturunan herbivora"""
        if self.energy >= self.reproduction_threshold:
            # Kurangi energi induk
            self.energy -= self.reproduction_threshold * 0.3
            self.total_offspring += 1
            
            # Posisi keturunan di sekitar induk
            offspring_x = self.x + random.randint(-1, 1)
            offspring_y = self.y + random.randint(-1, 1)
            
            return HerbivoreAgent(offspring_id, offspring_x, offspring_y)
        
        return None


class ElkAgent(BaseAgent):
    """
    Agen elk (herbivora besar)
    Berdasarkan data Yellowstone - mangsa utama serigala
    """
    
    def __init__(self, agent_id: str, x: int, y: int, config: dict = None):
        if config is None:
            from .config_helper import get_elk_config
            config = get_elk_config()
        
        super().__init__(agent_id, config['species_name'], SpeciesType.LARGE_HERBIVORE, x, y, config)
        self.consumption_rate = config['consumption_rate']
        self.foraging_efficiency = config.get('foraging_efficiency', 0.9)
        self.herd_size = config.get('herd_size', 5)  # Elk hidup dalam kelompok
        self.defense_strength = config.get('defense_strength', 0.4)  # Bisa melawan predator
    
    def find_optimal_position(self, environment, grid_bounds: Tuple[int, int]) -> Tuple[int, int]:
        """
        Elk mencari area dengan makanan melimpah dan aman dari predator
        """
        max_x, max_y = grid_bounds
        best_score = float('-inf')
        best_position = (self.x, self.y)
        
        # Cek semua posisi dalam radius mobilitas
        for dx in range(-self.mobility, self.mobility + 1):
            for dy in range(-self.mobility, self.mobility + 1):
                new_x = max(0, min(max_x - 1, self.x + dx))
                new_y = max(0, min(max_y - 1, self.y + dy))
                
                cell = environment.get_cell(new_x, new_y)
                distance = abs(dx) + abs(dy)
                
                # Elk butuh makanan banyak karena ukuran besar
                score = cell.food * 3.0 - distance * 1.5
                
                # Bonus untuk kondisi lingkungan yang sesuai
                if (self.min_temp <= cell.temperature <= self.max_temp and
                    self.min_humidity <= cell.humidity <= self.max_humidity):
                    score += 15.0
                
                # Bonus untuk area terbuka (elk suka grassland)
                if cell.food > 50:  # Area dengan banyak rumput
                    score += 20.0
                
                if score > best_score:
                    best_score = score
                    best_position = (new_x, new_y)
        
        return best_position
    
    def forage(self, environment_cell) -> float:
        """
        Elk makan rumput dengan konsumsi yang lebih besar dari kelinci
        """
        available_food = environment_cell.food
        
        if available_food <= 0:
            return 0.0
        
        # Elk konsumsi lebih banyak karena ukuran besar
        desired_consumption = min(self.consumption_rate, available_food)
        actual_consumption = desired_consumption * self.foraging_efficiency
        
        # Faktor lingkungan
        if (self.min_temp <= environment_cell.temperature <= self.max_temp and
            self.min_humidity <= environment_cell.humidity <= self.max_humidity):
            actual_consumption *= 1.3  # Bonus lebih besar
        else:
            actual_consumption *= 0.6  # Penalti lebih besar
        
        # Pastikan tidak melebihi yang tersedia
        actual_consumption = min(actual_consumption, available_food)
        
        # Kurangi makanan dari lingkungan
        environment_cell.food -= actual_consumption
        
        return actual_consumption
    
    def check_predator_nearby(self, all_agents: List[BaseAgent]) -> bool:
        """
        Cek apakah ada predator di sekitar untuk flee response
        """
        for agent in all_agents:
            if (agent.alive and 
                agent.species_type == SpeciesType.CARNIVORE):
                distance = abs(agent.x - self.x) + abs(agent.y - self.y)
                if distance <= 3:  # Detect predator dalam radius 3
                    return True
        return False
    
    def defend_against_predator(self) -> float:
        """
        Elk bisa melawan predator dengan kekuatan tertentu
        Returns: defensive bonus yang mengurangi predation success
        """
        base_defense = self.defense_strength
        
        # Defense lebih kuat jika energi tinggi
        energy_factor = min(1.5, self.energy / 100.0)
        
        # Defense lebih kuat jika ada elk lain nearby (herd effect)
        # Ini akan dicek oleh predator saat attempt_hunt
        
        return base_defense * energy_factor
    
    def update(self, environment, all_agents: List['BaseAgent']) -> None:
        """
        Update elk untuk satu time step
        """
        if not self.alive:
            return
        
        # 1. Tambah usia
        self.age_one_step()
        
        # 2. Cek predator dan flee jika perlu
        predator_nearby = self.check_predator_nearby(all_agents)
        
        if predator_nearby:
            # Flee behavior - cari posisi terjauh dari predator
            self._flee_from_predators(environment, all_agents)
        else:
            # Normal foraging behavior
            grid_bounds = (environment.width, environment.height)
            optimal_pos = self.find_optimal_position(environment, grid_bounds)
            self.move_to(optimal_pos[0], optimal_pos[1], grid_bounds)
        
        # 3. Makan
        current_cell = environment.get_cell(self.x, self.y)
        food_consumed = self.forage(current_cell)
        self.energy += food_consumed
        
        # 4. Cek kematian
        mortality_prob = self.calculate_mortality_probability(current_cell)
        if random.random() < mortality_prob:
            self.die()
    
    def _flee_from_predators(self, environment, all_agents: List[BaseAgent]):
        """
        Flee behavior - lari dari predator
        """
        grid_bounds = (environment.width, environment.height)
        max_x, max_y = grid_bounds
        
        # Cari posisi terjauh dari semua predator
        best_score = float('-inf')
        best_position = (self.x, self.y)
        
        for dx in range(-self.mobility, self.mobility + 1):
            for dy in range(-self.mobility, self.mobility + 1):
                new_x = max(0, min(max_x - 1, self.x + dx))
                new_y = max(0, min(max_y - 1, self.y + dy))
                
                # Hitung jarak total dari semua predator
                total_predator_distance = 0
                for agent in all_agents:
                    if (agent.alive and agent.species_type == SpeciesType.CARNIVORE):
                        pred_distance = abs(agent.x - new_x) + abs(agent.y - new_y)
                        total_predator_distance += pred_distance
                
                # Skor berdasarkan jarak dari predator
                score = total_predator_distance
                
                if score > best_score:
                    best_score = score
                    best_position = (new_x, new_y)
        
        self.move_to(best_position[0], best_position[1], grid_bounds)
    
    def create_offspring(self, offspring_id: str) -> 'ElkAgent':
        """Buat keturunan elk"""
        if self.energy >= self.reproduction_threshold:
            # Kurangi energi induk
            self.energy -= self.reproduction_threshold * 0.35
            self.total_offspring += 1
            
            # Posisi keturunan di sekitar induk
            offspring_x = self.x + random.randint(-1, 1)
            offspring_y = self.y + random.randint(-1, 1)
            
            return ElkAgent(offspring_id, offspring_x, offspring_y)
        
        return None


class CarnivoreAgent(BaseAgent):
    """
    Agen karnivora (predator)
    Implementasi model Lotka-Volterra dari PDF - VERSI DIPERBAIKI
    """
    
    def __init__(self, agent_id: str, x: int, y: int, config: dict = None):
        if config is None:
            from .config_helper import get_carnivore_config
            config = get_carnivore_config()
        
        super().__init__(agent_id, config['species_name'], SpeciesType.CARNIVORE, x, y, config)
        
        # Parameter predasi dari Lotka-Volterra - DIPERBAIKI
        self.predation_rate = config['predation_rate']        # DIPERBAIKI: 0.15 instead of 0.3
        self.conversion_efficiency = config['conversion_efficiency']  # DIPERBAIKI: 0.75 instead of 0.6
        self.hunt_range = config['hunt_range']
        self.energy_per_kill = config['energy_per_kill']      # DIPERBAIKI: 40.0 instead of 60.0
        self.hunting_cost = config['hunting_cost']            # DIPERBAIKI: 4.0 instead of 10.0
        
        # PARAMETER BARU UNTUK STABILITAS
        self.pack_hunting_bonus = config.get('pack_hunting_bonus', 1.8)
        self.starvation_tolerance = config.get('starvation_tolerance', 12)
        self.hunt_cooldown = config.get('hunt_cooldown', 1)
        self.territorial_range = config.get('territorial_range', 5)
        
        # Tracking
        self.total_kills = 0
        self.days_without_kill = 0
        self.last_hunt_day = -1  # Untuk cooldown mechanism
    
    def find_optimal_position(self, environment, grid_bounds: Tuple[int, int]) -> Tuple[int, int]:
        """
        Karnivora mencari posisi strategis untuk berburu
        """
        max_x, max_y = grid_bounds
        best_score = float('-inf')
        best_position = (self.x, self.y)
        
        for dx in range(-self.mobility, self.mobility + 1):
            for dy in range(-self.mobility, self.mobility + 1):
                new_x = max(0, min(max_x - 1, self.x + dx))
                new_y = max(0, min(max_y - 1, self.y + dy))
                
                cell = environment.get_cell(new_x, new_y)
                distance = abs(dx) + abs(dy)
                
                # Karnivora tertarik area dengan makanan (menarik herbivora)
                score = cell.food * 0.5 - distance * 1.0
                
                # Bonus kondisi lingkungan yang sesuai
                if (self.min_temp <= cell.temperature <= self.max_temp and
                    self.min_humidity <= cell.humidity <= self.max_humidity):
                    score += 8.0
                
                if score > best_score:
                    best_score = score
                    best_position = (new_x, new_y)
        
        return best_position
    
    def scan_for_prey(self, all_agents: List[BaseAgent]) -> List[BaseAgent]:
        """
        Scan area untuk mencari mangsa dalam radius berburu
        Termasuk kelinci dan elk
        """
        prey_list = []
        
        for agent in all_agents:
            if (agent.alive and 
                (agent.species_type == SpeciesType.HERBIVORE or 
                 agent.species_type == SpeciesType.LARGE_HERBIVORE) and
                agent != self):
                
                # Cek jarak
                distance = abs(agent.x - self.x) + abs(agent.y - self.y)
                
                if distance <= self.hunt_range:
                    prey_list.append(agent)
        
        return prey_list
    
    def select_preferred_target(self, available_prey: List[BaseAgent]) -> BaseAgent:
        """
        Pilih target berdasarkan preferensi predator
        Berdasarkan data Yellowstone: Serigala lebih suka elk daripada kelinci
        """
        if not available_prey:
            return None
        
        # Pisahkan berdasarkan jenis
        elk_prey = [p for p in available_prey if p.species_type == SpeciesType.LARGE_HERBIVORE]
        rabbit_prey = [p for p in available_prey if p.species_type == SpeciesType.HERBIVORE]
        
        # Preferensi: 70% elk, 30% rabbit (sesuai data Yellowstone diet)
        if elk_prey and random.random() < 0.7:
            return random.choice(elk_prey)
        elif rabbit_prey:
            return random.choice(rabbit_prey)
        elif elk_prey:
            return random.choice(elk_prey)
        else:
            return None
    
    def attempt_hunt(self, target: BaseAgent, all_agents: List[BaseAgent] = None) -> bool:
        """
        Implementasi berburu berdasarkan model Lotka-Volterra yang diperbaiki
        Berbeda untuk elk vs kelinci
        """
        if not target or not target.alive:
            return False
        
        # Hitung probabilitas sukses berburu berdasarkan jenis mangsa
        if target.species_type == SpeciesType.LARGE_HERBIVORE:
            # Elk - lebih sulit diburu tapi memberikan energi lebih banyak
            base_success = 0.25  # Lebih rendah dari kelinci
            energy_reward = self.energy_per_kill * 2.5  # Elk memberikan 2.5x energi
            
            # Elk bisa melawan balik
            if hasattr(target, 'defend_against_predator'):
                elk_defense = target.defend_against_predator()
                base_success *= (1.0 - elk_defense)  # Defense mengurangi success rate
        else:
            # Kelinci - lebih mudah diburu
            base_success = 0.4
            energy_reward = self.energy_per_kill
        
        # Faktor kondisi predator
        predator_condition = min(1.5, self.energy / 80.0)
        
        # Faktor kondisi mangsa (yang lemah lebih mudah)
        prey_condition = max(0.3, 1.0 - (target.energy / 100.0))
        
        # Pack hunting bonus - lebih penting untuk elk
        pack_bonus = 1.0
        if all_agents:
            nearby_carnivores = self._count_nearby_carnivores(all_agents)
            if nearby_carnivores > 0:
                if target.species_type == SpeciesType.LARGE_HERBIVORE:
                    # Pack hunting sangat penting untuk elk
                    pack_bonus = min(2.5, 1.0 + nearby_carnivores * 0.5)  # Max 2.5x bonus
                else:
                    # Pack hunting kurang penting untuk kelinci
                    pack_bonus = min(1.8, 1.0 + nearby_carnivores * 0.3)  # Max 1.8x bonus
        
        # Probabilitas sukses total
        success_prob = base_success * predator_condition * prey_condition * self.predation_rate * pack_bonus
        success_prob = min(0.9, success_prob)  # Cap maksimum 90%
        
        # Hunting cost - lebih mahal untuk elk
        hunting_cost = self.hunting_cost
        if target.species_type == SpeciesType.LARGE_HERBIVORE:
            hunting_cost *= 1.5  # 50% lebih mahal berburu elk
        
        self.energy = max(0, self.energy - hunting_cost)
        
        # Coba berburu
        if random.random() < success_prob:
            # Berburu berhasil!
            self.total_kills += 1
            self.days_without_kill = 0
            
            # Energy gain berdasarkan jenis mangsa
            energy_gained = energy_reward * self.conversion_efficiency
            self.energy += energy_gained
            
            # Kill the prey
            target.die()
            
            return True
        else:
            # Berburu gagal
            self.days_without_kill += 1
            return False
    
    def _count_nearby_carnivores(self, all_agents: List[BaseAgent]) -> int:
        """
        Hitung jumlah karnivora lain di sekitar untuk pack hunting bonus
        """
        count = 0
        for agent in all_agents:
            if (agent != self and 
                hasattr(agent, 'species_type') and 
                agent.species_type == SpeciesType.CARNIVORE and
                agent.alive):
                distance = abs(agent.x - self.x) + abs(agent.y - self.y)
                if distance <= 3:  # Dalam radius pack
                    count += 1
        return count
    
    def can_survive_starvation(self) -> bool:
        """
        Toleransi kelaparan berdasarkan data biologis
        Serigala bisa bertahan 12 hari tanpa makan
        """
        return self.days_without_kill <= self.starvation_tolerance
    
    def update(self, environment, all_agents: List['BaseAgent']) -> None:
        """
        Update karnivora untuk satu time step - VERSI DIPERBAIKI
        """
        if not self.alive:
            return
        
        # 1. Tambah usia
        self.age_one_step()
        
        # 2. Cek starvation tolerance sebelum hunt
        if not self.can_survive_starvation():
            # Jika sudah melewati batas toleransi kelaparan, tingkatkan mortalitas
            additional_mortality = 0.1 * (self.days_without_kill - self.starvation_tolerance)
            if random.random() < additional_mortality:
                self.die()
                return
        
        # 3. Scan untuk mangsa
        available_prey = self.scan_for_prey(all_agents)
        
        if available_prey and self.energy > 20:  # Hanya berburu jika punya energi cukup
            # Ada mangsa, pilih target berdasarkan preferensi
            target = self.select_preferred_target(available_prey)
            
            if target:
                hunt_success = self.attempt_hunt(target, all_agents)
                
                if not hunt_success:
                    # Jika gagal, coba pindah lebih dekat ke target
                    if abs(target.x - self.x) <= self.mobility and abs(target.y - self.y) <= self.mobility:
                        grid_bounds = (environment.width, environment.height)
                        self.move_to(target.x, target.y, grid_bounds)
        else:
            # Tidak ada mangsa atau energi rendah, cari posisi strategis
            grid_bounds = (environment.width, environment.height)
            optimal_pos = self.find_optimal_position(environment, grid_bounds)
            self.move_to(optimal_pos[0], optimal_pos[1], grid_bounds)
        
        # 4. Mortalitas dengan starvation tolerance
        current_cell = environment.get_cell(self.x, self.y)
        mortality_prob = self.calculate_mortality_probability(current_cell)
        
        # Penalti kelaparan hanya setelah melewati toleransi
        if self.days_without_kill > self.starvation_tolerance:
            starvation_penalty = 0.05 * (self.days_without_kill - self.starvation_tolerance)
            mortality_prob += starvation_penalty
        
        if random.random() < mortality_prob:
            self.die()
    
    def create_offspring(self, offspring_id: str) -> 'CarnivoreAgent':
        """Buat keturunan karnivora"""
        if self.energy >= self.reproduction_threshold:
            # Kurangi energi induk
            self.energy -= self.reproduction_threshold * 0.4
            self.total_offspring += 1
            
            # Posisi keturunan di sekitar induk
            offspring_x = self.x + random.randint(-1, 1)
            offspring_y = self.y + random.randint(-1, 1)
            
            return CarnivoreAgent(offspring_id, offspring_x, offspring_y)
        
        return None
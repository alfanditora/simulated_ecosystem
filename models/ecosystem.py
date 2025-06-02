"""
Engine utama simulasi ekosistem - VERSI LENGKAP
Koordinasi semua komponen dengan support untuk kelinci, elk, dan serigala
Implementasi algoritma simulasi berdasarkan rumus PDF
"""

from typing import List, Dict, Any
from .environment import Environment
from data.config_fixed import SIMULATION_CONFIG

class EcosystemSimulation:
    """
    Kelas utama untuk menjalankan simulasi ekosistem
    Support untuk 3 spesies: kelinci (herbivora), elk (herbivora besar), serigala (karnivora)
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.time_step = 0
        self.carrying_capacity = SIMULATION_CONFIG['carrying_capacity']
        
        # Inisialisasi lingkungan dengan food zones
        self.environment = Environment(width, height)
        
        # Daftar semua agen (kelinci, elk, serigala)
        self.agents: List[Any] = []
        
        # Data untuk analisis - ditambah elk tracking
        self.population_history = {
            'herbivore': [],      # Kelinci
            'elk': [],            # Elk
            'carnivore': [],      # Serigala
            'total_food': [],
            'avg_temperature': []
        }
        
        # Counter untuk ID unik
        self.agent_counter = 0
        
        print(f"🦎 EcosystemSimulation initialized: {width}x{height} dengan 3 spesies")
    
    def setup_species(self):
        """
        Setup populasi awal semua spesies: kelinci, elk, dan serigala
        """
        # Import di dalam function untuk menghindari circular import
        from agents.config_helper import get_herbivore_config, get_carnivore_config, get_elk_config
        
        # Tambah herbivora kecil (kelinci)
        herbivore_config = get_herbivore_config()
        herbivore_count = herbivore_config['initial_population']
        for _ in range(herbivore_count):
            self._create_herbivore()
        
        # Tambah herbivora besar (elk)
        elk_config = get_elk_config()
        elk_count = elk_config['initial_population']
        for _ in range(elk_count):
            self._create_elk()
        
        # Tambah karnivora (serigala)
        carnivore_config = get_carnivore_config()
        carnivore_count = carnivore_config['initial_population']
        for _ in range(carnivore_count):
            self._create_carnivore()
        
        print(f"🐰 Kelinci awal: {herbivore_count}")
        print(f"🦌 Elk awal: {elk_count}")
        print(f"🐺 Serigala awal: {carnivore_count}")
        print(f"📊 Total agen: {len(self.agents)}")
        
        # Info habitat zones
        print(f"🌍 Habitat zones: River Valley (center), Grassland (middle), Mountain (edge)")
    
    def _create_herbivore(self):
        """
        Buat herbivora (kelinci) baru di posisi acak
        """
        import random
        from agents.base_agent import HerbivoreAgent
        
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        agent_id = f"H_{self.agent_counter}"
        self.agent_counter += 1
        
        herbivore = HerbivoreAgent(agent_id, x, y)
        self.agents.append(herbivore)
        return herbivore
    
    def _create_elk(self):
        """
        Buat elk baru di posisi acak
        """
        import random
        from agents.base_agent import ElkAgent
        
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        agent_id = f"E_{self.agent_counter}"
        self.agent_counter += 1
        
        elk = ElkAgent(agent_id, x, y)
        self.agents.append(elk)
        return elk
    
    def _create_carnivore(self):
        """
        Buat karnivora (serigala) baru di posisi acak
        """
        import random
        from agents.base_agent import CarnivoreAgent
        
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        agent_id = f"C_{self.agent_counter}"
        self.agent_counter += 1
        
        carnivore = CarnivoreAgent(agent_id, x, y)
        self.agents.append(carnivore)
        return carnivore
    
    def step(self):
        """
        Satu langkah simulasi - implementasi algoritma dari flowchart PDF
        Dengan support untuk elk dan food zones
        """
        self.time_step += 1
        
        # 1. Update lingkungan (termasuk seasonal changes dan food regeneration)
        self.environment.update()
        
        # 2. Update semua agen (kelinci, elk, serigala)
        alive_agents = [agent for agent in self.agents if agent.alive]
        
        for agent in alive_agents:
            agent.update(self.environment, self.agents)
        
        # 3. Proses reproduksi untuk semua spesies
        self._process_reproduction()
        
        # 4. Hapus agen yang mati
        self.agents = [agent for agent in self.agents if agent.alive]
        
        # 5. Catat statistik untuk semua spesies
        self._record_statistics()
    
    def _process_reproduction(self):
        """
        Proses reproduksi berdasarkan model logistik untuk semua spesies
        """
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent, ElkAgent
        
        # Hitung populasi saat ini per spesies
        herbivore_count = len([a for a in self.agents if a.alive and isinstance(a, HerbivoreAgent)])
        elk_count = len([a for a in self.agents if a.alive and isinstance(a, ElkAgent)])
        carnivore_count = len([a for a in self.agents if a.alive and isinstance(a, CarnivoreAgent)])
        
        new_agents = []
        
        # Proses reproduksi herbivora (kelinci)
        for agent in self.agents:
            if (agent.alive and isinstance(agent, HerbivoreAgent) and
                agent.can_reproduce(herbivore_count, self.carrying_capacity)):
                
                offspring = agent.create_offspring(f"H_{self.agent_counter}")
                if offspring:
                    offspring.x = max(0, min(self.width - 1, offspring.x))
                    offspring.y = max(0, min(self.height - 1, offspring.y))
                    new_agents.append(offspring)
                    self.agent_counter += 1
        
        # Proses reproduksi elk (carrying capacity berdasarkan ratio Yellowstone)
        elk_capacity = max(30, self.carrying_capacity // 7)  # Berdasarkan ratio Yellowstone: ~1:7
        for agent in self.agents:
            if (agent.alive and isinstance(agent, ElkAgent) and
                agent.can_reproduce(elk_count, elk_capacity)):
                
                offspring = agent.create_offspring(f"E_{self.agent_counter}")
                if offspring:
                    offspring.x = max(0, min(self.width - 1, offspring.x))
                    offspring.y = max(0, min(self.height - 1, offspring.y))
                    new_agents.append(offspring)
                    self.agent_counter += 1
        
        # Proses reproduksi karnivora (serigala)
        carnivore_capacity = max(15, self.carrying_capacity // 13)  # Berdasarkan ratio Yellowstone: ~1:13
        for agent in self.agents:
            if (agent.alive and isinstance(agent, CarnivoreAgent) and
                agent.can_reproduce(carnivore_count, carnivore_capacity)):
                
                offspring = agent.create_offspring(f"C_{self.agent_counter}")
                if offspring:
                    offspring.x = max(0, min(self.width - 1, offspring.x))
                    offspring.y = max(0, min(self.height - 1, offspring.y))
                    new_agents.append(offspring)
                    self.agent_counter += 1
        
        # Tambahkan agen baru
        self.agents.extend(new_agents)
        
        if new_agents:
            herb_births = len([a for a in new_agents if isinstance(a, HerbivoreAgent)])
            elk_births = len([a for a in new_agents if isinstance(a, ElkAgent)])
            carn_births = len([a for a in new_agents if isinstance(a, CarnivoreAgent)])
            
            print(f"  🍼 Kelahiran: {herb_births} kelinci, {elk_births} elk, {carn_births} serigala")
    
    def _record_statistics(self):
        """
        Catat statistik populasi dan lingkungan untuk semua spesies
        """
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent, ElkAgent
        
        # Hitung populasi
        herbivore_count = len([a for a in self.agents if a.alive and isinstance(a, HerbivoreAgent)])
        elk_count = len([a for a in self.agents if a.alive and isinstance(a, ElkAgent)])
        carnivore_count = len([a for a in self.agents if a.alive and isinstance(a, CarnivoreAgent)])
        
        # Statistik lingkungan
        env_stats = self.environment.get_stats()
        
        # Simpan ke history
        self.population_history['herbivore'].append(herbivore_count)
        self.population_history['elk'].append(elk_count)
        self.population_history['carnivore'].append(carnivore_count)
        self.population_history['total_food'].append(env_stats['total_food'])
        self.population_history['avg_temperature'].append(env_stats['avg_temperature'])
    
    def run(self, steps: int, realtime_vis: bool = False):
        """
        Jalankan simulasi untuk sejumlah langkah dengan support elk
        """
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent, ElkAgent
        
        print(f"🚀 Memulai simulasi untuk {steps} langkah...")
        if realtime_vis:
            print("🎬 Real-time visualization enabled")
        print("-" * 50)
        
        # Setup real-time visualizer jika diminta
        visualizer = None
        if realtime_vis:
            try:
                from visualization.realtime import create_realtime_visualizer
                visualizer = create_realtime_visualizer(self.width, self.height)
                visualizer.show()
            except ImportError as e:
                print(f"⚠️  Real-time visualization tidak tersedia: {e}")
                realtime_vis = False
        
        for step in range(steps):
            self.step()
            
            # Update real-time visualization
            if realtime_vis and visualizer:
                env_stats = self.environment.get_stats()
                visualizer.update_data(step, self.agents, self.environment, env_stats)
            
            # Tampilkan progress
            if step % SIMULATION_CONFIG['show_progress_every'] == 0:
                self._show_progress(step)
            
            # Cek kondisi berhenti (kepunahan)
            herbivore_count = len([a for a in self.agents if a.alive and isinstance(a, HerbivoreAgent)])
            elk_count = len([a for a in self.agents if a.alive and isinstance(a, ElkAgent)])
            carnivore_count = len([a for a in self.agents if a.alive and isinstance(a, CarnivoreAgent)])
            
            # Kondisi berhenti: semua herbivora punah ATAU semua karnivora punah
            total_prey = herbivore_count + elk_count
            if total_prey == 0:
                print(f"\n⚠️  Simulasi dihentikan pada langkah {step}: Semua herbivora punah!")
                break
            elif carnivore_count == 0:
                print(f"\n⚠️  Simulasi dihentikan pada langkah {step}: Karnivora punah!")
                break
        
        # Tutup visualizer
        if visualizer:
            print("\n🎬 Tekan Enter untuk menutup real-time visualization...")
            input()
            visualizer.close()
        
        print(f"\n✅ Simulasi selesai pada langkah {self.time_step}")
    
    def _show_progress(self, step: int):
        """
        Tampilkan progress simulasi dengan semua spesies
        """
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent, ElkAgent
        
        herbivore_count = len([a for a in self.agents if a.alive and isinstance(a, HerbivoreAgent)])
        elk_count = len([a for a in self.agents if a.alive and isinstance(a, ElkAgent)])
        carnivore_count = len([a for a in self.agents if a.alive and isinstance(a, CarnivoreAgent)])
        env_stats = self.environment.get_stats()
        
        print(f"Langkah {step:3d}: "
              f"🐰 {herbivore_count:2d} | "
              f"🦌 {elk_count:2d} | "
              f"🐺 {carnivore_count:2d} | "
              f"🌡️  {env_stats['avg_temperature']:5.1f}°C | "
              f"🍃 {env_stats['total_food']:6.0f}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Hitung statistik analisis ekosistem untuk semua spesies
        """
        if len(self.population_history['herbivore']) < 10:
            return {"error": "Data tidak cukup untuk analisis"}
        
        import numpy as np
        
        # Stabilitas populasi (standard deviation)
        herb_stability = np.std(self.population_history['herbivore'][-100:])
        elk_stability = np.std(self.population_history['elk'][-100:])
        carn_stability = np.std(self.population_history['carnivore'][-100:])
        
        # Keseimbangan predator-mangsa (total prey vs predator)
        recent_herbs = np.mean(self.population_history['herbivore'][-50:])
        recent_elk = np.mean(self.population_history['elk'][-50:])
        recent_carns = np.mean(self.population_history['carnivore'][-50:])
        
        total_prey = recent_herbs + recent_elk
        predator_prey_ratio = recent_carns / max(1, total_prey)
        
        # Yellowstone-style ratios
        wolf_elk_ratio = recent_carns / max(1, recent_elk)
        
        return {
            'total_steps': self.time_step,
            'final_herbivores': recent_herbs,
            'final_elk': recent_elk,
            'final_carnivores': recent_carns,
            'total_prey': total_prey,
            'herbivore_stability': herb_stability,
            'elk_stability': elk_stability,
            'carnivore_stability': carn_stability,
            'predator_prey_ratio': predator_prey_ratio,
            'wolf_elk_ratio': wolf_elk_ratio,  # Yellowstone comparison
            'population_history': self.population_history.copy()
        }
    
    def show_results(self):
        """
        Tampilkan hasil akhir simulasi dengan analisis untuk semua spesies
        """
        stats = self.get_statistics()
        
        if "error" in stats:
            print(f"❌ {stats['error']}")
            return
        
        print("\n" + "=" * 60)
        print("📊 HASIL ANALISIS EKOSISTEM 3-SPESIES")
        print("=" * 60)
        print(f"⏱️  Total langkah simulasi: {stats['total_steps']}")
        print(f"🐰 Populasi akhir kelinci: {stats['final_herbivores']:.0f}")
        print(f"🦌 Populasi akhir elk: {stats['final_elk']:.0f}")
        print(f"🐺 Populasi akhir serigala: {stats['final_carnivores']:.0f}")
        print(f"🍽️  Total mangsa: {stats['total_prey']:.0f}")
        
        print(f"\n📈 Stabilitas (Standard Deviation):")
        print(f"   • Kelinci: {stats['herbivore_stability']:.2f}")
        print(f"   • Elk: {stats['elk_stability']:.2f}")
        print(f"   • Serigala: {stats['carnivore_stability']:.2f}")
        
        print(f"\n⚖️  Rasio Ekosistem:")
        print(f"   • Predator:Total Mangsa = {stats['predator_prey_ratio']:.3f}")
        print(f"   • Serigala:Elk = {stats['wolf_elk_ratio']:.3f} (Yellowstone: ~0.013)")
        
        # Evaluasi stabilitas berdasarkan semua spesies
        stable_species = 0
        if stats['herbivore_stability'] < 10:
            stable_species += 1
        if stats['elk_stability'] < 8:
            stable_species += 1
        if stats['carnivore_stability'] < 5:
            stable_species += 1
        
        print(f"\n🎯 Evaluasi Ekosistem:")
        if stable_species == 3:
            print("✅ Ekosistem SANGAT STABIL (semua spesies stabil)")
        elif stable_species == 2:
            print("✅ Ekosistem STABIL (mayoritas spesies stabil)")
        elif stable_species == 1:
            print("⚠️  Ekosistem CUKUP STABIL (beberapa spesies stabil)")
        else:
            print("❌ Ekosistem TIDAK STABIL (fluktuasi tinggi)")
        
        # Validasi dengan data Yellowstone
        yellowstone_valid = (0.005 <= stats['wolf_elk_ratio'] <= 0.020)
        print(f"\n🏔️  Validasi Yellowstone:")
        if yellowstone_valid:
            print("✅ Rasio serigala:elk sesuai data Yellowstone")
        else:
            print("⚠️  Rasio serigala:elk di luar range Yellowstone")
        
        print("=" * 60)
    
    def get_habitat_analysis(self) -> Dict[str, Any]:
        """
        Analisis distribusi agen berdasarkan habitat zones
        """
        from agents.base_agent import HerbivoreAgent, CarnivoreAgent, ElkAgent
        
        # Inisialisasi counter untuk setiap zone
        zones = {'River Valley': {'kelinci': 0, 'elk': 0, 'serigala': 0},
                'Grassland': {'kelinci': 0, 'elk': 0, 'serigala': 0},
                'Mountain': {'kelinci': 0, 'elk': 0, 'serigala': 0}}
        
        # Hitung distribusi agen
        for agent in self.agents:
            if not agent.alive:
                continue
                
            zone_type = self.environment.get_area_type(agent.x, agent.y)
            
            if isinstance(agent, HerbivoreAgent):
                zones[zone_type]['kelinci'] += 1
            elif isinstance(agent, ElkAgent):
                zones[zone_type]['elk'] += 1
            elif isinstance(agent, CarnivoreAgent):
                zones[zone_type]['serigala'] += 1
        
        return zones
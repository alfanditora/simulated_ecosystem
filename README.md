# 🌱 Simulasi Ekosistem - Agent Based Model

Simulasi ekosistem berbasis komputer yang menggambarkan interaksi antara herbivora dan karnivora dalam lingkungan buatan. Implementasi berdasarkan rumus-rumus ekologi klasik.

## 📋 Implementasi Rumus Ekologi

### 1. **Reproduksi Spesies (Pertumbuhan Logistik)**
```
dN/dt = rN(1 - N/K)
```
- N: populasi saat ini
- r: laju reproduksi intrinsik
- K: carrying capacity lingkungan

### 2. **Kematian Spesies**
```
P_mati = d + f_lingkungan + f_kelaparan
```
- d: probabilitas kematian alami
- f_lingkungan: penalti kondisi lingkungan buruk
- f_kelaparan: penalti energi rendah

### 3. **Predasi (Model Lotka-Volterra)**
```
dN/dt = rN - aNP  (mangsa)
dP/dt = baNP - mP (predator)
```
- a: laju predasi
- b: efisiensi konversi mangsa menjadi predator
- m: laju kematian predator

### 4. **Perubahan Lingkungan Musiman**
```
T(t) = T0 + A × sin(ωt)
```
- T0: suhu rata-rata
- A: amplitudo variasi musiman
- ω: frekuensi musiman

### 5. **Mobilitas Agen**
```
Move to = arg max [Makanan(x,y) - Jarak(x,y)]
```
Heuristik untuk mencari posisi optimal berdasarkan ketersediaan makanan dan biaya pergerakan.

## 🗂️ Struktur Proyek

```
ecosystem_simulation/
├── agents/
│   ├── __init__.py
│   └── base_agent.py          # Implementasi agen herbivora & karnivora
├── data/
│   ├── __init__.py
│   └── config.py              # Konfigurasi parameter simulasi
├── models/
│   ├── __init__.py
│   ├── environment.py         # Manajemen lingkungan dan sel
│   └── ecosystem.py           # Engine utama simulasi
├── visualization/
│   ├── __init__.py
│   └── plots.py               # Visualisasi dan analisis hasil
├── README.md                  # Dokumentasi ini
├── requirements.txt           # Dependencies
└── run.py                     # File utama untuk menjalankan simulasi
```

## 🚀 Cara Menjalankan

### 1. **Instalasi Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Jalankan Simulasi**
```bash
python run.py
```

### 3. **Output yang Dihasilkan**
- Progress simulasi real-time di terminal
- Analisis statistik ekosistem
- Grafik dinamika populasi (Lotka-Volterra)
- Metrik stabilitas dan keseimbangan
- Interpretasi hasil otomatis

## 📊 Metrik Evaluasi

### **Stabilitas Populasi**
- Standard deviation populasi (target: < 10 untuk stabil)
- Rolling window analysis untuk trend

### **Keseimbangan Ekosistem**
- Rasio predator:mangsa yang konstan
- Phase plot Lotka-Volterra

### **Validitas Biologis**
- Kesesuaian dengan teori ekologi klasik
- Kurva yang mengikuti pola Lotka-Volterra

### **Efisiensi Komputasi**
- Optimisasi untuk grid 30x30 dengan 500 langkah
- Monitoring memory usage dan performance

## ⚙️ Konfigurasi Parameter

Edit file `data/config.py` untuk mengubah parameter:

### **Simulasi Umum**
```python
SIMULATION_CONFIG = {
    'grid_width': 30,           # Lebar grid
    'grid_height': 30,          # Tinggi grid  
    'max_steps': 500,           # Langkah maksimum
    'carrying_capacity': 200,    # Kapasitas dukung
}
```

### **Herbivora (Kelinci)**
```python
HERBIVORE_CONFIG = {
    'reproduction_rate': 0.3,   # r dalam rumus logistik
    'mortality_rate': 0.05,     # d dalam rumus kematian
    'consumption_rate': 15.0,   # Konsumsi makanan per step
    'mobility': 2,              # Jarak maksimum bergerak
    # ... parameter lainnya
}
```

### **Karnivora (Serigala)**
```python
CARNIVORE_CONFIG = {
    'predation_rate': 0.3,      # a dalam Lotka-Volterra
    'conversion_efficiency': 0.6, # b dalam Lotka-Volterra
    'hunt_range': 2,            # Radius berburu
    # ... parameter lainnya
}
```

## 📈 Contoh Output

```
🌱 SIMULASI EKOSISTEM - AGENT BASED MODEL
============================================================
📋 Implementasi rumus dari PDF:
   • Reproduksi: dN/dt = rN(1-N/K)
   • Kematian: P_mati = d + f_lingkungan + f_kelaparan
   • Predasi: Model Lotka-Volterra
   • Lingkungan: T(t) = T0 + A*sin(ωt)

🚀 Menjalankan simulasi...
Langkah   0: 🐰  50 | 🐺 10 | 🌡️  25.2°C | 🍃   1847
Langkah  50: 🐰  67 | 🐺 12 | 🌡️  27.8°C | 🍃   1923
Langkah 100: 🐰  73 | 🐺 15 | 🌡️  24.1°C | 🍃   1756
...

📊 HASIL ANALISIS EKOSISTEM
============================================================
⏱️  Total langkah simulasi: 500
🐰 Populasi akhir herbivora: 68
🐺 Populasi akhir karnivora: 14
📈 Stabilitas herbivora (std): 8.45
📈 Stabilitas karnivora (std): 3.21
⚖️  Rasio predator:mangsa: 0.206
✅ Ekosistem STABIL
```

## 🎨 Visualisasi

Simulasi menghasilkan 3 jenis grafik:

1. **Dinamika Populasi**: Timeline dan phase plot Lotka-Volterra
2. **Metrik Ekosistem**: Stabilitas, rasio, distribusi, kondisi lingkungan
3. **Analisis Ringkasan**: Bar charts dan interpretasi status

## 🔬 Validasi Ilmiah

### **Referensi Teori**
- Hukum Lotka-Volterra untuk dinamika predator-mangsa
- Model pertumbuhan logistik Verhulst
- Konsep carrying capacity dan regulasi populasi
- Pengaruh faktor lingkungan terhadap mortalitas

### **Dataset Referensi**
- Global Biodiversity Information Facility (GBIF)
- National Ecological Observatory Network (NEON)
- Knowledge Network for Biocomplexity (KNB)

## 🎯 Potensi Penggunaan

### **Edukasi**
- Demonstrasi konsep ekologi
- Pembelajaran interaktif dinamika populasi
- Visualisasi teori Lotka-Volterra

### **Penelitian**
- Analisis skenario "what-if"
- Pengembangan strategi konservasi
- Studi dampak perubahan lingkungan

### **Simulasi Kebijakan**
- Evaluasi dampak aktivitas manusia
- Perencanaan manajemen ekosistem
- Prediksi risiko kepunahan

## 🛠️ Pengembangan Lanjutan

### **Fitur yang Dapat Ditambahkan**
- Spesies omnivora (pemakan segala)
- Migrasi musiman agen
- Bencana alam (kebakaran, banjir)
- Mutasi genetik dan evolusi
- Interface GUI interaktif

### **Optimisasi**
- Parallel processing untuk grid besar
- Database storage untuk simulasi panjang
- Web interface untuk akses remote
- Export data untuk analisis eksternal

## 📞 Kontak & Kontribusi

Proyek ini dikembangkan sebagai implementasi tugas ekologi computational biology. 

**Tim Pengembang:**
- 18222037 Alfandito Rais Akbar
- 18222045 Givari Al Fachri  
- 18222097 Muhammad Nurul Hakim

---

*Simulasi ini mengimplementasikan rumus-rumus ekologi klasik dalam bentuk Agent-Based Model untuk memahami dinamika ekosistem secara komputasional.*
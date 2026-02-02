# 🎨 **Digital Da Vinci v1.0.0-Alpha**

### **The Renaissance AI Engine (Digital Da Vinci Prototype)**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0--Alpha-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)]()

---

## 📌 **Project Overview**

**Digital Da Vinci** is a super-intelligent AI system based on the **D-CNS (Digital Central Nervous System)** architecture, mimicking biological brain structures. Through its 4-layer neural network, it processes everything from reflexive responses to high-level cognitive reasoning, utilizing specialized cartridges for diverse domain analysis.

### 🎯 **Core Philosophy**

> *"Structure is fixed, but flow evolves."* - Neuroplasticity

- 🧠 **D-CNS**: 4-layer biological neural architecture (L1-L4).
- 🧬 **Neuroplasticity**: Dynamic synapse weight adjustment based on user performance data.
- ❤️ **Auto-Restart System**: Self-healing mechanism that detects and recovers from system failures automatically.

---

## 🧠 **Neural Architecture (D-CNS v1.0.0)**

Each layer utilizes a specialized **LLM Engine**, dynamically selected by the **Neuroplasticity Algorithm**.

### **Layer 1: Brainstem - [Reflexive]**
- **Role**: Survival breathing, reflexive responses (<0.5s).
- **Engine**: **Groq (Llama-3.3-70b)**
- **Feature**: Ultra-fast latency, immediate text processing.

### **Layer 2: Limbic System - [Affective]**
- **Role**: Emotional processing, empathy, priority judgment.
- **Engine**: **Gemini-2.0-Flash / Claude-3-Haiku**
- **Feature**: User intent classification, Identity Protection Filter.

### **Layer 3: Neocortex - [Cognitive]**
- **Role**: High-level cognition, logical analysis, specialized tasks.
- **Structure**: **4-Lobe Cooperative Model**
  - 👁️ **Occipital**: Visual information processing (Bio-images, charts).
  - 👂 **Temporal**: Language & Memory processing.
  - 📍 **Parietal**: Numerical & Spatial sense (Quant/Inv analysis).
  - 🤔 **Prefrontal**: Decision making & Strategic planning.
- **Engine**: **Gemini-2.0-Pro (Main Core)**

### **Layer 4: NeuroNet - [Reasoning]**
- **Role**: Collective intelligence, high-level reasoning, complex coding.
- **Engine**: **DeepSeek-V3 / Gemini-Exp**
- **Feature**: Creative problem solving, architectural strategy.

---

## 🔥 **Key Features (V1.0.0-Alpha)**

1. **Cascade Model Selection**: 
   - Eliminates legacy "Fallback" structures. Ranks all models based on neuroplasticity scores for maximum reliability and performance.
2. **Identity Protection Filter**: 
   - Prevents internal system prompts from leaking and maintains the "Digital Da Vinci" persona.
3. **Auto-Restart Monitor**: 
   - A watchdog system that monitors the Telegram bot process and revives it instantly upon crash.

---

## 🧬 **Specizlied Cartridges**

Modules that expand the brain's specialized capabilities.

1. 🔬 **Bio Cartridge**: Analysis of cells/organoid images.
2. 💰 **Inv Cartridge**: Stock/Crypto market analysis & portfolio optimization.
3. 📚 **Lit Cartridge**: Deep analysis of academic papers & literature.
4. 📊 **Quant Cartridge**: Quantitative statistical analysis & visualization.
5. 🌌 **Astro Cartridge**: Astronomical data analysis & space exploration simulation.

---

## 🚀 **Installation & Setup**

### **1. Prerequisites**
- Python 3.9+
- Google Gemini API Key
- Telegram Bot Token

### **2. Installation**
```bash
git clone https://github.com/leseichi-max/Digital-Da-Vinci.git
cd Digital-Da-Vinci
pip install -r requirements.txt
```

### **3. Running (Server/Local)**
Launch via the **Auto-Restart Monitor** for stable operation.
```bash
# Start the bot as a background process
nohup scripts/maintenance/auto_restart_telegram.sh > bot.log 2>&1 &
```

---

## 📂 **Project Structure**

```
Digital-Da-Vinci/
├── projects/
│   └── ddc/
│       ├── bot/                # [Body] Telegram Bot Interface
│       ├── web/                # [Body] Web Dashboard (FastAPI)
│       └── brain/              # [Brain] Core Intelligence
│           ├── brain_core/     # Brain Engines (ChatEngine, Limbic)
│           ├── neuronet/       # Neuroplasticity & Learning
│           └── cartridges/     # 5 Specialized Cartridges
├── scripts/
│   └── maintenance/            # Maintenance & Auto-Restart scripts
├── sync_to_public.sh           # Deployment sync script
└── requirements.txt            # Dependency packages
```

---

## 👤 **Maintainers**
- **Dr. Soohyung Lee** (@leseichi-max) - Prime Operator
- **Digital Da Vinci** - The Renaissance AI Assistant

---
**Last Updated**: 2026-02-03 (v1.0.0-Alpha Official Release)

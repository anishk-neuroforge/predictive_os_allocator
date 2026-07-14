# 🎮 Predictive OS Resource Allocator

A real-time **Machine Learning-based Operating System resource monitoring and allocation system** that predicts CPU, memory, and disk utilization and generates dynamic resource management decisions.

Developed as an Operating Systems and Machine Learning project, it combines **system monitoring, predictive analytics, resource allocation logic, and real-time data visualization** in an interactive desktop dashboard.

---

## 🖥️ Demo Dashboard

<!-- Add your dashboard screenshot inside the assets folder as dashboard.png -->

![Predictive OS Resource Allocator Dashboard](OSDEMO.png)

---

## 🔍 Project Overview

Traditional resource monitoring systems primarily react to system load after resource usage changes.

The **Predictive OS Resource Allocator** explores a predictive approach to resource management.

The application continuously collects live system telemetry, processes system metrics using Machine Learning models, predicts future resource utilization, and generates dynamic resource allocation decisions.

The system:

- 📊 Monitors CPU, memory, disk, network, and process activity in real time
- 🧠 Predicts CPU, memory, and disk resource utilization using Machine Learning
- ⚙️ Generates dynamic resource allocation decisions
- 📈 Compares predicted CPU utilization with actual system usage
- 💾 Visualizes real-time memory distribution
- 🔄 Monitors active processes and their resource consumption
- 🖥️ Displays system metrics through an interactive desktop dashboard

The complete pipeline follows:

```text
System Telemetry
       ↓
Feature Collection
       ↓
Machine Learning Prediction
       ↓
Resource Allocation Decision
       ↓
Real-Time Dashboard
```

---

## 🛠️ Features

### 🧠 Machine Learning Resource Prediction

Predicts future system resource utilization based on live operating system telemetry.

The prediction system estimates:

- CPU utilization
- Memory utilization
- Disk utilization

### 🎛️ Dynamic Resource Allocation

The allocation engine analyzes system metrics and predicted resource usage to generate dynamic resource-management decisions.

Example decisions include:

- Maintain Current Allocation
- Reduce Disk I/O
- Optimize Memory Usage
- Adjust Resource Priority

### 📊 Real-Time GUI Dashboard

The application includes a modern dark-themed desktop dashboard built using **CustomTkinter**.

The dashboard displays:

- Live process queue
- CPU utilization
- Real-time CPU usage graph
- Memory distribution
- Predicted vs actual CPU utilization
- AI scheduler decisions
- Active process count
- Predicted memory utilization
- Predicted disk utilization

### ⚙️ Live System Monitoring

The application continuously collects operating system statistics using `psutil`.

Monitored system metrics include:

- CPU usage
- Memory usage
- Available memory
- Swap utilization
- Disk utilization
- Disk read activity
- Disk write activity
- Network bytes sent
- Network bytes received
- Active process count
- System load averages

### 📈 Predicted vs Actual Resource Usage

The dashboard provides real-time visualization of:

- Actual CPU utilization
- Predicted CPU utilization

This makes it possible to observe Machine Learning predictions alongside real system behavior.

### 🔄 Process Queue Monitoring

The application dynamically monitors active system processes and displays:

- Process ID (PID)
- Process name
- Process state
- CPU utilization
- Memory consumption

---

## 💻 Technologies Used

1. **Python 3.x** — Core application development
2. **CustomTkinter** — Modern desktop GUI
3. **Matplotlib** — Real-time data visualization
4. **psutil** — Operating system telemetry collection
5. **Scikit-learn** — Machine Learning models and prediction
6. **Pandas** — Dataset processing and manipulation
7. **NumPy** — Numerical computation

---

## 📁 Folder Structure

```text
predictive_os_allocator/
│
├── main.py
│   └── Application entry point
│
├── gui.py
│   └── Real-time monitoring dashboard
│
├── monitor.py
│   └── System telemetry collection
│
├── predictor.py
│   └── Machine Learning prediction logic
│
├── allocator.py
│   └── Resource allocation decision engine
│
├── utils.py
│   └── Utility functions
│
├── dataset.csv
│   └── System resource utilization dataset
│
├── requirements.txt
│   └── Project dependencies
│
├── assets/
│   └── dashboard.png
│
└── README.md
```

Each module is separated to maintain a clear and modular project architecture.

---

## ⚙️ How It Works

### 1️⃣ System Monitoring

The application continuously collects live operating system statistics using `psutil`.

```text
CPU Usage
Memory Usage
Swap Usage
Disk Activity
Network Activity
Process Count
System Load
```

### 2️⃣ Feature Collection

The collected system statistics are transformed into numerical features for the Machine Learning prediction pipeline.

### 3️⃣ Resource Prediction

The Machine Learning models analyze the system features and predict:

```text
Predicted CPU Usage
Predicted Memory Usage
Predicted Disk Usage
```

### 4️⃣ Resource Allocation Decision

The allocation engine analyzes system conditions and generates a dynamic resource management recommendation.

### 5️⃣ Real-Time Visualization

The results are continuously displayed through the interactive dashboard.

```text
Live System Metrics
        +
ML Resource Predictions
        +
Allocation Decisions
        ↓
Real-Time Dashboard
```

---

## 🧠 Machine Learning Pipeline

The prediction system processes multiple system-level features:

```text
Memory Utilization
Available Memory
Swap Utilization
Disk Utilization
Disk Read Activity
Disk Write Activity
Network Bytes Sent
Network Bytes Received
Process Count
1-Minute System Load
5-Minute System Load
15-Minute System Load
```

These features are used to estimate future system resource utilization.

```text
System Features
       ↓
Machine Learning Models
       ↓
CPU Prediction
Memory Prediction
Disk Prediction
       ↓
Resource Allocation Engine
       ↓
Dynamic Scheduling Decision
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/anishk-neuroforge/predictive_os_allocator.git
cd predictive_os_allocator
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 3️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python main.py
```

The **Predictive OS Resource Allocator Dashboard** will launch and begin monitoring system resources.

---

## 🎯 Project Objectives

The primary objectives of this project are to:

- Explore predictive resource management concepts
- Apply Machine Learning to operating system telemetry
- Understand CPU, memory, disk, and process monitoring
- Develop a modular Python application
- Integrate ML models with real-time system data
- Build an interactive system monitoring dashboard
- Visualize predicted and actual resource utilization

---

## 🔮 Future Improvements

- ⚡ Implement background threads for smoother real-time monitoring
- 🧠 Experiment with advanced time-series prediction models
- 📊 Add model evaluation metrics such as MAE, RMSE, and R²
- 🔍 Implement system resource anomaly detection
- 📈 Add historical resource usage analytics
- 💾 Store monitoring history in a database
- 📄 Export system reports to CSV and PDF
- 🎛️ Add configurable monitoring intervals
- 🖥️ Improve cross-platform system monitoring
- 🔄 Add process-level resource prediction
- 📉 Compare reactive and predictive resource allocation strategies
- 🧪 Add automated testing for prediction and allocation modules

---

## ⚠️ Project Scope

This project is an educational and experimental implementation of predictive resource management.

The application operates at the **user/application level** and does not replace or directly modify the kernel-level operating system scheduler.

Its purpose is to explore how Machine Learning, system telemetry, and predictive analytics can be integrated to support intelligent resource-management decisions.

---

## 🤝 Contribution

Contributions, suggestions, and improvements are welcome.

For major changes, please open an issue first to discuss the proposed improvements.

You can also:

- Fork the repository
- Create a new feature branch
- Implement your changes
- Submit a pull request

---

## ✨ About

The **Predictive OS Resource Allocator** combines concepts from:

- 🖥️ Operating Systems
- 🧠 Machine Learning
- 📊 Data Visualization
- ⚙️ System Monitoring
- 🐍 Python Development

It collects real-time operating system telemetry, predicts future CPU, memory, and disk utilization, generates dynamic resource-management decisions, and visualizes the complete pipeline through an interactive desktop dashboard.

The project demonstrates how **Machine Learning and Operating Systems concepts can be integrated into a practical end-to-end application**.

---

## 👨‍💻 Author

**Anish K**

B.Tech Computer Science Engineering  
Artificial Intelligence & Machine Learning

---

⭐ If you found this project useful or interesting, consider starring the repository.

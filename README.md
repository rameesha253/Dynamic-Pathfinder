# 🚀 **Dynamic Pathfinding Agent**
*A Real-Time, Grid-Based Pathfinding Simulator with Dynamic Obstacles & Smart Re-planning*

---

## 🎯 **Project Overview**
This project is a **real-time, interactive pathfinding simulator** that visualizes and compares the performance of **Greedy Best-First Search (GBFS)** and **A* Search** algorithms. It features **dynamic obstacle spawning**, **automatic re-planning**, and **interactive map editing**, making it perfect for learning and experimenting with informed search algorithms.

---

## 🧠 **Implemented Algorithms**

### **1️⃣ Greedy Best-First Search (GBFS)**
- **Formula:** `f(n) = h(n)`
- **Pros:** Blazing fast, great for quick pathfinding
- **Cons:** Not always optimal, can get stuck in local minima
- **Heuristics:** Manhattan & Euclidean

### **2️⃣ A-star Search**
- **Formula:** `f(n) = g(n) + h(n)`
- **Pros:** Guaranteed optimal path with admissible heuristics, efficient node expansion
- **Cons:** Slightly slower than GBFS due to cost calculation
- **Heuristics:** Manhattan & Euclidean

---

## ✨ **Key Features**


Features


| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| **Dynamic Grid Sizing**     | Adjust grid size on the fly for different scenarios                        |
| **Interactive Map Editor**  | Draw, erase, and modify obstacles in real-time                             |
| **Random Obstacle Generator** | Spawn random obstacles for unpredictable pathfinding challenges           |
| **Dynamic Obstacle Spawning** | Obstacles can appear/disappear during runtime, forcing re-planning         |
| **Automatic Re-planning**   | Algorithm recalculates path instantly when obstacles change                |
| **Visualization**           | See frontier, visited nodes, and final path in different colors            |
| **Real-Time Metrics**       | Track nodes visited, path cost, and execution time                         |

---

## 📊 **Performance Metrics**
- **Nodes Visited:** See how many nodes each algorithm explores
- **Path Cost:** Compare the efficiency of GBFS vs. A*
- **Execution Time:** Measure how fast each algorithm finds a path (in milliseconds)

---

## 💡 **Why This Project?**
- **Learn Informed Search:** Understand how heuristics guide search algorithms
- **Compare Algorithms:** See the trade-offs between speed and optimality
- **Dynamic Environments:** Experiment with real-time changes and re-planning
- **Visual Learning:** Watch algorithms in action with colorful visualizations

---

## 🏆 **Pros & Conclusions**

Here’s the "Pros" section formatted as bullet points for your README file:

---

### **Pros**
- **Educational:** Perfect for students and enthusiasts to visualize pathfinding algorithms in action
- **Interactive:** Real-time grid editing and dynamic obstacle spawning make learning engaging and fun
- **Comparative:** Easily compare the performance and behavior of GBFS and A* side by side
- **No Dependencies:** Runs with pure Python—no external libraries required, making setup hassle-free

---

### **Conclusions**
- **A* is optimal** but slower due to cost calculations
- **GBFS is fast** but can miss the shortest path
- **Dynamic re-planning** is crucial for real-world applications (e.g., robotics, game AI)
- **Heuristic choice matters:** Manhattan vs. Euclidean can change path shape and efficiency

---

## 🛠 **How to Run**
1. **Install Python 3.x**
2. **Run the script:**
   ```bash
   python dynamic-pathfinder.py
   ```
3. **Interact with the grid:**
   - Click to add/remove obstacles
   - Watch the algorithm adapt in real-time!

---

## 📌 **Future Improvements**
- Add more algorithms (Dijkstra, D*, JPS)
- Implement 3D pathfinding
- Save/load custom maps
- Multi-agent pathfinding

---

## 📢 **Call to Action**
**Try it out, tweak the code, and see how pathfinding algorithms tackle dynamic challenges!**
*Perfect for projects, learning, or just having fun with AI.*

---

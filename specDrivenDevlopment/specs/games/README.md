# 🧱 3D Block World – Spec-Driven Development README

## 1. Purpose

Build a **minimal 3D block world** in which:
- A player character can **move around freely**
- The world is composed of **axis-aligned cube blocks**
- Rendering happens in the **browser**
- The system is **extensible** toward a Minecraft-like experience

This is **not** a full game.  
This is a **foundational 3D sandbox** with movement, blocks, and camera control.

---

## 2. Non-Goals (Out of Scope)

The first implementation **must not** include:
- Multiplayer
- Persistence / saving
- Crafting systems
- Complex physics
- Advanced lighting or shaders
- Procedural terrain generation beyond flat or simple noise

---

## 3. Technology Stack (Mandatory Choices)

### 3.1 Runtime
- **Language**: JavaScript (ES2020+)
- **Platform**: Browser (Chrome-compatible)

### 3.2 Rendering
- **Three.js** (mandatory)

### 3.3 Physics & Collision
- Manual AABB collision detection
- Gravity and jumping handled numerically

### 3.4 Controls
- Pointer Lock API for mouse look
- WASD keyboard movement

---

## 4. High-Level Architecture

src/
 ├── index.html
 ├── main.js
 ├── engine/
 │    ├── Renderer.js
 │    ├── Scene.js
 │    ├── GameLoop.js
 ├── world/
 │    ├── World.js
 │    ├── Chunk.js
 │    ├── Block.js
 ├── player/
 │    ├── Player.js
 │    ├── CameraController.js
 │    ├── InputController.js
 └── utils/
      ├── Math.js
      ├── Constants.js

---

## 5. Core Concepts & Definitions

### 5.1 World Coordinate System
- Right-handed coordinate system
- 1 unit = 1 block

---

## 6. Player Specification

- First-person camera
- Player height: 1.8 units
- Gravity: ~9.8 units/s²
- Movement speed: 5 units/s

---

## 7. Game Loop

Uses requestAnimationFrame:
1. Handle input
2. Update physics
3. Resolve collisions
4. Render scene

---

## 8. Acceptance Criteria

- Player can move with WASD
- Mouse controls camera
- Player cannot fall through ground
- Blocks align to grid
- Runs at ~60 FPS

---

## 9. AI Agent Instructions

Follow this spec literally.
Do not invent features.
Prefer clarity over cleverness.

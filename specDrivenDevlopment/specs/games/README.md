# 3D world with character spec

This document is a **build spec** intended for an AI coding agent to recreate the project behavior of **dgreenheck/minecraft-threejs-clone**: a browser-based Minecraft-like voxel game built with Three.js, featuring procedural world generation, biomes, resources, chunked terrain, terraforming, and save/load. citeturn1view0turn4search4

> Target outcome: running `npm install && npm run dev` launches a local dev server with a playable first‑person voxel world, matching the gameplay loop and controls described below. Make sure the working directory is clear.

---

## 0) Source-of-truth behaviors (must match)

### 0.1 Controls (must)
From the live demo UI:
- **WASD**: move
- **SHIFT**: sprint
- **SPACE**: jump
- **R**: reset camera
- **U**: toggle UI
- **0**: pickaxe (remove blocks mode)
- **1–8**: select block type for placement
- **F1**: save game
- **F2**: load game
- **F10**: debug camera (free/fly camera) citeturn4search4

### 0.2 Core feature set (must)
The recreated project MUST include:
- Procedural world generation
- Biomes
- Resources: **Coal** and **Iron**
- Terrain chunking (infinite / streamed or at least large world by chunk)
- Terraforming (add/remove blocks)
- Save/load citeturn1view0turn4search4

### 0.3 Build tooling (must)
Repository is a JavaScript project and includes `package.json`, `vite.config.js`, `index.html`, `style.css`, `scripts/`, and `public/`. The spec below assumes **Vite** + **Three.js** as the primary stack. citeturn1view0
Build it using Typescript

---

## 1) Product requirements

### 1.1 Player experience
When the app loads:
1. Show a simple title screen overlay: “PRESS ANY KEY TO START”.
2. On key press:
   - request pointer lock (mouse look)
   - begin rendering loop
   - hide title overlay and show HUD (unless toggled off) citeturn4search4

The player spawns on/near terrain surface and can:
- walk/sprint/jump with basic physics and collision against voxel terrain
- look around with mouse (first-person)
- place blocks (selected by 1–8)
- break blocks (pickaxe = key 0)
- the player should have an axe held in a hand
- create a hand holding a wooden stick
- at the top of the stick is a green blocky blade
- when clicking in pickaxe mode, the axe should strike the block using a movement
- make sure the hand and the axe are clearly visible. so they can be drawn at a distance

### 1.2 World
World is a voxel grid represented as chunks (see §3).
- World should appear “Minecraft-like”: rolling hills, varied terrain heights, and block layers.
- Biomes impact surface blocks/colors/types (e.g., grass vs sand vs snow—exact palette is flexible, but biome variation must be visible).
- Coal and iron appear embedded in stone underground as resource blocks.

### 1.3 Terraforming
Player can:
- remove a targeted block if within reach using the axe
- place a block on a face adjacent to a targeted block (if empty)
Constraints:
- Placement cannot intersect the player’s bounding volume
- Max reach distance (suggested 5–7 blocks)

### 1.4 Save / Load
- **Save (F1)** persists the player state + world edits (not necessarily full regenerated base terrain) locally.
- **Load (F2)** restores player state + edits.
Implementation guidance: localStorage is acceptable; compression optional.

### 1.5 UI
HUD must at least include:
- crosshair (center)
- selected block indicator (1–8 + pickaxe)
- instructions panel (toggle with U) listing controls above

---

## 2) Non-goals (explicitly out of scope)
- Inventory management, crafting, item drops, NPCs (these appear on the repo TODO list). citeturn1view0
- Multiplayer/network sync
- Custom shaders / advanced rendering tricks (goal is educational/simple). citeturn1view0

---

## 3) Technical design

### 3.1 High-level architecture
Implement a minimal module layout under `scripts/` (names flexible, responsibilities not):

- `main.js` (entry): bootstraps renderer, scene, camera, game loop
- `world/World.js`: world orchestration, chunk grid management, streaming
- `world/Chunk.js`: stores voxel data + mesh generation
- `world/generation/*`: noise + biome selection + resource placement
- `player/Player.js`: controls, physics, collision
- `ui/*`: HUD + overlays
- `persistence/saveLoad.js`: save/load state

The public folder should include static assets (textures/fonts), but the build must not depend on proprietary assets.

### 3.2 Data model

#### 3.2.1 Block IDs
Use integer IDs:
- 0: Air
- 1: Grass
- 2: Dirt
- 3: Stone
- 4: Sand (or biome surface alt)
- 5: Wood/Log (optional)
- 6: Leaves (optional)
- 7: Coal Ore
- 8: Iron Ore

Only **Coal** and **Iron** are required as “resources” (7 and 8). citeturn1view0

#### 3.2.2 Chunk
- Chunk dimensions: `CHUNK_SIZE = 16` (x,z), `CHUNK_HEIGHT = 128` (y) — adjustable.
- Store blocks in a typed array for speed:
  - `Uint8Array(CHUNK_SIZE * CHUNK_HEIGHT * CHUNK_SIZE)`
- Indexing:
  - `idx(x,y,z) = x + CHUNK_SIZE * (z + CHUNK_SIZE * y)`

#### 3.2.3 World coordinates
- World is an infinite (or large) grid of chunks in XZ plane.
- Chunk coordinate:
  - `cx = floor(wx / CHUNK_SIZE)`, `cz = floor(wz / CHUNK_SIZE)`
- Local coordinate:
  - `lx = mod(wx, CHUNK_SIZE)` etc.

### 3.3 Procedural generation

#### 3.3.1 Noise
Use a deterministic noise function with a seed:
- Perlin/Simplex noise for heightmap + biome
- Keep seed in state (for save/load reproducibility)

Generate:
- `height(wx,wz) = base + amplitude * fBm(noise)`
- Clamp to `[0, CHUNK_HEIGHT-1]`

#### 3.3.2 Biomes
Biome selection based on low-frequency noise (temperature/moisture) or a single biome noise:
- Example biomes:
  - Plains: grass/dirt
  - Desert: sand
  - Snow: snow surface (or light grass)
Acceptance requirement:
- At least **2 distinct biome surface looks** visible while walking around.

#### 3.3.3 Block layering
For each `(wx,wz)` column:
- `y == height`: surface block depends on biome
- `y in (height-1 .. height-4)`: dirt (or sand)
- `y < height-4`: stone
- below y=0: air (or bedrock optional)

#### 3.3.4 Resource placement
Within stone region:
- Coal: common, small clusters
- Iron: less common, small clusters
Approach:
- For each voxel in stone, sample a higher-frequency noise; threshold into ore.
- Or place N veins per chunk using random walk with seeded RNG.

### 3.4 Meshing strategy (performance-critical)
Requirement: chunking + meshing must support a playable framerate at a modest view distance.

Minimum acceptable:
- One `THREE.Mesh` per chunk using `BufferGeometry`
- Only create faces that are adjacent to Air (no internal faces)
- Merge faces into a single geometry per chunk, grouped by material OR use a texture atlas to keep draw calls low.

Recommended:
- Greedy meshing (optional), but face-culling meshing is sufficient for a basic clone.

### 3.5 Rendering
- Three.js scene with:
  - Directional light + ambient light
  - Fog for distance
- Camera:
  - First-person camera attached to player
  - `R` resets camera yaw/pitch to defaults citeturn4search4

### 3.6 Player physics & collision

#### 3.6.1 Player body
- Capsule or AABB collider
- Suggested: AABB with width=0.6, height=1.8

#### 3.6.2 Movement
- Walk speed and sprint speed multiplier (SHIFT)
- Jump impulse when grounded
- Gravity constant

#### 3.6.3 Collision resolution
Voxel collision:
- Determine occupied voxels near the player AABB
- Resolve axis-by-axis:
  1. move X, resolve
  2. move Y, resolve (grounded detection)
  3. move Z, resolve

### 3.7 Interaction (raycast)
- Raycast from camera center to max distance
- Determine targeted block coordinate
- Determine hit face normal for placement

Controls:
- Left click: break (only when pickaxe selected, key 0)
- Right click: place selected block (keys 1–8) on adjacent cell

### 3.8 Save/Load format
Persist a single JSON object:
```json
{
  "version": 1,
  "seed": 12345,
  "player": { "pos":[x,y,z], "vel":[x,y,z], "yaw":0, "pitch":0, "selected": 1 },
  "edits": [
    {"x":1,"y":64,"z":2,"id":0},
    {"x":4,"y":64,"z":2,"id":7}
  ]
}
```
- `edits` stores only changes vs generated terrain.
- On load: regenerate chunks using seed, then apply edits.

---

## 4) Milestones & acceptance tests (agent checklist)

### Milestone A — Ask the user to Build & boot using the following instructions
**Done when:**
- `npm install` succeeds
- `npm run dev` serves a page with the start overlay
- pressing any key starts the game loop and pointer lock citeturn4search4

### Milestone B — First-person controller
**Done when:**
- mouse look works
- WASD moves
- SHIFT sprints
- SPACE jumps
- player collides with terrain and can’t fall through

### Milestone C — Chunked terrain
**Done when:**
- world is built from chunk meshes
- moving around loads/keeps nearby chunks (fixed radius is fine)
- framerate remains playable (target: ~60fps on a typical dev laptop at low-medium view distance)

### Milestone D — Biomes + resources
**Done when:**
- at least two surface looks exist (biomes)
- coal and iron blocks appear underground citeturn1view0

### Milestone E — Terraforming
**Done when:**
- key 0 selects pickaxe mode
- keys 1–8 select placement blocks
- blocks can be removed/placed via click with a reach limit
- chunk meshes update only for affected chunk(s)

### Milestone F — Save/Load
**Done when:**
- F1 saves
- F2 loads
- after reload (browser refresh), load restores state and edits citeturn4search4

### Milestone G — UI toggles + debug camera
**Done when:**
- U toggles the HUD
- F10 toggles a debug camera mode (free-fly with WASD + mouse) citeturn4search4

---

## 5) Repo scaffolding requirements

### 5.1 File structure (minimum)
Create/keep:
- `index.html`
- `style.css`
- `vite.config.js`
- `package.json`
- `scripts/**`
- `public/**` citeturn1view0

### 5.2 Scripts (suggested)
In `package.json`:
- `dev`: `vite`
- `build`: `vite build`
- `preview`: `vite preview`

### 5.3 Deploy (optional)
Support GitHub Pages deployment (not required for acceptance here), but keep build output compatible with static hosting.

---

## 6) Implementation notes (pragmatic choices)
- Use a deterministic RNG (seeded) so save/load can regenerate reliably.
- Keep materials simple: one material with a texture atlas, or a small set of materials by block type.
- Use instancing **only if** not meshing; meshing is preferred.
- Update meshes incrementally (dirty chunk rebuild), not every frame.

---

## 7) Reference (what we’re matching)
- Project description + feature list (procedural generation, biomes, coal/iron, chunking, terraforming, save/load). citeturn1view0
- Live demo control scheme (WASD/SHIFT/SPACE/R/U/0/1–8/F1/F2/F10). citeturn4search4
- Repo is a JS Three.js project using Vite-era structure (vite config + scripts/public folders). citeturn1view0

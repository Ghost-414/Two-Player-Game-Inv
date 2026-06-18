## 🕹️ Game Mechanics

* **Screen Divide:** Players are locked to their respective halves of the map ($1000 \times 800$ boundaries).
* **Strategic Cooldowns:** Weapon fire triggers a strict **4-second reload delay**, forcing players to aim precisely.
* **Dynamic Environment:** An AI alien ship glides along the ceiling dropping downward salvos, while a high-velocity kinetic ball bounces off the walls.

## 🛠️ Python & Pygame Implementation Details

### 1. Game Loop & Delta Time Regulation
The engine operates on a deterministic `while` loop throttled by a hardware clock wrapper. This prevents the execution speed from tying directly to the host CPU's capability.
* `clock.tick(60)` clamps the maximum frame processing rate to 60 Frames Per Second (FPS).

### 2. State Management & Resource Handling
* **Surface Rendering:** Sprite textures (`.png`) are pulled into memory as `Surface` objects and explicitly downscaled using standard matrix scaling wrappers: `pygame.transform.scale()`.
* **State Trackers:** Time-sensitive event blocks (like weapon cooldowns) leverage absolute uptime calculations:
  ```python
  # Non-blocking polling method for cooldown checks
  pygame.time.get_ticks() - last_shot_time >= shoot_cooldown

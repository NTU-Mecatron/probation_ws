# Probation Task: Autonomous Gate Navigation with Unity Simulation

This repository contains the probation task for autonomous gate navigation using ROS2 and a Unity simulation.

> **You should NOT clone this repository directly from the Mecatron GitHub organisation.**
> 
> Instead, **fork** this repository to your own GitHub account and clone from it. *(Please ask ChatGPT how to fork a github repository if you are unsure)*.
> After cloning, ensure you are on the `probation/task` branch:
> ```bash
> git checkout probation/task
> ```
> Implement your solution in this branch `probation/task` in either Python or C++ and send us the link to your forked repository once completed.

## 1. Getting Started

> We use `ROS2 Jazzy + Ubuntu 24.04` for all development. The environment is fully Dockerized (Native installation is not encouraged).

See **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** for the full step-by-step setup guide (Ubuntu 24.04 via WSL2 → Git → Docker → Build).

**Prerequisites to Download (Installed & Run on Windows Host):**
1. [**Unity Simulation**](https://github.com/NTU-Mecatron/probation_ws/releases/tag/v1.0.0) — the simulation environment (`UnitySim.exe`), downloaded and run on Windows.
2. [**Foxglove Studio**](https://foxglove.dev/download) — for monitoring vehicle state and topics visually. See **[docs/FOXGLOVE_SETUP.md](docs/FOXGLOVE_SETUP.md)** for connection and layout import instructions.

## 2. Problem Statement

**Task Goal**: Navigate an Autonomous Underwater Vehicle (AUV) through a gate in a simulated underwater environment.

**Learning Objectives**:
- Working with a robot simulator using ROS2
- Processing object detection data to extract meaningful information
- Developing autonomous decision-making and control algorithms
- Managing a project with multiple concurrent processes and nodes

**Success Criteria**:
- The vehicle navigates autonomously through the gate **3 times**, at **3 different random initial positions**.

## 3. Workspace Structure

```
probation_ws/
├── src/
│   ├── ROS-TCP-Endpoint/               # Unity-ROS2 communication bridge
│   ├── probation_bringup/              # Launch, config, and your solution scripts
│   │   ├── launch/
│   │   │   └── probation.launch.py     # <-- Main launch file for the simulation
│   │   └── scripts/
│   │       └── solution_template.py    # <-- Start here: implement your solution
│   └── vision/
│       └── vision_msgs/                # Custom message definitions for bounding boxes
```

## 4. Running the Simulation

Enter the container first (every time you open a new Ubuntu terminal):
```bash
cd ~/probation_ws
docker compose run --rm dev-core bash
```

### Step 1 — Launch the ROS2 Bridge
Inside your Docker container (or native terminal), run:
```bash
ros2 launch probation_bringup probation.launch.py
```

This starts two processes:
- **ROS-TCP-Endpoint** on port `10000` — the Unity simulation connects to this.
- **Foxglove Bridge** on port `8765` — open Foxglove Studio, connect to `ws://localhost:8765`, and import **[docs/probation_foxglove_layout.json](docs/probation_foxglove_layout.json)** (see **[docs/FOXGLOVE_SETUP.md](docs/FOXGLOVE_SETUP.md)**).

### Step 2 — Start the Unity Simulation
Launch `UnitySim.exe` on your Windows host. Once it connects, you will see topics appear in ROS2.

### Step 3 — Verify the Connection
In a second terminal inside the container:
```bash
# Check that simulation topics are visible
ros2 topic list

# Verify vehicle state is being published
ros2 topic echo /mavros/state
```

### Step 4 — Run Your Solution
Open a second Ubuntu terminal:
```bash
cd ~/probation_ws
docker compose run --rm dev-core bash
```
Then run:
```bash
ros2 run probation_bringup solution_template.py
```

> **Tip:** If you create new Python scripts in `src/probation_bringup/scripts/`, ensure they have executable permissions:
> ```bash
> chmod +x src/probation_bringup/scripts/<script_name>.py
> ```

## 5. Available Topics

Use these commands to explore any topic yourself:
```bash
ros2 topic info <topic>               # See the message type
ros2 interface show <message_type>    # See all fields of a message type
ros2 topic echo <topic>               # Print live data
```

| Topic                                         | Message Type                   | Description                                    |
| --------------------------------------------- | ------------------------------ | ---------------------------------------------- |
| `/main_camera/detection/bounding_boxes`       | `vision_msgs/BoundingBoxArray` | Gate detection from the front camera           |
| `/mavros/global_position/compass_hdg`         | `std_msgs/Float64`             | Current heading in degrees (0–360)             |
| `/mavros/global_position/rel_alt`             | `std_msgs/Float64`             | Current depth/altitude in meters               |
| `/mavros/setpoint_velocity/cmd_vel_unstamped` | `geometry_msgs/Twist`          | **Send velocity commands to move the vehicle** |
| `/mavros/state`                               | `mavros_msgs/State`            | Vehicle armed/mode status                      |

### Bounding Box Format

The camera publishes all detected objects as a [`BoundingBoxArray`](src/vision/vision_msgs/msg/BoundingBoxArray.msg). Each [`BoundingBox`](src/vision/vision_msgs/msg/BoundingBox.msg) contains:

![BoundingBox description](docs/images/bounding_box_description.png)

| Field        | Type   | Description                                                         |
| ------------ | ------ | ------------------------------------------------------------------- |
| `x`          | float  | Horizontal center (0.0 = left edge, 0.5 = center, 1.0 = right edge) |
| `y`          | float  | Vertical center (0.0 = top edge, 0.5 = center, 1.0 = bottom edge)   |
| `w`          | float  | Width of bounding box (normalized 0.0–1.0)                          |
| `h`          | float  | Height of bounding box (normalized 0.0–1.0)                         |
| `conf`       | float  | Detection confidence (0.0–1.0)                                      |
| `label_id`   | int    | Numeric class ID of the detected object                             |
| `label_name` | string | String class name of the detected object                            |

### Velocity Command Format

To move the vehicle, publish a `geometry_msgs/Twist` message:

```
linear.x  — forward (+) / backward (−)     [m/s]
linear.y  — strafe left (+) / right (−)    [m/s]
linear.z  — up (+) / down (−)              [m/s]
angular.z — yaw left/CCW (+) / right/CW (−)[rad/s]
```

## 6. Simulation Characteristics

- **Random Initial Position**: The vehicle spawns at a random location and orientation on each run.
- **Imperfect Detection**: The object detector does not detect the gate 100% of the time. Your solution should handle frames where no detection is received.
- **GUIDED Mode Required**: The vehicle must be in `GUIDED` flight mode to accept velocity commands from ROS2. Without this, all published commands are ignored.

## 7. Where to Start

Open [`src/probation_bringup/scripts/solution_template.py`](src/probation_bringup/scripts/solution_template.py).

It contains a clean ROS2 node skeleton to start building your solution.

> Reference ROS2 code examples (publishers, subscribers, clients, services) are available under [`docs/help/`](docs/help/).

**Suggested progression**:
1. Set the vehicle to `GUIDED` mode via the service client.
2. Subscribe to sensor topics and log what you receive.
3. Send a simple constant velocity and watch the vehicle move.
4. Implement closed-loop control using sensor feedback to navigate through the gate.

> Refer to [Section 8](#8-appendix) for useful commands and links.

## 8. Appendix

### 8.1 Suggested Logic

One possible approach — there are many valid solutions:

1. Set vehicle to `GUIDED` mode
2. Descend to a depth where the gate is likely visible
3. Implement a search pattern to find the gate
4. Align laterally and in heading with the gate center
5. Drive forward through the gate

### 8.2 Obstacle Avoidance Note

The gate area contains an orange flare that may appear as an obstacle. If the vehicle's initial position faces this obstacle:
- You may implement obstacle avoidance for bonus points (not required).
- Alternatively, you may reset the simulation and try a new spawn.

Focus on the gate navigation first. Obstacle avoidance is optional.

### 8.3 Useful Commands

```bash
# Check available topics and services
ros2 topic list
ros2 service list

# Inspect message types
ros2 interface show vision_msgs/msg/BoundingBox
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show mavros_msgs/srv/SetMode

# Monitor live data
ros2 topic echo /main_camera/detection/bounding_boxes
ros2 topic echo /mavros/global_position/compass_hdg
ros2 topic echo /mavros/global_position/rel_alt

# Set vehicle mode manually (useful for testing)
ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'GUIDED'}"

# Switch back to manual keyboard control
ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'ALT_HOLD'}"

# Verify your velocity commands are being published
ros2 topic echo /mavros/setpoint_velocity/cmd_vel_unstamped
ros2 topic hz /mavros/setpoint_velocity/cmd_vel_unstamped
```

### 8.4 Useful Links

- [ROS2 Jazzy Tutorials](https://docs.ros.org/en/jazzy/Tutorials.html)
- [geometry_msgs/Twist](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)
- [MAVROS Wiki](https://wiki.ros.org/mavros)

---

**Good luck!** The key is building a system that handles imperfect sensing robustly. Start simple, iterate, and test frequently.

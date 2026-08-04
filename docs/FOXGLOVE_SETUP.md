# Foxglove Studio Setup & User Guide

[Foxglove Studio](https://foxglove.dev/download) is a modern robotics visualization tool used to monitor ROS 2 topics, plot sensor data, call services, and control the vehicle in real-time.

---

## 1. Quick Beginner Guide: Using Foxglove Studio

Before importing pre-configured layouts, here is how to navigate and use Foxglove Studio:

### Connecting to ROS 2
1. Launch Foxglove Studio on your Windows host.
2. Click **Open Connection**.
3. Select **Foxglove WebSocket**.
4. Enter the WebSocket URL: `ws://localhost:8765` (or `ws://127.0.0.1:8765`).
5. Click **Open**. A green connection indicator at the top left confirms you are connected.

### Understanding Panels
Foxglove layouts are composed of modular **Panels**:
- **Raw Messages**: Inspect live topic data structures and values in real-time.
- **Plot**: Graph numerical variables over time (e.g. depth, heading, velocity).
- **Indicator**: Visual status flags (e.g. ARMED / DISARMED, Flight Mode).
- **Call Service**: Trigger ROS 2 service calls with a single click.
- **Teleop**: On-screen directional buttons to publish velocity commands manually.
- **3D**: Visualize coordinate frames (TFs) and 3D environment data.

### Handy Foxglove Tips
- **Add a Panel**: Click the `+` icon on the top bar or split any existing panel.
- **Inspect Topics**: Add a **Raw Messages** panel and type any topic name (e.g. `/mavros/state`) to view live fields.
- **Customize Layout**: Drag panel headers to split, resize, or rearrange panels.

---

## 2. Importing the Official Probation Layout

We provide a pre-configured layout tailored for the probation task containing all required plots, status indicators, service buttons, dual teleop controls, and vision detection displays.

### Step-by-Step Import Instructions:
1. Open Foxglove Studio connected to `ws://localhost:8765`.
2. Click the **Layout** menu in the top-right toolbar.
3. Select **Import layout from file...**.
4. Browse to your cloned workspace and select:
   ```text
   probation_ws/docs/probation_foxglove_layout.json
   ```
   *(Or select `Probation_Foxglove_Layout.json` from your Windows Downloads folder).*

---

## 3. What’s Included in the Probation Layout

The layout is split into tabs for easy navigation:

### AUV Monitor Tab (Right Sidebar)
- **System State & Mode Indicators**: Shows live `ARMED`/`DISARMED` status and active flight mode (`GUIDED`, `DEPTH_HOLD`, `MANUAL`).
- **Service Buttons**: Click **ARM**, **DISARM**, or **GUIDED** to trigger mode changes directly without typing terminal commands.
- **Dual Teleop Controls**:
  - **Forward & Yaw**: Controls forward/backward (`linear.x`) and turning/heading rate (`angular.z`).
  - **Up Down & Sideways**: Controls depth ascend/descend (`linear.z`) and strafing left/right (`linear.y`).

### Main Tab (Plots & Logs)
- **Depth Plot**: Graphs vehicle relative altitude/depth over time (`/mavros/global_position/rel_alt`).
- **Compass Heading Plot**: Graphs live compass heading in degrees (`/mavros/global_position/compass_hdg`).
- **Cmd Vel Plot**: Graphs velocity setpoints published by candidate nodes (`/mavros/setpoint_velocity/cmd_vel_unstamped`).
- **RosOut Console**: Displays ROS 2 node log messages (`info`, `warn`, `error`).

### Task Gate Tab
- **3D View**: Visualizes vehicle coordinate frames (TFs) and origin reference frames.
- **Camera Bounding Boxes**: Displays live numerical gate detections (`x`, `y`, `w`, `h`, `conf`, `label_name`) from `/main_camera/detection/bounding_boxes`.

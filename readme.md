# WPG 300-120 Gripper ROS2 & GRIPLINK Plugin

## Overview

The **WPG 300-120 Gripper ROS2 Package** integrates **Weiss Robotics’ WPG 300-120 gripper** with ROS2 via the **GRIPLINK-ROS2 Plugin 1.0.0**. It provides a **C++ ROS2 interface** to control the gripper and demonstrates usage through a **demo node**.

### Features

* **GRIPLINK Node**: Implements GRIPLINK  as a ROS2 node for controlling devices.

  * **Topics**: Publishes device states.
  * **Services**: Exposes GRIPLINK commands as ROS2 services.
  * **Actions**: Time-consuming commands like grip/release handled via ROS2 actions.
* **Demo Node**: Example client node demonstrating basic gripper operations: homing, gripping, and releasing.
* **Visualization Support**: Integration with WPG 300-120 URDF and RViz2.

Tested on **ROS2 Jazzy Jalisco** with **Ubuntu 24.04**.

---

## Repository Structure

# WPG 300-120 Gripper ROS2 & GRIPLINK Plugin

## Overview

The **WPG 300-120 Gripper ROS2 Package** integrates **Weiss Robotics’ WPG 300-120 gripper** with ROS2 via the **GRIPLINK-ROS2 Plugin 1.0.0**. It provides a **C++ ROS2 interface** to control the gripper and demonstrates usage through a **demo node**.  


### Features

- **GRIPLINK Node**: Implements GRIPLINK as a ROS2 node for controlling devices.
  - **Topics**: Publishes device states.
  - **Services**: Exposes GRIPLINK commands as ROS2 services.
  - **Actions**: Time-consuming commands like grip/release handled via ROS2 actions.
- **Demo Node**: Example client node demonstrating basic gripper operations: homing, gripping, and releasing.
- **Visualization Support**: Integration with WPG 300-120 URDF and RViz2.

Tested on **ROS2 Jazzy Jalisco** with **Ubuntu 24.04**.

---

## Repository Structure

```text
iai_weiss_wpg_300-120-gripper/
├── griplink/
│   ├── griplink/                   # GRIPLINK driver node
│   │   ├── include/
│   │   ├── launch/                 # Launch files for GRIPLINK node & demo
│   │   ├── package.xml
│   │   └── src/
│   ├── griplink_interfaces/        # Custom messages, services, actions
│   ├── LICENSE
│   └── README.md
├── readme.md
└── wpg_300_120_description/
    ├── CMakeLists.txt
    ├── launch/                     # Launch files for visualization & interface
    ├── meshes/                     # STL files
    ├── package.xml
    ├── rviz2/                      # RViz configuration
    └── urdf/                        # URDF and XACRO files
```
---

## Hardware Setup

### WPG-Series Grippers

Follow [WPG Series Manual](https://weiss-robotics.com/servo-electric/wpg-series/product/wpg-series/?file=files/downloads/wpg/um_wpg_series_en.pdf&cid=10276), sections 5.2.1 & 5.2.2.

---

## Installation & Build

### Prerequisites

* ROS2 Jazzy installed on Ubuntu 24.04
* GRIPLINK device supporting GRIPLINK protocol V3

### Steps

```bash
# Navigate to workspace
cd ~/ros2_ws

# Install package dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build workspace
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# Source workspace
source install/local_setup.bash
```

---

## Launching the Gripper

### Visualise WPG Robot + Gripper in RViz

```bash
ros2 launch wpg_300_120_gripper_description display.launch.py
```
### Launch with Actual Gripper

```bash
ros2 launch wpg_300_120_gripper_description gripper_interface.launch.py
```

---

## GRIPLINK Node API

### Parameters

* `ip`: GRIPLINK IP address (default: `192.168.1.40`)
* `port`: GRIPLINK TCP port (default: `10001`)

### Topics

* `/griplink_node/device_states` – Publishes current state of connected devices.

### Services

Refer to [service definitions](griplink/griplink_interfaces/srv).
Examples:

```bash
ros2 service call /griplink_node/home griplink_interfaces/srv/Home "{port: 0}"
ros2 service call /griplink_node/grip griplink_interfaces/srv/Grip "{port: 0, index: 0}"
```

### Actions

* `/griplink_node/grip` – Gripper action
* `/griplink_node/release` – Release action
* WPG-specific: `/flexgrip`, `/flexrelease`

```bash
ros2 action send_goal /griplink_node/grip griplink_interfaces/action/Grip "{port: 0, index: 0}" --feedback
```

---

## Debugging

1. Check available topics, services, and actions:

```bash
ros2 topic list
ros2 service list
ros2 action list
```

2. Inspect published data:

```bash
ros2 topic echo /griplink_node/device_states
```

3. Use services or actions to test gripper functionality.

---

## References

* [Weiss Robotics WPG Series Manual](https://weiss-robotics.com/servo-electric/wpg-series/product/wpg/selectVariant/wpg-300-120-218/?file=files/downloads/wpg/um_wpg_series_en.pdf&cid=10276)

---

## License

This project is licensed under **MIT License** – see the [LICENSE](LICENSE) file.

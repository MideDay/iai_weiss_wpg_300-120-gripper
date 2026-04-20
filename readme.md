# Griplink Python Wrapper & ROS2 Integration – README

## Overview

This repository provides a **complete interface stack** for controlling the **WPG 300-120 gripper**:

* **Griplink Python Wrapper** – Lightweight scripting for fast prototyping
* **ROS2 Integration** – Full robotic system integration (planning, control, execution)

This dual approach enables a seamless transition from
**quick experiments → real robotic deployment**.

---

# Part 1: Griplink Python Wrapper

## Installation

Download and install the official wrapper:

```bash
wget https://weiss-robotics.com/files/griplink-plugins-table/pygriplink-2.0.0.zip
unzip pygriplink-2.0.0.zip
cd pygriplink-2.0.0

tar -xf pygriplink-2.0.0.tar.gz
cd pygriplink-2.0.0

pip install -e .
```

---

## Quick Start

```python
from griplink import Griplink

gripper = Griplink("192.168.1.40")  # Replace with your gripper IP
```

---

## Core Commands

| Command         | Description                           | Example                      |
| --------------- | ------------------------------------- | ---------------------------- |
| `grip()`        | Close gripper using preset            | `gripper.grip(0, 1)`         |
| `release()`     | Open gripper using preset             | `gripper.release(0, 1)`      |
| `flexgrip()`    | Precise grip (position, force, speed) | See below                    |
| `flexrelease()` | Controlled release motion             | See below                    |
| `get_pos_mm()`  | Read jaw position                     | `gripper.get_pos_mm(0)`      |
| `mgrip()`       | Multi-device grip                     | `gripper.mgrip([...], 1)`    |
| `mrelease()`    | Multi-device release                  | `gripper.mrelease([...], 1)` |

---

## Flexible Control (Recommended for Precision Tasks)

```python
gripper.flexgrip(
    device_idx=0,
    target_position=20.0,
    force=10,
    speed=50.0,
    acceleration=100.0
)
```

```python
gripper.flexrelease(
    device_idx=0,
    target_position=50.0,
    speed=50.0,
    acceleration=100.0
)
```

---

## Multi-Gripper Example

```python
gripper.mgrip([True, False, True], preset_idx=1)
gripper.mrelease([True, False, True], preset_idx=1)
```

**Note:** Multi-device control is only applicable when multiple grippers are connected via a [GRIPLINK](https://weiss-robotics.com/griplink/griplink-et4/product/griplink-et4/) controller (e.g., GRIPLINK ET4).

---

## Minimal Example

```python
from griplink import Griplink

gripper = Griplink("192.168.1.40")

gripper.grip(0, 1)
gripper.release(0, 1)

gripper.disconnect()
```

### Parameter Explanation

```python
gripper.grip(0, 1)
```

* `0` → **device_idx (port number)**

  * Default port for WPG gripper = **0**

* `1` → **preset index**

  * Predefined gripping configuration stored in the gripper
  * Range typically: **1 to 8**
  * Each preset corresponds to a predefined:

    * Position
    * Force
    * Speed

Same applies for:

```python
gripper.release(0, 1)
```

---

## ⚠️ Notes

* `device_idx` = port on GRIPLINK controller
* Units:

  * Position → **mm**
  * Force → **N**
  * Speed → **mm/s**
* Default TCP port: **10001**

---

# Part 2: ROS2 Integration (WPG 300-120)

## Features

* GRIPLINK exposed as a ROS2 node
* Real-time device state publishing
* Service-based command interface
* Action-based execution for long tasks
* RViz visualization support

---

## Repository Structure

```text
iai_weiss_wpg_300-120-gripper/
├── griplink/
│   ├── griplink/
│   ├── griplink_interfaces/
├── wpg_300_120_description/
```

---

## Installation

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/local_setup.bash
```

---

## Launch

### Visualization

```bash
ros2 launch wpg_300_120_gripper_description display.launch.py
```

### Real Hardware

```bash
ros2 launch wpg_300_120_gripper_description gripper_interface.launch.py
```

---

## ROS2 API

### Topics

| Topic                          | Description           |
| ------------------------------ | --------------------- |
| `/griplink_node/device_states` | Current gripper state |

---

## 🧾 Key Services

| Service        | Purpose           | Example                                            |
| -------------- | ----------------- | -------------------------------------------------- |
| `/enable`      | Enable device     | `ros2 service call /griplink_node/enable ...`      |
| `/home`        | Home gripper      | `ros2 service call /griplink_node/home ...`        |
| `/grip`        | Grip preset       | `ros2 service call /griplink_node/grip ...`        |
| `/release`     | Release preset    | `ros2 service call /griplink_node/release ...`     |
| `/flexgrip`    | Precision grip    | `ros2 service call /griplink_node/flexgrip ...`    |
| `/flexrelease` | Precision release | `ros2 service call /griplink_node/flexrelease ...` |
| `/devstate`    | Device state      | `ros2 service call /griplink_node/devstate ...`    |

---

## ⚙️ Complete Service Reference

### 🟢 System Services

| Service       | Purpose          | Key Inputs        | Notes         |
| ------------- | ---------------- | ----------------- | ------------- |
| `/id`         | System ID        | –                 | Identifier    |
| `/protocol`   | Protocol version | –                 | Compatibility |
| `/protassert` | Assert protocol  | protocol, version | Safety        |
| `/ver`        | Firmware version | –                 | System info   |
| `/sn`         | Serial number    | –                 | Unique ID     |
| `/labelget`   | Get label        | –                 | Name          |
| `/labelset`   | Set label        | label             | Rename        |
| `/verbose`    | Debug mode       | enable            | Logging       |
| `/bye`        | Disconnect       | –                 | Session close |

---

### 🔌 Device Information Services

| Service      | Purpose     | Key Inputs     | Notes          |
| ------------ | ----------- | -------------- | -------------- |
| `/devname`   | Device name | port           | e.g. WPG       |
| `/devvendor` | Vendor      | port           | Weiss Robotics |
| `/devsn`     | Serial      | port           | Hardware ID    |
| `/devver`    | Version     | port           | Firmware       |
| `/devvid`    | Vendor ID   | port           | USB-style ID   |
| `/devpid`    | Product ID  | port           | Device ID      |
| `/devtagget` | Get tag     | port           | Metadata       |
| `/devtagset` | Set tag     | port, tag      | Custom label   |
| `/devstate`  | State       | port           | IMPORTANT      |
| `/devassert` | Validate    | port, vid, pid | Safety check   |

---

### ⚙️ Control Services

| Service        | Purpose          | Key Inputs                                 |
| -------------- | ---------------- | ------------------------------------------ |
| `/enable`      | Enable device    | port                                       |
| `/disable`     | Disable device   | port                                       |
| `/home`        | Home gripper     | port                                       |
| `/grip`        | Grip preset      | port, index                                |
| `/release`     | Release preset   | port, index                                |
| `/flexgrip`    | Advanced grip    | port, position, force, speed, acceleration |
| `/flexrelease` | Advanced release | port, position, speed, acceleration        |
| `/clamp`       | Clamp control    | port, enable                               |
| `/led`         | LED control      | port, index                                |

---

## 🤖 Actions

| Action         | Purpose            | Goal Inputs                                | Feedback      |
| -------------- | ------------------ | ------------------------------------------ | ------------- |
| `/grip`        | Close gripper      | port, index                                | current state |
| `/release`     | Open gripper       | port, index                                | current state |
| `/flexgrip`    | Parametric grip    | port, position, force, speed, acceleration | current state |
| `/flexrelease` | Parametric release | port, position, speed, acceleration        | current state |

---

## Debugging

```bash
ros2 topic list
ros2 service list
ros2 action list
ros2 topic echo /griplink_node/device_states
```

---

## ⚠️ Execution Rules

* Enable device before issuing commands
* Always home the gripper before first use
* Monitor `/griplink_node/device_states`
* Ensure correct port mapping (**WPG default = 0**)

---

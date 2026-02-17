# GRIPLINK-ROS2 Plugin 1.0.0

## Overview

The **GRIPLINK-ROS2 Plugin** is a C++ project that provides a ROS2 interface for managing communication between the ROS2 environment and Weiss Robotics' GRIPLINK technology. The [GRIPLINK Unified Command Set (UCS) manual](https://weiss-robotics.com/griplink-technology/?file=files/downloads/griplink/unified_command_set_reference_manual_en.pdf&cid=12367) offers an overview of the commands used to control grippers or other devices connected to the GRIPLINK.

### Features

- **GRIPLINK Node**: Implements the GRIPLINK UCS as a ROS2 node, allowing other ROS2 nodes to control devices connected to the GRIPLINK via topics, services, and actions.
  - **Topics**: Periodic publication of information from the GRIPLINK.
  - **Services**: The entire GRIPLINK UCS is implemented as ROS2 services.
  - **Actions**: Time-consuming commands like grip and release are implemented as ROS2 actions.
- **Demo Node**: A simple client node example demonstrating communication with the GRIPLINK node. It performs basic gripper operations such as homing, gripping, and releasing. Functions as a quick start.

The plugin has been tested with **ROS2 Humble Hawksbill** on **Ubuntu 22.04**.
---

## Building from Source

### Prerequisites

- **ROS2 Humble** installed on **Ubuntu 22.04**.
- The connected GRIPLINK device must support the GRIPLINK protocol V3.

### Installation Steps

1. **Install Required Tools**

    ```sh
    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install -U rosdep
    ```

2. **Initialize `rosdep`**

    ```sh
    sudo rosdep init
    rosdep update
    ```

3. **Source ROS2 Underlay**

    ```sh
    source /opt/ros/humble/setup.bash
    ```

4. **Navigate to the Repository**

    ```sh
    cd GRIPLINK_ROS2/
    ```

5. **Install Dependencies**

    ```sh
    rosdep install --from-paths src --ignore-src -r -y
    ```

6. **Build the Workspace**

    ```sh
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
    ```

7. **Source the Workspace**

    ```sh
    . install/local_setup.bash
    ```

---

## Package Overview

The repository contains the following packages:

- **griplink**: Contains the source code for the **GRIPLINK Node** [(`griplink_node.cpp`)](src/griplink/src/griplink_node/griplink_node.cpp) and the **Demo Node** [(`demo_node.cpp`)](src/griplink/src/demo_node/demo_node.cpp). It also includes the implementation of the communication between the GRIPLINK node and the GRIPLINK hardware [(`griplink.cpp`)](src/griplink/src/griplink_node/griplink.cpp).
- **griplink_interfaces**: The interface definition package. It contains custom message, service, and action definitions used by the GRIPLINK node.

---

## Hardware Setup

Ensure that your GRIPLINK or WPG-Series gripper hardware is set up correctly.

- **For GRIPLINK**: Refer to the [Weiss Robotics GRIPLINK Quickstart Guide](https://weiss-robotics.com/griplink-et4/?file=files/downloads/griplink-et4/quickstart_griplink-et4_en.pdf&cid=11021) for hardware setup instructions.

- **For WPG-Series Grippers (Gripper with Integrated GRIPLINK)**: Refer to the [Weiss Robotics WPG Series Manual](https://weiss-robotics.com/servo-electric/wpg-series/product/wpg-series/?file=files/downloads/wpg/um_wpg_series_en.pdf&cid=10276), particularly sections 5.2.1 and 5.2.2, for hardware setup instructions.

### Connection Test

You can test the connection using the web interface (default IP address: http://192.168.1.40) when the GRIPLINK/WPG is connected to your computer's network interface via Ethernet.

---

## Usage

Before running the nodes, make sure to source ROS2 and your workspace in each new terminal session.

```sh
source /opt/ros/humble/setup.bash
. install/local_setup.bash
```

### Launching Nodes

- #### Launch the GRIPLINK Node

    ```sh
    ros2 launch griplink launch.py
    ```

    This command launches the GRIPLINK node, which starts communication with the GRIPLINK hardware.

- #### Launch the Demo Node

    For a quick start, you can launch both the GRIPLINK node and the demo node using:

    ```sh
    ros2 launch griplink demo_launch.py
    ```

    The demo node provides an example of a client node interacting with the GRIPLINK node. It runs a standard gripper cycle, starting with a homing command, and then periodically performing grip and release actions, with or without a workpiece. This demo is designed for a GRIPLINK with a Weiss Robotics servo gripper connected to port 0, or alternatively a WPG-Series gripper.

---

## GRIPLINK Node Documentation

### Parameters

- **`ip`** (default: `192.168.1.40`)

  The IP address of the GRIPLINK connection.

- **`port`** (default: `10001`)

  The port number of the GRIPLINK connection.

### Published Topics

- **`/griplink_node/device_states`**

  Publishes the current state of devices connected to the GRIPLINK.

### Services

The GRIPLINK node provides services corresponding to the GRIPLINK Unified Command Set (UCS). These services allow you to send commands to the GRIPLINK hardware. Documentation of each command is specified in the [GRIPLINK UCS Manual](https://weiss-robotics.com/griplink-technology/?file=files/downloads/griplink/unified_command_set_reference_manual_en.pdf&cid=12367).

All services have additional return values status and message, which is a status response from the GRIPLINK after the command. For service arguments and additional return values, refer to the [service definitions](src/griplink_interfaces/srv). 

- **System Information Services**

  - **`/griplink_node/id`** (/griplink_node/srv/Id)
  - **`/griplink_node/protocol`** (/griplink_node/srv/Protocol)
  - **`/griplink_node/protassert`** (/griplink_node/srv/Protassert)
  - **`/griplink_node/sn`** (/griplink_node/srv/Sn)
  - **`/griplink_node/labelget`** (/griplink_node/srv/Labelget)
  - **`/griplink_node/labelset`** (/griplink_node/srv/Labelset)
  - **`/griplink_node/ver`** (/griplink_node/srv/Ver)
  - **`/griplink_node/verbose`** (/griplink_node/srv/Verbose)

- **Device Information Services**

  - **`/griplink_node/devvid`** (/griplink_node/srv/Devvid)
  - **`/griplink_node/devpid`** (/griplink_node/srv/Devpid)
  - **`/griplink_node/devassert`** (/griplink_node/srv/Devassert)
  - **`/griplink_node/devname`** (/griplink_node/srv/Devname)
  - **`/griplink_node/devvendor`** (/griplink_node/srv/Devvendor)
  - **`/griplink_node/devsn`** (/griplink_node/srv/Devsn)
  - **`/griplink_node/devtagget`** (/griplink_node/srv/Devtagget)
  - **`/griplink_node/devtagset`** (/griplink_node/srv/Devtagset)
  - **`/griplink_node/devver`** (/griplink_node/srv/Devver)

- **Controller Command Service**

  - **`/griplink_node/bye`** (/griplink_node/srv/Bye)
  
- **Device Command Services**

  - **`/griplink_node/enable`** (/griplink_node/srv/Enable)
  - **`/griplink_node/disable`** (/griplink_node/srv/Disable)
  - **`/griplink_node/home`** (/griplink_node/srv/Home)
  - **`/griplink_node/grip`** (/griplink_node/srv/Grip)
  - **`/griplink_node/release`** (/griplink_node/srv/Release)
   - **`/griplink_node/flexgrip`** (/griplink_node/srv/Flexgrip)
  - **`/griplink_node/flexrelease`** (/griplink_node/srv/Flexrelease)
  - **`/griplink_node/led`** (/griplink_node/srv/Led)
  - **`/griplink_node/clamp`** (/griplink_node/srv/Clamp)
  - **`/griplink_node/wstr`** (/griplink_node/srv/Wstr)
  - **`/griplink_node/setval`** (/griplink_node/srv/Setval)
  - **`/griplink_node/waitval`** (/griplink_node/srv/Waitval)

- **Device Status and Diagnosis Services**

  - **`/griplink_node/devstate`** (/griplink_node/srv/Devstate)
  - **`/griplink_node/value`** (/griplink_node/srv/Value)

- **Device Configuration Services**

  - **`/griplink_node/gripcfgget`** (/griplink_node/srv/Gripcfgget)
  - **`/griplink_node/gripcfgset`** (/griplink_node/srv/Gripcfgset)

### Actions

Some GRIPLINK commands are time-consuming and may interfere with subsequent commands if not managed properly. To handle this, these commands are implemented as ROS2 actions, which provide feedback and result reporting. Using the action interface ensures that these operations complete before new commands are processed, preventing mid-operation interruptions.

All actions have additional return values status and message, which is a status response from the GRIPLINK after the command.

- **`/griplink_node/grip`** (/griplink_node/action/Grip)
- **`/griplink_node/release`** (/griplink_node/action/Release)

  For WPG-Series only:
  - **`/griplink_node/flexgrip`** (/griplink_node/action/Flexgrip)
  - **`/griplink_node/flexrelease`** (/griplink_node/action/Flexrelease)


---

## Debugging

There are three types of GRIPLINK commands:

- **Command**: Executes an action on the device.
- **Query**: Retrieves information from the device.
- **Assignment**: Sets a parameter on the device.

Understanding these can help in troubleshooting and interacting with the GRIPLINK hardware and its response.

### Testing the GRIPLINK Node in the Terminal

List available ROS2 topics, services, and actions:

```sh
ros2 topic list
ros2 service list
ros2 action list
```

Inspect data and interact with the node:

- **Example: View Published Topics**

  ```sh
  ros2 topic echo /griplink_node/device_states
  ```

- **Example: Call Services**

  ```sh
  ros2 service call /griplink_node/home griplink_interfaces/srv/Home "{port: 0}"
  ```

- **Example: Send Action Goals**

  ```sh
  ros2 action send_goal /griplink_node/grip griplink_interfaces/action/Grip "{port: 0, index: 0}" --feedback
  ```

---

## Additional Resources

- **[GRIPLINK UCS Manual](https://weiss-robotics.com/griplink-technology/?file=files/downloads/griplink/unified_command_set_reference_manual_en.pdf&cid=12367)**: For detailed information about the GRIPLINK Unified Command Set.
- **[ROS2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html)**: For general ROS2 guidance and troubleshooting.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
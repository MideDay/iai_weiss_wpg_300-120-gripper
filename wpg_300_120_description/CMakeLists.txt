cmake_minimum_required(VERSION 3.8)
project(wpg_300_120_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclpy REQUIRED)

# Install folders
install(
  DIRECTORY launch urdf meshes rviz2
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

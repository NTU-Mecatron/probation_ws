cmake_minimum_required(VERSION 3.8)
project(probation_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(PROGRAMS
  scripts/solution_template.py
  DESTINATION lib/${PROJECT_NAME})

ament_package()

#!/bin/bash
set -e

# Source ROS2 underlay
source "/opt/ros/jazzy/setup.bash"

# Source probation_ws overlay if built
if [ -f "$HOME/probation_ws/install/setup.bash" ]; then
  source "$HOME/probation_ws/install/setup.bash"
fi

exec "$@"

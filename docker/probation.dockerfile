FROM ros:jazzy-ros-base

# Install system essentials & core ROS 2 packages for probation_ws
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    sudo git vim nano tmux ca-certificates \
    python3-pip python3-colcon-common-extensions \
    ros-jazzy-mavros ros-jazzy-mavros-extras \
    ros-jazzy-foxglove-bridge \
    bash-completion \
    && pip install --break-system-packages --no-cache-dir colcon-clean \
    && rm -rf /var/lib/apt/lists/*

# Setup non-root user matching host UID/GID (1000)
ARG USERNAME=mecatron
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if id -u $USER_UID >/dev/null 2>&1; then userdel -f `id -un $USER_UID`; fi \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME/probation_ws

# Setup bashrc strictly for probation_ws
COPY --chown=$USERNAME:$USERNAME docker/bashrc_custom.txt /tmp/bashrc_custom.txt
RUN cat /tmp/bashrc_custom.txt >> /home/$USERNAME/.bashrc && rm /tmp/bashrc_custom.txt

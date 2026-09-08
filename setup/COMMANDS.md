# Команды установки

Краткая шпаргалка без пояснений. Подробности и ограничения: [`FROM_ZERO.md`](FROM_ZERO.md).

## Windows PowerShell (администратор)

```powershell
winget install --id Microsoft.WindowsTerminal -e
winget install --id Microsoft.PowerShell -e
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id OpenJS.NodeJS.LTS -e

git --version
code --version
node --version
npm --version

wsl --install -d Ubuntu-24.04
```

## VS Code extensions

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-iot.vscode-ros
code --install-extension ms-vscode.cpptools
code --install-extension ms-vscode.cmake-tools
code --install-extension redhat.vscode-yaml
code --install-extension bradlc.vscode-tailwindcss
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-vscode-remote.remote-ssh
```

## Ubuntu 24.04: база и VS Code

```bash
sudo apt update
sudo apt install -y \
  git curl wget unzip ca-certificates gnupg locales software-properties-common \
  build-essential python3 python3-pip python3-venv python3-dev \
  mesa-utils libxcb-cursor0 libxcb-xinerama0
sudo snap install --classic code

git --version
python3 --version
code --version
glxinfo -B
```

## Git и SSH

```bash
git config --global user.name "Nikita Shilov"
git config --global user.email "YOUR_EMAIL"
git config --global init.defaultBranch main
ssh-keygen -t ed25519 -C "chvt-2026"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub

mkdir -p ~/scripts
git clone git@github.com:mavxa/mvch.git ~/scripts/mvch
git clone git@github.com:mavxa/mvch-docs.git ~/scripts/mvch-docs

git -C ~/scripts/mvch remote add gitea ssh://git@GITEA_HOST/USER/mvch.git
git -C ~/scripts/mvch push gitea --all
git -C ~/scripts/mvch push gitea --tags
git -C ~/scripts/mvch-docs remote add gitea ssh://git@GITEA_HOST/USER/mvch-docs.git
git -C ~/scripts/mvch-docs push gitea --all
git -C ~/scripts/mvch-docs push gitea --tags
```

## ROS 2 Jazzy

```bash
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo add-apt-repository universe
sudo apt update

export ROS_APT_SOURCE_VERSION="$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F 'tag_name' | awk -F\" '{print $4}')"
curl -L -o /tmp/ros2-apt-source.deb \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

sudo apt update
sudo apt install -y ros-jazzy-desktop ros-dev-tools \
  ros-jazzy-rmw-fastrtps-cpp python3-colcon-common-extensions python3-rosdep

sudo rosdep init
rosdep update
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```

## Webots

```bash
sudo mkdir -p /etc/apt/keyrings
sudo wget -q https://cyberbotics.com/Cyberbotics.asc \
  -O /etc/apt/keyrings/Cyberbotics.asc
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/Cyberbotics.asc] https://cyberbotics.com/debian binary-amd64/" \
  | sudo tee /etc/apt/sources.list.d/Cyberbotics.list
sudo apt update
sudo apt install -y webots
which webots
readlink -f "$(command -v webots)"
webots --version
```

## ROS-пакеты ЧВТ

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://gitlab.mobird.dev/fms_group/ar_webots_fms_ros2.git
git clone https://gitlab.mobird.dev/fms_group/ar_arm95_moveit_config.git
git clone https://gitlab.mobird.dev/fms_group/ar_aruco_detect_ros2.git
git clone https://gitlab.mobird.dev/fms_group/ar_dual_lidar_merge_ros2.git
git clone https://gitlab.mobird.dev/fms_group/ar_nav_ros2.git

cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src -y --ignore-src --rosdistro jazzy
colcon build --symlink-install
source ~/ros2_ws/install/setup.bash
```

## Python/YOLO

```bash
cd ~/scripts/mvch/module3
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements.txt tqdm ultralytics-thop
.venv/bin/pip install --force-reinstall \
  "numpy<2" "opencv-python<4.12" lark transforms3d

source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
.venv/bin/python -c \
  "import rclpy, cv_bridge, numpy, torch, ultralytics; print('Python/ROS/YOLO OK')"
```

## Bun, module4 и Node.js

```bash
curl -fsSL https://bun.com/install | bash
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
bun --version

cd ~/scripts/mvch/module4
bun install
bun run check
bun run build

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install --lts
node --version
npm --version
```

## OpenCode (необязательно)

Ubuntu/Linux:

```bash
curl -fsSL https://opencode.ai/install | bash
source ~/.bashrc
opencode --version
```

Windows PowerShell:

```powershell
npm install -g opencode-ai
opencode --version
```

## Проверка окружения и топиков

```bash
cd ~/scripts/mvch-docs
./setup/check_environment.sh

source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

ros2 node list
ros2 topic list | sort
ros2 topic echo /RMC1/odometry --once
ros2 topic echo /RMC2/odometry --once
ros2 topic echo /RMC2/scan_front --once
```

## Git bundle на флешку

```bash
mkdir -p ~/chvt-backup
git -C ~/scripts/mvch bundle create ~/chvt-backup/mvch.bundle --all
git -C ~/scripts/mvch-docs bundle create ~/chvt-backup/mvch-docs.bundle --all
git bundle verify ~/chvt-backup/mvch.bundle
git bundle verify ~/chvt-backup/mvch-docs.bundle
```

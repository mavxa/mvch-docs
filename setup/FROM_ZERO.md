# Подготовка рабочего места с нуля

Цель — за день настройки получить воспроизводимое рабочее место для физических РМК и Webots. Основная среда проекта: **Ubuntu 24.04 x86-64, ROS 2 Jazzy, Webots, Fast DDS, Python 3 и Git**.

Все команды без объяснений продублированы в [`COMMANDS.md`](COMMANDS.md).

## Сначала уточнить у эксперта

До установки и обновлений зафиксируйте:

1. Какая ОС и что уже установлено.
2. Нужно ли использовать готовый образ организаторов.
3. Какую версию Webots требует выданный пакет.
4. Адреса GitLab/локального Git, логин и доступ к интернету.
5. `ROS_DOMAIN_ID`, RMW и схему сети физических РМК.
6. Разрешённые программы, сайты и LLM.

Не обновляйте целиком уже работающее окружение непосредственно перед попыткой.

## Если выдали Windows

Windows используем как хост для редактора, Git и резервного доступа. Конкурсный ROS-стек из материалов рассчитан на Ubuntu 24.04. Нативную сборку всех пакетов под Windows нельзя считать равноценной без подтверждения организаторов.

Откройте PowerShell от администратора:

```powershell
winget install --id Microsoft.WindowsTerminal -e
winget install --id Microsoft.PowerShell -e
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id OpenJS.NodeJS.LTS -e
```

После установки закройте и снова откройте терминал:

```powershell
git --version
code --version
node --version
npm --version
```

Для вспомогательной Linux-среды можно установить Ubuntu 24.04 в WSL:

```powershell
wsl --install -d Ubuntu-24.04
```

После команды требуется перезапуск Windows. WSL подходит для Git, Python, Bun и редактирования, но DDS discovery, multicast, USB-камера и графический Webots могут отличаться от обычного Ubuntu. Для физического заезда предпочтительны нативный Ubuntu либо выданная Ubuntu VM с bridged-сетью и проверенным OpenGL.

Если используется Ubuntu VM, выделите не менее 4 CPU, 8 ГБ RAM и 50 ГБ диска. Включайте 3D-ускорение только после проверки стабильности конкретного гипервизора.

## Если выдали Ubuntu 24.04

### Базовые программы

```bash
sudo apt update
sudo apt install -y \
  git curl wget unzip ca-certificates gnupg locales software-properties-common \
  build-essential python3 python3-pip python3-venv python3-dev \
  mesa-utils libxcb-cursor0 libxcb-xinerama0
```

Проверка GPU:

```bash
glxinfo -B
```

В `OpenGL renderer` не должно быть `llvmpipe`, если Webots должен работать с аппаратным ускорением.

### Visual Studio Code

Короткий официальный вариант для Ubuntu:

```bash
sudo snap install --classic code
code --version
```

Snap здесь используется только для VS Code. Webots устанавливайте через `.deb`/APT: Snap-версия Webots уже создавала проблемы с ROS и Qt.

Минимальные расширения:

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
```

Для Windows/WSL дополнительно:

```powershell
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-vscode-remote.remote-ssh
```

### Git и доступ к репозиториям

```bash
git config --global user.name "Nikita Shilov"
git config --global user.email "YOUR_EMAIL"
git config --global init.defaultBranch main

ssh-keygen -t ed25519 -C "chvt-2026"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Добавьте **публичный** ключ в GitHub/Gitea. Приватный `~/.ssh/id_ed25519` никуда не отправляйте и не коммитьте.

```bash
mkdir -p ~/scripts
git clone git@github.com:mavxa/mvch.git ~/scripts/mvch
git clone git@github.com:mavxa/mvch-docs.git ~/scripts/mvch-docs
```

Если GitHub недоступен, замените URL на зеркало Gitea. После клонирования код полностью локален; интернет для `git status`, веток и коммитов не нужен.

Добавление зеркала к уже клонированному репозиторию:

```bash
git remote add gitea ssh://git@GITEA_HOST/USER/mvch.git
git push gitea --all
git push gitea --tags
```

Для `mvch-docs` повторите команды в его каталоге с URL репозитория `mvch-docs`.

### ROS 2 Jazzy

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
```

Инициализация `rosdep` выполняется один раз:

```bash
sudo rosdep init
rosdep update
```

Если `rosdep init` пишет, что файл источников уже существует, повторять команду не нужно.

```bash
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ros2 --help
```

### Webots

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

Не задавайте `WEBOTS_HOME=/snap/webots/...` для APT-версии. Сначала проверьте реальный путь.

### Пакеты симулятора и управления

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

Если закрытый GitLab не открывается, это вопрос доступа организаторов. Не подменяйте пакеты случайными форками.

Добавить окружение в Bash можно после успешной ручной проверки:

```bash
printf '%s\n' \
  'source /opt/ros/jazzy/setup.bash' \
  'source ~/ros2_ws/install/setup.bash' \
  'export RMW_IMPLEMENTATION=rmw_fastrtps_cpp' \
  >> ~/.bashrc
```

### Python, YOLO и ROS

```bash
cd ~/scripts/mvch/module3
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements.txt tqdm ultralytics-thop
.venv/bin/pip install --force-reinstall \
  "numpy<2" "opencv-python<4.12" lark transforms3d
```

Проверка:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
~/scripts/mvch/module3/.venv/bin/python -c \
  "import rclpy, cv_bridge, numpy, torch, ultralytics; print('Python/ROS/YOLO OK')"
```

CPU-сборки достаточно для запуска и короткой проверки. CUDA/ROCm устанавливайте только под фактическую видеокарту по официальному селектору PyTorch.

### Bun и Node.js

Для `module4` нужен Bun:

```bash
sudo apt install -y unzip
curl -fsSL https://bun.com/install | bash
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
bun --version

cd ~/scripts/mvch/module4
bun install
bun run check
bun run build
```

Node.js для этого проекта не обязателен, но полезен как запасной runtime и для npm-инструментов:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install --lts
node --version
npm --version
```

### OpenCode — только если разрешён и нужен

Linux/Ubuntu:

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
```

Windows после установки Node.js:

```powershell
npm install -g opencode-ai
opencode --version
```

Не записывайте API-ключи в репозитории, README или историю терминала. Способ авторизации выбирайте по правилам площадки.

## День настройки физического оборудования

Делайте проверки по слоям:

1. `ip addr`, `ip route`, доступность адресов РМК.
2. `ROS_DOMAIN_ID` и `RMW_IMPLEMENTATION` по данным эксперта.
3. `ros2 topic list | sort` и `ros2 node list`.
4. Отдельно проверить `/RMC1/odometry`, `/RMC2/odometry`, лидары, камеры и TF.
5. На вывешенных колёсах кратко подать малую скорость и немедленно STOP.
6. Проверить лифт RMC2 без стеллажа.
7. Проверить ARM95 сначала без детали и на безопасной высоте.
8. Собрать датасет только выданной/разрешённой камерой и сделать dry-run детектора.
9. Зафиксировать реальные топики, фреймы, размеры, точки и параметры в отдельном локальном коммите.
10. Сделать контрольный прогон и офлайн-бэкап.

Не начинайте с полного модуля Д: сначала независимо подтвердите каждую платформу, лифт, камеру, детектор и манипулятор.

## Защита от блокировки GitHub

Основной вариант — зеркало на доступной Gitea. Дополнительно сделайте Git bundle обоих репозиториев:

```bash
mkdir -p ~/chvt-backup
git -C ~/scripts/mvch bundle create ~/chvt-backup/mvch.bundle --all
git -C ~/scripts/mvch-docs bundle create ~/chvt-backup/mvch-docs.bundle --all
git bundle verify ~/chvt-backup/mvch.bundle
git bundle verify ~/chvt-backup/mvch-docs.bundle
```

Проверка восстановления:

```bash
git clone ~/chvt-backup/mvch.bundle /tmp/mvch-restore-test
git -C /tmp/mvch-restore-test log -1 --oneline
```

Bundle содержит историю Git и отслеживаемые веса модели, но не содержит `.venv`, `node_modules`, системные пакеты и секреты. На флешку отдельно сохраните установщик/образ Ubuntu, нужную версию Webots, экспорт датасета и при необходимости wheel/cache зависимостей.

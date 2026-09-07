#!/usr/bin/env bash
set -u

warnings=0

check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    printf '[OK] %s: %s\n' "$1" "$(command -v "$1")"
  else
    printf '[WARN] команда %s не найдена\n' "$1"
    warnings=$((warnings + 1))
  fi
}

if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  source /etc/os-release
  printf '[INFO] OS: %s %s\n' "${NAME:-unknown}" "${VERSION_ID:-unknown}"
  if [[ "${ID:-}" == ubuntu && "${VERSION_ID:-}" == 24.04 ]]; then
    :
  else
    printf '[WARN] официальное окружение задания рассчитано на Ubuntu 24.04\n'
    warnings=$((warnings + 1))
  fi
fi

for command_name in git python3 ros2 colcon webots; do
  check_command "$command_name"
done

if [[ -r /opt/ros/jazzy/setup.bash ]]; then
  set +u
  # shellcheck disable=SC1091
  source /opt/ros/jazzy/setup.bash
  set -u
  printf '[OK] ROS 2 Jazzy setup найден\n'
else
  printf '[WARN] /opt/ros/jazzy/setup.bash не найден\n'
  warnings=$((warnings + 1))
fi

workspace_path="${ROS_WORKSPACE:-$HOME/ros2_ws}"
if [[ -r "$workspace_path/install/setup.bash" ]]; then
  set +u
  # shellcheck disable=SC1090
  source "$workspace_path/install/setup.bash"
  set -u
  printf '[OK] workspace: %s\n' "$workspace_path"
else
  printf '[WARN] workspace не собран: %s\n' "$workspace_path"
  warnings=$((warnings + 1))
fi

if command -v ros2 >/dev/null 2>&1; then
  for package_name in ar_webots_fms_ros2 ar_arm95_moveit_config ar_aruco_detect_ros2; do
    if ros2 pkg prefix "$package_name" >/dev/null 2>&1; then
      printf '[OK] ROS-пакет: %s\n' "$package_name"
    else
      printf '[WARN] ROS-пакет не найден: %s\n' "$package_name"
      warnings=$((warnings + 1))
    fi
  done
fi

if python3 -c 'import rclpy, cv_bridge' >/dev/null 2>&1; then
  printf '[OK] Python: rclpy и cv_bridge импортируются\n'
else
  printf '[WARN] Python не импортирует rclpy/cv_bridge\n'
  warnings=$((warnings + 1))
fi

if command -v glxinfo >/dev/null 2>&1; then
  glxinfo -B 2>/dev/null | sed -n '/OpenGL vendor/p;/OpenGL renderer/p'
fi

printf '\nИтог: %d предупреждений. WARN не всегда означает поломку, но проверьте его до заезда.\n' "$warnings"

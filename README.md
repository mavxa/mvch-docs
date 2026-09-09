# ЧВТ-2026: документы и памятка по подготовке

Этот приватный репозиторий — офлайн-набор для подготовки: исходные материалы организаторов, порядок установки окружения, ссылки на документацию и короткие ROS-примеры. Рабочие решения модулей лежат отдельно в [`mavxa/mvch`](https://github.com/mavxa/mvch).

> Конкурсное задание, критерии и указания экспертов на площадке имеют приоритет над этой памяткой и старыми презентациями. Не меняйте мир Webots, расположение объектов и штатные управляющие пакеты, если это прямо не разрешено экспертами.

## Что лежит в репозитории

- [`materials/presentations`](materials/presentations) — пять учебных презентаций (введение, документация, Python/ROS, симулятор, развитие компетенции).
- [`materials/pdf`](materials/pdf) — шестая презентация про датасет и модели, расписание.
- [`materials/final`](materials/final) — полный очный финал: инфраструктурный лист, КЗ модулей А–Д, критерии и приложения.
- [`materials/tasks`](materials/tasks) — отдельный ранний/отборочный комплект по навигации; не путать с полным финалом.
- [`basic`](basic) — примеры для реального ROS 2: движение к ArUco с odometry/TF/lidar, ручной `cmd_vel`, остановка, лифт, мониторинг и BFS-маршрут.
- [`setup/FROM_ZERO.md`](setup/FROM_ZERO.md) — подготовка полностью чистого Windows/Ubuntu и день настройки оборудования.
- [`setup/COMMANDS.md`](setup/COMMANDS.md) — только команды для копирования в терминал.
- [`setup/check_environment.sh`](setup/check_environment.sh) — безопасная read-only проверка окружения.
- [`COMPETITION_NOTES.md`](COMPETITION_NOTES.md) — актуальные устные уточнения, лимиты скриптов и предложения 30% изменений.

Материалы собраны из выданного набора ЧВТ. Репозиторий оставлен приватным: права на исходные презентации и задание принадлежат их авторам/организаторам.
Актуальную опубликованную редакцию сверяйте с [официальным комплектом финала 2026](https://esim.firpo.ru/d/f/2026), раздел «Оператор-техник складских роботов (AGV/AMR)».

## Порядок чтения

1. `materials/final/04-final-task.docx` и `materials/final/05-final-criteria.xlsx` — сначала понять конечный результат и баллы очного финала.
2. `1. Введение...` и `2. Документация...` — термины, РМК и структура компетенции.
3. `3. Разбор...` — Python, ROS 2, топики и сервисы.
4. `4. Практика... (симулятор)` — установка и работа с Webots.
5. `5. Практика... (датасет + модели)` — разметка и обучение детектора.
6. `setup/FROM_ZERO.md` — подготовка ПК и оборудования.
7. README каждого модуля в `mvch` — точные команды текущего решения.

## Быстрый старт на подготовленной VM

Нужны SSH-ключ с доступом к приватным GitHub-репозиториям и уже установленное окружение ROS/Webots.

```bash
mkdir -p ~/scripts
git clone git@github.com:mavxa/mvch-docs.git ~/scripts/mvch-docs
git clone git@github.com:mavxa/mvch.git ~/scripts/mvch

cd ~/scripts/mvch-docs
./setup/check_environment.sh
```

Если на площадке недоступен GitHub, подготовлены отдельные зеркала на Gitea:

- код модулей: [`mavxa/chvt-bak`](https://git.vihrev.com/mavxa/chvt-bak);
- документация: [`mavxa/chvt-docs`](https://git.vihrev.com/mavxa/chvt-docs).

```bash
mkdir -p ~/scripts
git clone ssh://git@git.vihrev.com:2222/mavxa/chvt-bak.git ~/scripts/mvch
git clone ssh://git@git.vihrev.com:2222/mavxa/chvt-docs.git ~/scripts/mvch-docs
```

SSH-доступ к обоим серверам проверьте заранее. Помимо удалённых репозиториев,
держите готовые копии каталогов на флешке: блокировка сети может затронуть и
GitHub, и внешний Gitea.

В каждом новом ROS-терминале:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

Перед поездкой обновлять только fast-forward:

```bash
cd ~/scripts/mvch
git switch main
git pull --ff-only
```

## Установка чистого окружения

Официальная целевая база материалов — **Ubuntu 24.04 LTS + ROS 2 Jazzy + Webots + Fast DDS + colcon**. На площадке лучше использовать выданный и заранее проверенный образ, если он будет предоставлен.

Полный путь от чистой Windows/Ubuntu, включая VS Code, расширения, Git/SSH, ROS, Webots, Python/YOLO, Bun, Node.js и OpenCode: [`setup/FROM_ZERO.md`](setup/FROM_ZERO.md). Краткий файл только с командами: [`setup/COMMANDS.md`](setup/COMMANDS.md).

### 1. ROS 2 Jazzy

Устанавливайте Jazzy по [официальной инструкции ROS 2 для Ubuntu](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), включая настройку locale и репозитория ROS. Минимальный набор после подключения репозитория:

```bash
sudo apt update
sudo apt install ros-jazzy-desktop ros-dev-tools python3-colcon-common-extensions \
  python3-rosdep python3-venv git

source /opt/ros/jazzy/setup.bash
```

`rosdep init` выполняется один раз на систему:

```bash
sudo rosdep init
rosdep update
```

Если команда сообщает, что sources list уже существует, повторный `rosdep init` не нужен.

### 2. Webots

Сверяйте установку с [официальной инструкцией Cyberbotics](https://cyberbotics.com/doc/guide/installing-webots). Версия симулятора должна совпадать с версией, под которую собран выданный ROS-пакет; самовольно обновлять её прямо перед соревнованием не стоит.

### 3. Пакеты симулятора ЧВТ

Команды из выданных материалов:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

git clone https://gitlab.mobird.dev/fms_group/ar_webots_fms_ros2.git
git clone https://gitlab.mobird.dev/fms_group/ar_arm95_moveit_config.git
git clone https://gitlab.mobird.dev/fms_group/ar_aruco_detect_ros2.git
git clone https://gitlab.mobird.dev/fms_group/ar_dual_lidar_merge_ros2.git
git clone https://gitlab.mobird.dev/fms_group/ar_nav_ros2.git

cd ~/ros2_ws
rosdep install --from-paths src -y --ignore-src
colcon build --symlink-install
source ~/ros2_ws/install/setup.bash
```

GitLab может потребовать выданный организаторами аккаунт/токен. Если clone не работает, не ищите случайные зеркала: запросите доступ у эксперта.

### 4. Python-окружение YOLO и ROS

ROS-библиотеки установлены системно, поэтому venv для модуля В создаётся с `--system-site-packages`. Это также предотвращает несовместимость отдельного Python с бинарными пакетами ROS; подробнее — в [официальной памятке ROS 2 по Python-пакетам](https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html).

```bash
cd ~/scripts/mvch/module3
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements.txt tqdm ultralytics-thop
```

В текущем образе `cv_bridge` требует NumPy 1.x:

```bash
.venv/bin/pip install --force-reinstall "numpy<2" "opencv-python<4.12" lark transforms3d
```

Для NVIDIA/ROCm сначала установите подходящую сборку PyTorch по [официальному селектору PyTorch](https://pytorch.org/get-started/locally/), затем остальные зависимости. Для CPU готовая команда выше достаточна.

### 5. Веб-интерфейс модуля Г

Установите [Bun](https://bun.sh/docs/installation), затем:

```bash
cd ~/scripts/mvch/module4
bun install
bun run build
```

## Быстрая проверка перед работой

```bash
cd ~/scripts/mvch-docs
./setup/check_environment.sh

source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 topic list
ros2 pkg prefix ar_webots_fms_ros2
```

Проверьте только один launch-файл за раз. После его запуска отдельно убедитесь, что приходят сообщения:

```bash
ros2 topic hz /RMC1/odometry
ros2 topic echo /RMC1/odometry --once
ros2 topic echo /RMC2/scan_front --once
```

Точный список топиков зависит от активного launch-файла. Если `scan_front` отсутствует, сначала посмотрите `ros2 topic list | sort`, а не меняйте код вслепую.

## Если на реальном ровере другие датчики или ROS API

Успешный запуск Python-процесса ещё не означает, что ровер готов ехать. Текущие
решения специально не начинают движение без обратной связи:

- нет `odometry` — ROS-нода запустится, но навигация останется в ожидании датчиков
  или завершит предварительную проверку с ошибкой;
- нет `scan`/`scan_front` — движение блокируется, потому что невозможно проверить
  препятствие и тормозной путь;
- нет `aruco_id` или TF `aruco_<ID>` — невозможно привязать odometry к полю и
  подтвердить точное прибытие на маркер;
- нет подписчика на `cmd_vel` — программа будет публиковать команды, но платформа
  не поедет;
- имя совпало, но тип сообщения или QoS отличается — publisher и subscriber не
  соединятся.

Это безопасное поведение. Не отключайте проверки датчиков и не заменяйте odometry
движением «скорость × несколько секунд» на физическом роботе.

### Что снять в день настройки оборудования

Сначала сохраните фактический ROS API, пока ничего не движется:

```bash
mkdir -p ~/equipment-audit

ros2 node list | tee ~/equipment-audit/nodes.txt
ros2 topic list -t | tee ~/equipment-audit/topics.txt
ros2 topic info /RMC2/cmd_vel -v | tee ~/equipment-audit/cmd_vel.txt
ros2 topic info /RMC2/odometry -v | tee ~/equipment-audit/odometry.txt
ros2 topic info /RMC2/scan_front -v | tee ~/equipment-audit/scan_front.txt
ros2 topic info /RMC2/aruco_id -v | tee ~/equipment-audit/aruco_id.txt

timeout 5 ros2 topic hz /RMC2/odometry
timeout 5 ros2 topic hz /RMC2/scan_front
ros2 topic echo /RMC2/odometry --once
ros2 topic echo /RMC2/aruco_id --once

ros2 run tf2_ros tf2_echo RMC2/odom RMC2/base_link
ros2 run tf2_ros tf2_echo RMC2/odom aruco_0
ros2 run tf2_tools view_frames
mv frames.pdf ~/equipment-audit/ 2>/dev/null || true
```

Для RMC1 повторите команды с пространством имён `RMC1`. Номер в `aruco_0`
замените меткой, над которой реально стоит робот. Если ожидаемого топика нет,
сначала найдите аналог через `ros2 topic list -t`, а не создавайте пустой топик с
нужным названием.

### Как адаптировать решение

| Ситуация | Что делать |
| --- | --- |
| Данные те же, отличается только имя топика | Заменить имя в конфигурации/константах до контрольной попытки. В `basic/drive_to_aruco.py` для лидара есть `--scan-topic`. |
| Топик есть, но сообщения не приходят | Проверить активный launch, namespace, `ROS_DOMAIN_ID`, `RMW_IMPLEMENTATION`, сеть и QoS через `ros2 topic info -v`. |
| Вместо `LaserScan` выдаётся другой `LaserScan`-топик | Подставить его имя и проверить `frame_id`, направление нулевого угла, `range_min/max` и сектор перед роботом. |
| Вместо `LaserScan` доступен только `PointCloud2` | Нужен штатный преобразователь облака в scan или отдельная обработка `PointCloud2`; простой rename топика не поможет. |
| `aruco_id` имеет другой формат | Исправить тип подписки и callback. Если публикуется только изображение, сначала нужен штатный ArUco-детектор. |
| ID метки есть, но нет её относительной позы/TF | Одного ID недостаточно для точного центрирования. Найти топик позы метки либо настроить TF из штатного детектора. |
| Нет `/RMC2/odometry`, но есть TF `RMC2/odom -> RMC2/base_link` | Положение можно читать из TF вместо сообщения `Odometry`; потребуется небольшая замена источника позы в скрипте. |
| Есть только энкодеры колёс | Использовать штатный драйвер/локализатор, который формирует odometry и TF. Самостоятельное интегрирование допустимо только после проверки кинематики и масштаба. |
| Нет ни odometry, ни TF, ни позы относительно меток | Безопасная координатная навигация текущим алгоритмом невозможна. Зафиксировать отсутствие интерфейса и сразу сообщить эксперту. |
| Команды движения имеют другой тип, сервис или action | Нужен адаптер к реальному драйверу; публикация `Twist` в новый топик проблему не решит. |

После подключения данных сначала запустите только наблюдение:

```bash
python3 basic/watch_robot.py --robot RMC2
```

Затем проверьте аппаратный STOP и короткую команду на минимальной скорости. Только
после этого запускайте движение между соседними ArUco. До контрольной попытки
также измерьте шаг сетки, направления осей, габариты корпуса, безопасную скорость,
тормозной путь и реальные положения lidar. Во время самой контрольной попытки код
и интерфейс уже нельзя исправлять.

## Запуск модулей

| Модуль | Решение | Основной запуск |
| --- | --- | --- |
| Б | навигация RMC2 по ArUco | `python3 module2/module_b.py --target 14 --sim` |
| В | YOLO + ARM95 | `module3/.venv/bin/python module3/module3.py --target hammer` |
| Г | веб-FMS двух роверов | `cd module4 && bun run start` |
| Д | общий сценарий RMC1 + RMC2 | `module3/.venv/bin/python module5/module5.py --target hammer` |

Запускайте команды из `~/scripts/mvch`. До движения используйте dry-run:

```bash
python3 module2/module_b.py --target 14 --dry-run
module3/.venv/bin/python module3/module3.py --target hammer --dry-run --no-window
python3 module5/module5.py --target hammer --dry-run
```

Для модуля Д сначала проверяйте платформы и лифт без руки: `python3 module5/module5.py --target hammer --skip-arm`.

Лимит полного финального КЗ: модуль Б — максимум 2 скрипта, В — 1, Д — 4. Текущий модуль Д использует один центральный ROS 2 процесс для обоих пространств имён и укладывается в лимит; отдельного UDP-протокола нет.

## Модель для симулятора

Текущая YOLO11n лежит в `mvch/module3/models/latest.pt`. Классы и их написание:

```text
hammer
pliers
wrench
```

Текущий симуляторный датасет очень маленький: 28 train, 8 validation и 4 test изображения. Он годится для проверки пайплайна, но не доказывает работу на реальном стенде. Для реального оборудования нужен отдельный набор кадров с его камеры, светом, фоном, ракурсами и реальными карточками/деталями. Инструкции обучения — в `mvch/module3/README.md` и [Ultralytics Train mode](https://docs.ultralytics.com/modes/train/).

## План подготовки

1. Сохранить рабочую VM и проверить clone обоих репозиториев без старых локальных файлов.
2. Для каждого launch-файла записать реальные `ros2 topic list`, стартовые ID и положения объектов.
3. Пройти модуль Б на нескольких целях и с препятствием у стеллажа; проверить остановку при потере ArUco/лидара.
4. В модуле В сначала подтвердить dry-run координат, затем pick/place на каждом классе.
5. В модуле Г проверить ручной STOP, телеметрию обоих роверов и fallback без Nav2.
6. В модуле Д пройти `--skip-arm`, затем полный последовательный сценарий.
7. Сделать чистый контрольный прогон строго по процедуре эксперта и сохранить логи.
8. На площадке сначала снять фактические топики, TF, размеры, тормозной путь и геометрию ARM95; только потом менять параметры.

## Что уточнить у главного эксперта

- Финал проходит полностью в Webots, на физических РМК или в смешанном формате?
- Какая редакция конкурсного задания и критериев считается действующей?
- Будет ли готовая VM, доступ к закрытому GitLab и разрешено ли принести свой Git-репозиторий?
- Разрешены ли интернет, локальная документация, поисковики и LLM; как технически фиксируются нарушения?
- Какие действия участника допустимы между этапами: Enter, stop/resume, выбор цели, ручное подтверждение маршрута?
- Какие точки/ID сообщаются перед попыткой, а какие должны определяться автоматически?
- Что именно входит в разрешённые 30% изменений задания?

Ответы лучше получить письменно или зафиксировать в протоколе инструктажа.

## Документация и форумы

- [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/)
- [ROS 2 concepts](https://docs.ros.org/en/jazzy/Concepts.html)
- [ROS 2 tf2 tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [webots_ros2_driver API](https://docs.ros.org/en/jazzy/p/webots_ros2_driver/)
- [Webots User Guide](https://cyberbotics.com/doc/guide/index)
- [Webots Discussions](https://github.com/cyberbotics/webots/discussions)
- [MoveIt 2 documentation](https://moveit.picknik.ai/main/index.html)
- [MoveIt 2 issues](https://github.com/moveit/moveit2/issues)
- [Ultralytics documentation](https://docs.ultralytics.com/)
- [Roboflow Annotate documentation](https://docs.roboflow.com/annotate)
- [Robotics Stack Exchange: ROS 2](https://robotics.stackexchange.com/questions/tagged/ros2) — конкретные технические вопросы с логами и минимальным примером.
- [Open Robotics Discourse](https://discourse.ros.org/) — новости и общие обсуждения экосистемы; не основная площадка техподдержки.

Публичного официального форума именно по этому заданию ЧВТ в выданных материалах не указано. Вопросы о правилах, критериях, доступе к репозиториям и оборудованию адресуйте главному эксперту, а не стороннему форуму.

## Git на соревновании

Для критериев обычно достаточно локальной истории: `main`, понятные коммиты и при необходимости ветки модулей. GitHub удобен как резервная копия, но не рассчитывайте на интернет на площадке.

```bash
git status
git log --oneline --decorate --graph --all -20
git switch main
```

Не выполняйте `git reset --hard`, `git clean` и force-push перед попыткой. Скопируйте оба репозитория и веса модели на внешний накопитель или в снапшот VM.

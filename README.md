====================================================================
GUÍA PASO A PASO: CREACIÓN DE WORKSPACES Y PAQUETES EN ROS 2
Tutorial basado en la metodología de Articulated Robotics
====================================================================

EN ESTE TUTORIAL APRENDERÁS A:
1. Crear y estructurar un espacio de trabajo (workspace) con colcon.
2. Crear un paquete ROS 2 basado en CMake (ament_cmake).
3. Añadir y configurar archivos de lanzamiento (launch files) en Python.
4. Actualizar las dependencias y reglas de compilación (CMakeLists.txt y package.xml).
5. Sincronizar el paquete entre la Laptop y la Raspberry Pi mediante Git/GitHub.
6. Compilar, cargar el entorno y probar los nodos en red.

====================================================================
PASO 1: CREACIÓN DEL WORKSPACE (Espacio de Trabajo)
====================================================================
Un workspace es la carpeta contenedora de todos tus proyectos y código fuente.
Por convención:
- En la Laptop (Base Station) lo llamamos: dev_ws
- En la Raspberry Pi (Robot) lo llamamos: robot_ws

Ejecutar en la Laptop (WSL2):
--------------------------------------------------------------------
mkdir -p ~/dev_ws/src
cd ~/dev_ws
colcon build --symlink-install

Ejecutar en la Raspberry Pi:
--------------------------------------------------------------------
mkdir -p ~/robot_ws/src
cd ~/robot_ws
colcon build --symlink-install

Explicación de las opciones:
- `src`: Carpeta donde vivirá el código fuente de nuestros paquetes.
- `colcon build`: Comando para compilar todos los paquetes dentro del workspace.
- `--symlink-install`: Crea enlaces simbólicos en lugar de copiar los archivos.
  Esto permite modificar scripts (como archivos de Python o Launch) sin necesidad
  de volver a compilar con colcon cada vez que haces un cambio.

====================================================================
PASO 2: CREACIÓN DE UN PAQUETE EN ROS 2
====================================================================
Los paquetes organizan ejecutables, configuraciones y scripts reutilizables.

1. Navegar a la carpeta de código fuente en la Laptop:
   cd ~/dev_ws/src

2. Crear un paquete con soporte para CMake:
   ros2 pkg create --build-type ament_cmake my_package

Estructura generada dentro de ~/dev_ws/src/my_package:
- CMakeLists.txt : Reglas de compilación e instalación para CMake/colcon.
- package.xml    : Metadatos del paquete y lista de dependencias.
- include/       : Para archivos de cabecera C++ (opcional si solo usas Python/Launch).
- src/           : Para código fuente C++ (opcional si solo usas Python/Launch).

====================================================================
PASO 3: AÑADIR ARCHIVOS DE LANZAMIENTO (LAUNCH FILES)
====================================================================
Los launch files permiten ejecutar múltiples nodos con configuraciones predefinidas.

1. Crear la carpeta `launch` dentro de la raíz de `my_package`:
   mkdir -p ~/dev_ws/src/my_package/launch
   cd ~/dev_ws/src/my_package/launch

2. Crear el archivo `talker.launch.py`:
--------------------------------------------------------------------
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_cpp',
            executable='talker'
        )
    ])

3. Crear el archivo `listener.launch.py`:
--------------------------------------------------------------------
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_py',
            executable='listener'
        )
    ])

====================================================================
PASO 4: CONFIGURAR CMakeLists.txt Y package.xml
====================================================================

1. Editar CMakeLists.txt:
--------------------------------------------------------------------
Abre `~/dev_ws/src/my_package/CMakeLists.txt` e inserta la siguiente regla
justo antes de la línea `ament_package()` al final del archivo:

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

* Explicación: Le indica a CMake que copie la carpeta `launch` al directorio
  `share` de ROS 2 para que el comando `ros2 launch` pueda localizar los scripts.

2. Editar package.xml:
--------------------------------------------------------------------
Abre `~/dev_ws/src/my_package/package.xml` e incluye las dependencias necesarias
de ejecución antes del bloque `<export>`:

  <exec_depend>demo_nodes_cpp</exec_depend>
  <exec_depend>demo_nodes_py</exec_depend>

* Opcional: Puedes actualizar campos como <maintainer>, <license> y <description>.

====================================================================
PASO 5: COMPILACIÓN DEL WORKSPACE
====================================================================
Cada vez que agregas un paquete o modificas el CMakeLists.txt, debes compilar:

cd ~/dev_ws
colcon build --symlink-install

====================================================================
PASO 6: SINCRONIZACIÓN CON GIT Y GITHUB
====================================================================
Para compartir el paquete fácilmente entre la Laptop y la Raspberry Pi:

1. Crear un repositorio vacío en GitHub (ej. nombre: `my_package`).
2. Inicializar Git y subir desde la Laptop:
   cd ~/dev_ws/src/my_package
   git init
   git add .
   git commit -m "First Commit"
   git branch -M main
   git remote add origin git@github.com:<TU_USUARIO>/my_package.git
   git push -u origin main

3. Clonar y compilar en la Raspberry Pi:
   cd ~/robot_ws/src
   git clone git@github.com:<TU_USUARIO>/my_package.git
   cd ~/robot_ws
   colcon build --symlink-install

====================================================================
PASO 7: CARGAR EL OVERLAY Y PROBAR LOS LANCHERS
====================================================================
Para que ROS 2 reconozca los paquetes compilados en tu workspace personal,
debes hacer "source" del archivo de configuración del workspace (`install/setup.bash`).

1. En la Raspberry Pi:
   cd ~/robot_ws
   source install/setup.bash
   ros2 launch my_package talker.launch.py

2. En la Laptop (WSL2):
   cd ~/dev_ws
   source install/setup.bash
   ros2 launch my_package listener.launch.py

¡Resultado esperado!
El `listener` en la Laptop comenzará a recibir los mensajes enviados por el
`talker` de la Raspberry Pi mediante el archivo de lanzamiento `my_package`.
====================================================================

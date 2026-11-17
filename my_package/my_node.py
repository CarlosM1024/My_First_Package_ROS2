import rclpy  # Importa la librería principal de ROS 2 para Python.
from rclpy.node import Node  # Importa la clase base Node para crear un nodo ROS 2.

class MyNode(Node):  # Define una nueva clase llamada MyNode que hereda de Node.
    def __init__(self):  # Inicializa el nodo cuando se crea una instancia de MyNode.
        super().__init__('my_node')  # Llama al constructor de Node y crea un nodo con el nombre 'my_node'.
        time_period = 0.5  # Define el tiempo entre llamadas del temporizador en segundos.
        self.timer = self.create_timer(time_period, self.timer_callback)  # Crea un temporizador que ejecuta timer_callback cada 0.5 segundos.

    def timer_callback(self):  # Método que se ejecuta cada vez que el temporizador dispara.
        print('Olis senios desde ROS2')  # Muestra el mensaje por consola.

def main(args=None):  # Define la función principal del programa.
    try:  # Inicia un bloque para manejar errores.
        rclpy.init(args=args)  # Inicializa el cliente de ROS 2 con los argumentos recibidos.
        my_node = MyNode()  # Crea una instancia del nodo MyNode.
        rclpy.spin(my_node)  # Mantiene el nodo vivo y procesa callbacks de ROS 2.
    except KeyboardInterrupt:  # Captura la interrupción del teclado (Ctrl+C).
        print('....exit mode')  # Muestra un mensaje de salida controlada.
    except Exception as e:  # Captura cualquier otra excepción no controlada.
        print(e)  # Muestra el mensaje de error.

if __name__ == '__main__':  # Ejecuta esta sección solo cuando el archivo se ejecuta directamente.
    main()  # Llama a la función principal.

# Este archivo va a crear un nodo que va a contruir un mensaje que va a ser enviado atraves de un topico. 
# Por este mecanismo, otros nodos pueden recibir el mensaje y establecer comunicacion entre dos componentes de sofrware.

import rclpy  # Importa la librería principal de ROS 2 para Python.
from rclpy.node import Node  # Importa la clase base Node para crear un nodo ROS 2.
from std_msgs.msg import String  # Importa el tipo de mensaje String para ROS 2.

time_period = 0.1  # Define el tiempo entre llamadas del temporizador en segundos.

class MyPublisher(Node):  # Define una nueva clase llamada MyPublisher que hereda de Node.
    def __init__(self):  # Inicializa el nodo cuando se crea una instancia de MyPublisher.
        super().__init__('my_publisher')  # Llama al constructor de Node y crea un nodo con el nombre 'my_publisher'.
        self.publisher = self.create_publisher(String, 'my_topic', 10)  # Crea un publicador que enviará mensajes de tipo String al tópico 'my_topic' con una cola de tamaño 10.
        self.timer = self.create_timer(time_period, self.timer_callback)  # Crea un temporizador que ejecuta timer_callback cada 0.12 segundos.
        self.i = 0  # Inicializa un contador para los mensajes enviados.


    def timer_callback(self):  # Método que se ejecuta cada vez que el temporizador dispara.
        msg = String()  # Crea un mensaje de tipo String.
        msg.data = f'Olis senios desde ROS2 numero {self.i} y a velocidad de {time_period}'  # Asigna el texto al mensaje.
        self.publisher.publish(msg)  # Publica el mensaje en el tópico.
        self.get_logger().info(f'Publicando: "{msg.data}"')  # Muestra un mensaje de log con el contenido del mensaje publicado.
        self.i += 1  # Incrementa el contador.

def main(args=None):  # Define la función principal del programa.
    try:  # Inicia un bloque para manejar errores.
        rclpy.init(args=args)  # Inicializa el cliente de ROS 2 con los argumentos recibidos.
        publisher = MyPublisher()  # Crea una instancia del nodo MyPublisher.
        rclpy.spin(publisher)  # Mantiene el nodo vivo y procesa callbacks de ROS 2.
    except KeyboardInterrupt:  # Captura la interrupción del teclado (Ctrl+C).
        print('....exit mode')  # Muestra un mensaje de salida controlada.
    except Exception as e:  # Captura cualquier otra excepción no controlada.
        print(e)  # Muestra el mensaje de error.

if __name__ == '__main__':  # Ejecuta esta sección solo cuando el archivo se ejecuta directamente.
    main()  # Llama a la función principal.

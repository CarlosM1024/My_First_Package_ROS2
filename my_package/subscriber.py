# Este archivo va a crear un nodo que va a contruir un mensaje que va a ser recibido atraves de un topico. 
# Por este mecanismo, otros nodos pueden recibir el mensaje y establecer comunicacion entre dos componentes de sofrware.

import rclpy  # Importa la librería principal de ROS 2 para Python.
from rclpy.node import Node  # Importa la clase base Node para crear un nodo ROS 2.
from std_msgs.msg import String  # Importa el tipo de mensaje String para ROS 2.

class MySubscriber(Node):  # Define una nueva clase llamada MySubscriber que hereda de Node.
    def __init__(self):  # Inicializa el nodo cuando se crea una instancia de MySubscriber.
        super().__init__('my_subscriber')  # Llama al constructor de Node y crea un nodo con el nombre 'my_subscriber'.
        self.subscription = self.create_subscription(String, 'my_topic', self.listener_callback, 10)  # Crea una suscripción al tópico 'my_topic' con una cola de tamaño 10.

    def listener_callback(self, msg):  # Método que se ejecuta cada vez que se recibe un mensaje en el tópico.
        self.get_logger().info(f'Recibiendo: "{msg.data}"')  # Muestra un mensaje de log con el contenido del mensaje recibido.
    

def main(args=None):  # Define la función principal del programa.
    try:  # Inicia un bloque para manejar errores.
        rclpy.init(args=args)  # Inicializa el cliente de ROS 2 con los argumentos recibidos.
        subscriber = MySubscriber()  # Crea una instancia del nodo MySubscriber.
        rclpy.spin(subscriber)  # Mantiene el nodo vivo y procesa callbacks de ROS 2.
    except KeyboardInterrupt:  # Captura la interrupción del teclado (Ctrl+C).
        print('....exit mode')  # Muestra un mensaje de salida controlada.
    except Exception as e:  # Captura cualquier otra excepción no controlada.
        print(e)  # Muestra el mensaje de error.

if __name__ == '__main__':  # Ejecuta esta sección solo cuando el archivo se ejecuta directamente.
    main()  # Llama a la función principal.

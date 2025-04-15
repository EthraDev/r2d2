import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
from pynput import keyboard


class ManagerNode(Node):
    def __init__(self):
        # Initialise le noeud ROS2 avec le nom 'manager_node'
        super().__init__('manager_node')
        
        # Crée un éditeur pour publier des messages sur le topic 'topic_cmd'
        self.publisher_ = self.create_publisher(String, 'topic_cmd', 3)
        
        # Variable pour stocker la touche actuellement pressée
        self.current_key = None
        
        # Crée un timer pour appeler la méthode publish_command toutes les secondes
        self.timer = self.create_timer(1.0, self.publish_command)
        
        # Initialise un écouteur pour détecter les événements clavier
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def publish_command(self):
        # Génère une commande en fonction de la touche pressée
        if self.current_key == keyboard.Key.up:
            command = {'left': 100, 'right': 100}  # Avancer
        elif self.current_key == keyboard.Key.down:
            command = {'left': -100, 'right': -100}  # Reculer
        elif self.current_key == keyboard.Key.left:
            command = {'left': 100, 'right': -100}  # Tourner à gauche
        elif self.current_key == keyboard.Key.right:
            command = {'left': -100, 'right': 100}  # Tourner à droite
        else:
            # Pas de touche pressée : stop
            command = {'left': 0, 'right': 0}
        
        # Crée un message ROS2 de type String et publie la commande
        msg = String()
        msg.data = json.dumps(command)
        self.publisher_.publish(msg)
        
        # Affiche le message publié dans les logs
        self.get_logger().info(f"Published: {msg.data}")

    def on_press(self, key):
        # Met à jour la touche actuellement pressée
        print(key)  # Affiche la touche pressée dans la console
        self.current_key = key

    def on_release(self, key):
        # Réinitialise la touche actuelle si 'esc' est relâchée
        if key == keyboard.Key.esc:
            self.current_key = None


def main(args=None):
    # Initialise le contexte ROS2
    rclpy.init(args=args)
    
    # Crée une instance du noeud et démarre la boucle ROS2
    node = ManagerNode()
    rclpy.spin(node)
    
    # Détruit le noeud et arrête ROS2 proprement
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

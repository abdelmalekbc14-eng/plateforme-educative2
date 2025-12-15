import pika
import json

def process_message(ch, method, properties, body):
    # Décodage du message
    data = json.loads(body.decode())
    print(f"Notification reçue : {data}")

    # Exemple : on peut logguer dans un fichier, envoyer un email ou enregistrer à la base de données
    # Ici, on va juste afficher dans la console pour tester
    print(f"Message traité : L'étudiant {data['etudiant_email']} est inscrit au cours {data['cours_titre']}.")

    # Confirmer que le message a été traité
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Connexion à RabbitMQ et déclaration de la queue
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Déclare la queue 'inscriptions' si elle n'existe pas
channel.queue_declare(queue='inscriptions', durable=True)

# Consommer les messages
channel.basic_consume(queue='inscriptions', on_message_callback=process_message)

print("En attente de messages...")
channel.start_consuming()

from django.core.management.base import BaseCommand
import pika
import json
from django.conf import settings
from platforme_educatif.settings import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASS

class Command(BaseCommand):
    help = 'Runs the RabbitMQ consumer worker for Notifications'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting RabbitMQ Consumer..."))
        
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
            channel = connection.channel()

            channel.queue_declare(queue='inscriptions', durable=True)

            def process_message(ch, method, properties, body):
                try:
                    data = json.loads(body.decode())
                    self.stdout.write(f"Notification reçue : {data}")
                    
                    # Logic: Log/Send Email etc.
                    print(f"Message traité : L'étudiant {data.get('etudiant_email')} est inscrit au cours {data.get('cours_titre')}.")
                    
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing message: {e}"))
                    ch.basic_nack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue='inscriptions', on_message_callback=process_message)
            
            self.stdout.write("En attente de messages...")
            channel.start_consuming()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Critical RabbitMQ Error: {e}"))

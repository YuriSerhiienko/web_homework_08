import pika
from mongoengine import connect, Document, StringField, BooleanField
import time

# Підключення до MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

# Визначення моделі контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

# Функція для імітації надсилання листів
def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Надсилаю листа на {contact.email}")
        time.sleep(1)  # Імітуємо процес відправки листа
        contact.sent = True
        contact.save()

# Встановлення з'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')

# Функція, яка викликається при отриманні повідомлення з черги
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email(contact_id)
    print(f"Повідомлення для контакту з ID {contact_id} оброблено")

# Вказуємо, що функція callback буде використовуватися для обробки повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print("Чекаю на повідомлення. Для виходу натисніть CTRL+C")
channel.start_consuming()

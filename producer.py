import pika
import random
import string
from mongoengine import connect, Document, StringField, BooleanField

# Підключення до MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

# Визначення моделі контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

# Встановлення з'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів та запис до бази даних
for _ in range(10):
    fullname = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(10))
    email = f"{fullname}@example.com"
    contact = Contact(fullname=fullname, email=email)
    contact.save()

    # Публікація повідомлення в чергу
    channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))

print("Фейкові контакти збережено та відправлено в чергу")

connection.close()

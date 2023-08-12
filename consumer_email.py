import pika
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

# Встановлення з'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Оголошення черги для Email
channel.queue_declare(queue='email_queue')

# Функція для імітації надсилання Email
def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Надсилаю Email до контакту {contact.fullname} на адресу {contact.email}")
        # Тут може бути логіка для надсилання Email

# Функція, яка викликається при отриманні повідомлення з черги Email
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email(contact_id)
    print(f"Повідомлення для контакту з ID {contact_id} оброблено")

# Вказуємо, що функція callback буде використовуватися для обробки повідомлень з черги Email
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print("Чекаю на повідомлення Email. Для виходу натисніть CTRL+C")
channel.start_consuming()

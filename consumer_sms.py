import pika
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

# Встановлення з'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Оголошення черги для SMS
channel.queue_declare(queue='sms_queue')

# Функція для імітації надсилання SMS
def send_sms(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Надсилаю SMS до контакту {contact.fullname} на номер {contact.phone}")
        # Тут може бути логіка для надсилання SMS

# Функція, яка викликається при отриманні повідомлення з черги SMS
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_sms(contact_id)
    print(f"Повідомлення для контакту з ID {contact_id} оброблено")

# Вказуємо, що функція callback буде використовуватися для обробки повідомлень з черги SMS
channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print("Чекаю на повідомлення SMS. Для виходу натисніть CTRL+C")
channel.start_consuming()

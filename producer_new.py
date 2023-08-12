import pika
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

# Встановлення з'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Оголошення черги для SMS та Email
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')

# Створення фейкових контактів і запис до бази даних
contacts = [
    {
        "fullname": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "send_email": True,
        "send_sms": False,
        "preferred_method": "email"
    },
    {
        "fullname": "Jane Smith",
        "email": "jane@example.com",
        "phone": "9876543210",
        "send_email": True,
        "send_sms": False,
        "preferred_method": "email"
    },
    {
        "fullname": "Bob Johnson",
        "email": "bob@example.com",
        "phone": "5555555555",
        "send_email": False,
        "send_sms": True,
        "preferred_method": "sms"
    },
    {
        "fullname": "Alice Williams",
        "email": "alice@example.com",
        "phone": "8888888888",
        "send_email": False,
        "send_sms": True,
        "preferred_method": "sms"
    },
    {
        "fullname": "Michael Brown",
        "email": "michael@example.com",
        "phone": "7777777777",
        "send_email": False,
        "send_sms": True,
        "preferred_method": "sms"
    }
]

for contact_data in contacts:
    contact = Contact(**contact_data)
    contact.save()
    contact_id = str(contact.id)

    # Визначення черги для кожного контакту
    if contact.preferred_method == "email":
        queue_name = 'email_queue'
    else:
        queue_name = 'sms_queue'

    # Відправка ID контакту до черги
    channel.basic_publish(exchange='', routing_key=queue_name, body=contact_id)
    print(f"Контакт з ID {contact_id} додано до черги {queue_name}")

connection.close()

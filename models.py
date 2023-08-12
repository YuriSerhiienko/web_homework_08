from mongoengine import Document, StringField, ReferenceField, ListField
from mongoengine import BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    send_email = BooleanField(default=False)
    send_sms = BooleanField(default=False)
    preferred_method = StringField(choices=['email', 'sms'], default='email')

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

import json
from mongoengine import connect
from models import Author, Quote

# Підключення до хмарної бази даних MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")
# Завантаження даних з JSON-файлів
with open('authors.json', 'r') as authors_file:
    authors_data = json.load(authors_file)

with open('quotes.json', 'r') as quotes_file:
    quotes_data = json.load(quotes_file)

# Заповнення бази даних
for author_data in authors_data:
    author = Author(**author_data)
    author.save()

for quote_data in quotes_data:
    author_name = quote_data['author']
    author = Author.objects(fullname=author_name).first()
    if author:
        quote_data['author'] = author
        quote = Quote(**quote_data)
        quote.save()

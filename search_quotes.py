from mongoengine import connect
from models import Author, Quote

# Підключення до хмарної бази даних MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

while True:
    command = input("Введіть команду: ")
    if command == "exit":
        break
    elif command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print("Цитата:", quote.quote)
                print("Теги:", ", ".join(quote.tags))
                print("-" * 50)
        else:
            print("Автор не знайдений.")
    elif command.startswith("tag:"):
        tag = command.split(":")[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print("Автор:", quote.author.fullname)
            print("Цитата:", quote.quote)
            print("-" * 50)
    elif command.startswith("tags:"):
        tags = command.split(":")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print("Автор:", quote.author.fullname)
            print("Цитата:", quote.quote)
            print("Теги:", ", ".join(quote.tags))
            print("-" * 50)
    else:
        print("Невідома команда.")

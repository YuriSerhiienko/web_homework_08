import redis
from mongoengine import connect
from models import Author, Quote


# Підключення до MongoDB
connect(host="mongodb+srv://goitlearn:mO4zR0BhYNRTFQTH@cluster0.hi5rlnt.mongodb.net/?retryWrites=true&w=majority")

# Підключення до Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_quotes_by_author_name(author_name):
    # Спробувати отримати дані з Redis
    cached_quotes = redis_client.get(f'author_{author_name}')
    if cached_quotes:
        return cached_quotes.decode('utf-8')

    author = Author.objects(fullname__icontains=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        result = ''
        for quote in quotes:
            result += f"Цитата: {quote.quote}\n"
            result += f"Теги: {', '.join(quote.tags)}\n"
            result += "-" * 50 + "\n"

        # Зберегти дані в Redis
        redis_client.setex(f'author_{author_name}', 3600, result.encode('utf-8'))
        return result
    else:
        return "Автор не знайдений."

def get_quotes_by_tag(tag):
    # Спробувати отримати дані з Redis
    cached_quotes = redis_client.get(f'tag_{tag}')
    if cached_quotes:
        return cached_quotes.decode('utf-8')

    quotes = Quote.objects(tags__icontains=tag)
    result = ''
    for quote in quotes:
        result += f"Автор: {quote.author.fullname}\n"
        result += f"Цитата: {quote.quote}\n"
        result += "-" * 50 + "\n"

    # Зберегти дані в Redis
    redis_client.setex(f'tag_{tag}', 3600, result.encode('utf-8'))
    return result

while True:
    command = input("Введіть команду: ")
    if command == "exit":
        break
    elif command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        if len(author_name) >= 2:
            result = get_quotes_by_author_name(author_name)
            print(result)
        else:
            print("Занадто коротке ім'я автора.")
    elif command.startswith("tag:"):
        tag = command.split(":")[1].strip()
        if len(tag) >= 2:
            result = get_quotes_by_tag(tag)
            print(result)
        else:
            print("Занадто коротий тег.")
    else:
        print("Невідома команда.")

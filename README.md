# Assistant Bot - Персональний асистент для управління контактами

Консольний асистент-бот для управління контактами з підтримкою телефонів, email, адрес та днів народження.

## Встановлення з TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple assistant-bot-G30
```

## Запуск

```bash
assistant-bot-G30
```

## Встановлення з GitHub

```bash
git clone https://github.com/LesDevLabs/project-group-30.git
cd project-group-30
pip install -r requirements.txt
py main.py
```

## Основні можливості

✅ Управління контактами (додавання, редагування, видалення)  
✅ Збереження телефонів, email, адрес та днів народження  
✅ Пошук контактів за ім'ям, телефоном або email  
✅ Підтримка різних форматів збереження (Pickle, JSON)  
✅ Кольоровий інтерфейс з colorama  
✅ Автодоповнення команд  
✅ Валідація введених даних  
✅ Обробка помилок без закриття програми  

## Команди

### Управління контактами
- `add` - Додати новий контакт (інтерактивний режим)
- `show <name>` - Показати конкретний контакт
- `all` - Показати всі контакти
- `search-contacts <query>` - Пошук контактів
- `rename <old-name> <new-name>` - Перейменувати контакт
- `delete <name>` - Видалити контакт

### Управління телефонами
- `change <name> <old-phone> <new-phone>` - Змінити телефон
- `delete-phone <name> <phone>` - Видалити телефон

### Інше
- `help` - Показати всі команди
- `exit` / `quit` / `close` - Вийти з програми

## Приклад використання

```bash
# Додати контакт (інтерактивно)
> add
Name(required): John
Phone (optional): 1234567890
Email (optional): john@example.com
Address (optional): 123 Main St
Birthday (optional, dd.mm.yyyy): 01.01.1990

# Показати контакт
> show John

# Пошук контактів
> search-contacts john

# Змінити телефон
> change John 1234567890 0987654321

# Показати всі контакти
> all
```

## Структура проекту

```
project-group-30/
├── cli/                    # CLI компоненти
│   ├── presenter.py        # Кольоровий вивід
│   └── command_suggester.py # Підказки команд
├── handlers/               # Обробники команд
│   ├── command_handler.py  # Основний обробник
│   └── decorators.py       # Декоратори помилок
├── models/                 # Моделі даних
│   ├── contact.py          # Record
│   ├── name.py             # Name
│   ├── phone.py            # Phone
│   ├── email.py            # Email
│   ├── address.py          # Address
│   └── birthday.py         # Birthday
├── repositories/           # Репозиторії
│   └── contact_repository.py
├── storage/                # Збереження даних
│   ├── pickle_storage.py
│   └── json_storage.py
├── search/                 # Пошук
│   └── search_service.py
├── utils/                  # Утиліти
│   └── utils.py
└── main.py                 # Точка входу
```

## Вимоги

- Python 3.8 або вище
- colorama
- rich

## Розробка

```bash
# Створити venv
py -m venv venv

# Активувати venv (Windows)
venv\Scripts\activate.bat

# Встановити залежності
pip install -r requirements.txt

# Запустити
py main.py
```

## Ліцензія

MIT License

## Автори

Group 30 (2025)
- lestyshchenko
- Sagepol
- 444ten
- Koliaepov
- Valerian Demichev
- Zarudenska

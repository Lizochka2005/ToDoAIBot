import re
import json


a = {
    "intent": "Создать задачу",
    "params": {
        "date": "2025-03-22",  # если пользователь не указал дату, установи сегодняшнюю
        "time": "18:00",
        "task": "Купить молоко",
        "status": "Не выполнено",
        "query": "None",
        "notifications": "None",
        "username": None,
        "language": "None",
    },
}
print(a)
print(a["intent"])
print(a["params"])
print(a["params"]["date"])
print(a["params"]["time"])
print(a["params"]["task"])
print(a["params"]["status"])
print(a["params"]["query"])
print(a["params"]["notifications"])
print(a["params"]["username"])
print(a["params"]["language"])
b = """
{
    "intent": "Создать задачу",
    "params": {
        "date": "2025-03-22",
        "time": "18:00",
        "task": "Купить молоко",
        "status": "Не выполнено",
        "query": "None",
        "notifications": "None",
        "username": "None",
        "language": "None",
    },
}
"""

def raw_str_to_dict(s):
    # Удаляем все лишние запятые перед закрывающими скобками
    fixed = re.sub(r',\s*(?=}|])', '', s)
    return json.loads(fixed)

b = raw_str_to_dict(b)

print()
print(b)
print(b["intent"])
print(b["params"])
print(b["params"]["date"])
print(b["params"]["time"])
print(b["params"]["task"])
print(b["params"]["status"])
print(b["params"]["query"])
print(b["params"]["notifications"])
print(b["params"]["username"])
print((b["params"]["language"]))

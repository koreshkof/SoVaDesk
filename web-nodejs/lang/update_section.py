#!/usr/bin/env python3
"""
Скрипт для обновления секции в ru.json.
Использование:
    python3 update_section.py <section> <json_file>
    
Пример:
    python3 update_section.py common translated_common.json
"""
import json
import sys

if len(sys.argv) != 3:
    print("Использование: python3 update_section.py <section> <json_file>")
    sys.exit(1)

section = sys.argv[1]
json_file = sys.argv[2]

# Загрузить ru.json
with open('ru.json', 'r', encoding='utf-8') as f:
    ru_data = json.load(f)

# Загрузить переведённую секцию
with open(json_file, 'r', encoding='utf-8') as f:
    translated = json.load(f)

# Обновить секцию
ru_data[section] = translated

# Сохранить
with open('ru.json', 'w', encoding='utf-8') as f:
    json.dump(ru_data, f, ensure_ascii=False, indent=4)

print(f"Секция '{section}' обновлена")

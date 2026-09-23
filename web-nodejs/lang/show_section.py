#!/usr/bin/env python3
"""
Показать секцию из en.json в красивом виде.
Использование:
    python3 show_section.py <section>
"""
import json
import sys

if len(sys.argv) != 2:
    print("Использование: python3 show_section.py <section>")
    sys.exit(1)

section = sys.argv[1]

with open('en.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if section not in data:
    print(f"Секция '{section}' не найдена")
    sys.exit(1)

print(json.dumps(data[section], indent=4, ensure_ascii=False))

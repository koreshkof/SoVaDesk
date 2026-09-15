<div align="center">

# SoVa Desk

### Российская платформа удалённого администрирования

**Полный контроль над удалённым парком. Без подписок и облаков.**

<img src="sova.png" alt="SoVa Desk" width="640">

<br>

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.5.4-brightgreen.svg)](CHANGELOG.md)

**[Русский](README.md) • [English](README.en.md)**

</div>

---

## 📖 О платформе

**SoVa Desk** — это полноценная инфраструктура удалённого администрирования, развёрнутая **на вашей инфраструктуре**. Один Go-бинарник заменяет `hbbs` и `hbbr`, работает с SQLite или PostgreSQL, поддерживает TLS везде и предоставляет полноценный REST API.

**Для кого:**
- Компании, которые хотят **контролировать свой парк устройств** без зависимости от зарубежных облаков.
- Интеграторы и MSP, которым нужен **white-label продукт** для перепродажи.
- Госсектор и энтерпрайз, которым важна **автономность** и **аудит**.

**Чем отличается:**
- **Протокол RustDesk** — полная совместимость с существующими клиентами.
- **Один бинарник** — проще деплой, меньше точек отказа.
- **Российская платформа** — работает без VPN, соответствует требованиям регуляторов.
- **OEM-сборки** — выпускаем клиенты под вашим брендом.

---

## ✨ Ключевые возможности

### Один бинарник вместо двух
Один Go-бинарник заменяет `hbbs` (signal) + `hbbr` (relay). Проще деплой, меньше точек отказа, быстрее старт.

### База данных под задачу
**SQLite** — для малого парка (до 500 устройств, всё в одном файле). **PostgreSQL** — для продакшена (миллионы записей, репликация, LISTEN/NOTIFY). Один бинарник, два режима.

### TLS везде
Signal, relay, API, веб-консоль — всё шифруется. Dual-mode listener принимает TLS и plain на **одном порту** — старые клиенты работают без перенастройки.

### Полноценный REST API
JWT + API-ключи, REST-эндпоинты для всего, что видно в UI. Интеграция с биллингом, SIEM, мониторингом — без хаков.

### Multi-instance через PostgreSQL
LISTEN/NOTIFY для real-time синхронизации между инстансами. Горизонтальное масштабирование.

### E2E шифрование
NaCl handshake между RustDesk-клиентами. Опциональный TLS на relay-портах для дополнительной защиты.

### RBAC — 4 роли
Admin, Operator, Viewer, Pro. Гибкая система прав — от полного доступа до read-only.

### TOTP 2FA
RFC 6238, совместим с Google Authenticator, Authy, 1Password.

### Удалённый доступ через браузер
H.264 через WebCodecs, JMuxer fallback. Не нужен клиент — только браузер.

### File transfer
Передача файлов через браузер с прогресс-баром и историей.

### Wake-on-LAN
Удалённое включение устройств через magic packet.

### CDAP — Connected Device Automation Protocol
Управление IoT, ICS, SCADA-устройствами через единый интерфейс.

---

## 🏗️ Архитектура


```
┌─────────────────────────────────────────────────────────────┐
│           Клиенты (Windows, macOS, Linux, Android)          │
└────────────┬────────────────────────────────────────────────┘
             │
             │ UDP/TCP/WS
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    SoVa Desk Server (Go)                    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Signal :21116│  │ Relay :21117 │  │ API :21114/21121 │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ WS Signal    │  │ WS Relay     │  │ NAT test :21115  │   │
│  │ :21118       │  │ :21119       │  │                  │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         База данных (SQLite / PostgreSQL)            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP :5000
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Веб-консоль (Node.js + Express + EJS)             │
│  • Dashboard  • Devices  • Users  • Settings  • Chat        │
└─────────────────────────────────────────────────────────────┘
```

### Порты

| Порт | Протокол | Сервис |
|------|----------|--------|
| **21115** | TCP | NAT test + OnlineRequest |
| **21116** | TCP + UDP | Signal (регистрация, punch hole) |
| **21117** | TCP | Relay (bidirectional stream) |
| **21118** | WS(S) | WebSocket Signal |
| **21119** | WS(S) | WebSocket Relay |
| **21114** | HTTP | Go API (RustDesk + REST) |
| **21121** | HTTP | Go API (обратная совместимость) |
| **5000** | HTTP | Веб-консоль |
| **21122** | WS | CDAP (IoT) |

> Все TCP/WS-порты поддерживают **dual-mode TLS** — plain и TLS на одном порту с автоопределением.

---

## 🎨 OEM-сборки клиентов

SoVa Desk поставляет **брендированные клиенты под вашу компанию**:

- Свой логотип, название, палитра в окне клиента.
- Свой домен для ID/Relay-сервера (вшит в конфиг).
- Свой установщик (.msi / .exe / .dmg / .apk) с вашей иконкой.
- Автоконфигурация: пользователь ставит клиент — и он сразу подключается к вашему серверу.
- **Доступно для Windows x64/x86, macOS (Intel + Apple Silicon), Linux, Android.**

Сборка под OEM — **отдельная услуга**. Свяжитесь с нами для расчёта.

**Что даёт:** ваши сотрудники и клиенты видят **только ваш бренд**, никаких упоминаний upstream.

---

## 💼 Лицензирование

SoVa Desk работает по **гибкой модели** — выбирайте, что подходит вашей инфраструктуре.

### Варианты

**1. SaaS-подписка** — работайте на нашем сервере. Платите за активных клиентов.

**2. Серверная лицензия** — разверните SoVa Desk на своей инфраструктуре. Единоразовая лицензия, без ограничений по устройствам. Обновления — по подписке.

**3. OEM** — перепродавайте SoVa Desk под своим брендом. White-label, полный ребрендинг, автономные обновления.

### Тарифы

| Тариф | Что входит | Стоимость |
|-------|-----------|-----------|
| **Пробный** | 5 устройств, 14 дней, полный доступ | Бесплатно |
| **Команда** | До 50 устройств, 1 админ, поддержка email | Скоро будут |
| **Бизнес** | До 500 устройств, 10 админов, SLA, приоритет | Скоро будут |
| **Серверная лицензия** | 1 инсталляция сервера, безлимит устройств, 1 админ, поддержка email, обновления | Скоро будут |
| **OEM** | White-label, право перепродажи | Скоро будут |
| **Корпоративный** | On-premise, кастомные фичи, аудит | Индивидуально |

### Активация

Лицензия привязывается к **ID клиента**. Активация:


```bash
sudo sova activate <ID_КЛИЕНТА> <ДНИ>
```

Или в веб-консоли: **Dashboard → Devices → Activate**.

### Что входит

- **Обновления** — минорные и мажорные версии.
- **Поддержка** — email / Telegram (SLA по тарифу).
- **Миграция** — поможем переехать с RustDesk, TeamViewer, AnyDesk.

### Оплата

- **Рубли** — СБП, карта, для юрлиц — по счёту.
- **Крипта** — USDT, BTC.

---

## 📦 Установка

### Требования

| Компонент | Версия |
|-----------|--------|
| **ОС** | Ubuntu 22.04+, Debian 12+, CentOS 8+, Docker |
| **Go** | 1.21+ (устанавливается скриптом) |
| **Node.js** | 18+ (устанавливается скриптом) |
| **PostgreSQL** | 14+ (опционально, SQLite по умолчанию) |

### Docker (рекомендуется)

**Быстрый старт:**


```bash
curl -fsSL https://raw.githubusercontent.com/koreshkof/SoVaDesk/main/docker-compose.quick.single.yml -o docker-compose.yml
docker compose pull && docker compose up -d
docker compose exec sova-desk sova-show-admin-credentials
```

Откройте **http://localhost:5000** — API на порту **21121**.

**Сборка из исходников:**


```bash
git clone https://github.com/koreshkof/SoVaDesk.git
cd SoVaDesk

# Сборка образа
docker build -t sova-desk:3.5.94 .

# Запуск
docker compose -f docker-compose.single.yml up -d
```

### Native (без Docker)


```bash
git clone https://github.com/koreshkof/SoVaDesk.git
cd SoVaDesk

# Интерактивная установка
sudo ./sova.sh

# Автоматическая установка
sudo ./sova.sh --auto
```

Скрипт:
1. Установит Go и Node.js (если нет).
2. Соберёт `sova-server` из исходников.
3. Создаст systemd-сервисы.
4. Сгенерирует Ed25519-ключи.
5. Создаст админа (пароль в `.admin_credentials`).
6. Запустит сервисы.

### Что установится


```
/srv/sova-desk/
├── sova-server              # Go-бинарник (signal + relay + API)
├── id_ed25519               # Ed25519 приватный ключ
├── id_ed25519.pub           # Публичный ключ
├── db_v2.sqlite3            # SQLite БД
├── .admin_credentials       # Пароль админа
├── .api_key                 # API-ключ
└── web-console/             # Node.js консоль
```

---

## 🖥️ Настройка клиента

### Windows / macOS / Linux

1. Откройте **SoVa Desk клиент** (или RustDesk для совместимости).
2. **Меню (≡) → Network → ID/Relay Server**.
3. Заполните:

| Поле | Значение |
|------|----------|
| **ID Server** | `94.19.29.19` или ваш домен |
| **Relay Server** | То же (или пусто для auto-detect) |
| **API Server** | `http://94.19.29.19:21121` |
| **Key** | Содержимое `id_ed25519.pub` |

4. Войдите под аккаунтом (**иконка профиля → Login**) — активируются Pro-функции.

### Android

1. Скачайте **SoVa Desk для Android** (APK).
2. Установите, откройте.
3. Введите **ID Server**, **Relay Server**, **Key**.
4. Войдите под аккаунтом.

### Получение ключа

Ключ (`id_ed25519.pub`) находится:
- В веб-консоли: **Dashboard → Server Keys**.
- На сервере: `cat /srv/sova-desk/id_ed25519.pub`.
- В контейнере: `docker exec sova-desk cat /opt/rustdesk/id_ed25519.pub`.

---

## 📡 API

### Аутентификация


```bash
# JWT
curl -H "Authorization: Bearer <token>" http://localhost:21114/api/peers

# API-ключ
curl -H "X-API-Key: <key>" http://localhost:21114/api/peers
```

### Публичные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/health` | Healthcheck |
| GET | `/api/server/stats` | Статистика сервера |
| GET | `/api/server/pubkey` | Публичный ключ Ed25519 |
| GET | `/metrics` | Prometheus метрики |
| POST | `/api/auth/login` | Логин → JWT |

### Эндпоинты для клиентов

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/login` | Логин RustDesk-клиента |
| GET/POST | `/api/currentUser` | Информация о текущем пользователе |
| GET/POST | `/api/ab` | Адресная книга |
| POST | `/api/heartbeat` | Heartbeat клиента |
| POST | `/api/sysinfo` | Информация о системе |

### Admin-эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/peers` | Список устройств |
| POST | `/api/peers/{id}/ban` | Забанить устройство |
| POST | `/api/peers/{id}/unban` | Разбанить |
| POST | `/api/peers/{id}/change-id` | Сменить ID устройства |
| GET/POST | `/api/users` | CRUD пользователей |
| POST | `/api/users/{id}/totp/setup` | Настроить TOTP |
| GET/PUT | `/api/enrollment/mode` | Режим enrollment |
| POST | `/api/peers/{id}/wol` | Wake-on-LAN |

---

## 📊 Мониторинг и безопасность

### Prometheus метрики

Доступны на `GET /metrics`:


```
sova_registrations_total
sova_expired_total
sova_relay_sessions_total
sova_relay_bytes_total
sova_uptime_seconds
sova_peers_total
sova_peers_online
sova_peers_degraded
sova_peers_critical
sova_peers_offline
sova_peers_banned
sova_relay_active_sessions
sova_goroutines
sova_memory_alloc_bytes
```

### Аудит

Включите файловый аудит:


```bash
./sova-server -audit-log /var/log/sova/audit.jsonl
```

Логируются: логины, ошибки auth, баны, изменения конфига, ID-изменения, blocklist.

### Безопасность

| Компонент | Реализация |
|-----------|------------|
| **Transport** | NaCl secretbox, TLS 1.2+, WSS |
| **Пароли** | PBKDF2-HMAC-SHA256, 100K итераций |
| **JWT** | HS256, constant-time verification |
| **TOTP 2FA** | RFC 6238, ±1 step |
| **API** | JWT + API-ключи (SHA256) |
| **Input validation** | Peer ID, config key — regex |
| **SQL injection** | Parameterized queries only |
| **Rate limiting** | Per-IP sliding window |
| **Bandwidth** | Token bucket (1 GB/s global, 16 MB/s per-session) |
| **Audit** | Ring buffer 10K + JSON file |

---

## ❓ FAQ

### Какой протокол используется?

SoVa Desk реализует **публичный протокол RustDesk** для совместимости с существующими клиентами. Исходный код RustDesk **не используется**.

### Можно ли использовать оригинальный RustDesk-клиент?

Да. SoVa Desk **совместим** с RustDesk-клиентами v1.1.9+. Для полного брендинга рекомендуем **наши OEM-сборки**.

### Где хранятся ключи?

`id_ed25519` (приватный) и `id_ed25519.pub` (публичный) — в `/srv/sova-desk/`. **Обязательно сделайте бэкап** — потеря ключей отключит все клиенты.

### Как мигрировать с RustDesk?


```bash
cd sova-server/tools/migrate
go build -o migrate .
./migrate -mode rust2go -src /opt/rustdesk/db_v2.sqlite3 -dst /srv/sova-desk/db_v2.sqlite3
```

### Как обновить?

**Docker:**

```bash
docker compose pull
docker compose up -d
```

**Native:**

```bash
cd /srv/sova-desk
git pull
sudo ./sova.sh --update
```

### Как сменить пароль админа?


```bash
docker exec sova-desk sova-reset-admin-password
```

Или через веб-консоль: **Settings → Users → Admin → Reset Password**.

### Где логи?

- **Docker:** `docker logs sova-desk`
- **Native:** `journalctl -u sova-server -u sova-console`
- **Supervisor:** `/var/log/supervisor/`

### Какая минимальная конфигурация?

- **1 vCPU, 1 ГБ RAM** — для малого парка (до 50 устройств).
- **2 vCPU, 2 ГБ RAM** — для среднего (до 500).
- **4 vCPU, 4 ГБ RAM** — для крупного (500+).

---

## 📞 Контакты

- **Email:** [будет указан]
- **Telegram:** [будет указан]
- **Сайт:** [будет указан]

---

## 📄 Лицензия

SoVa Desk распространяется под **GNU GPL v3** — это обеспечивает свободу сообщества и открытость кода.

**Коммерческое лицензирование:** Для использования в проприетарных продуктах и OEM-сборках доступна **коммерческая лицензия**. Свяжитесь с нами для получения подробной информации.

---

*SoVa Desk является независимым продуктом. Мы реализуем опубликованный протокол RustDesk для совместимости с клиентами, но не содержаем исходный код RustDesk. Название «RustDesk» используется исключительно в описательных целях (совместимость с протоколом) и не подразумевает связи с командой RustDesk.*

---

<div align="center">

**Сделано с ❤️ командой SoVa**

</div>

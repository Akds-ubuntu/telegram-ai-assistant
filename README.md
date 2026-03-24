# 🤖 AI Tech Interviewer Bot

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg?logo=telegram)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)

Асинхронный Telegram-бот для автоматизированного проведения технических собеседований. Бот использует AI для оценки ответов кандидата, поддерживает голосовой ввод и умеет задавать наводящие вопросы в реальном времени, если ответ неполный.

## Что делает проект?

* **Умное тестирование:** Проводит квизы по различным категориям (SQL, Python и др.).
* **Voice-to-Text:** Принимает ответы голосовыми сообщениями и транскрибирует их с высокой точностью. Использует модель "nova-3" от Deepgram.
* **LLM-Оценка:** Анализирует ответ пользователя с помощью нейросетей, сравнивает с эталоном и дает развернутый фидбек. Используется модель gpt-oss-120b от Groq
* **Адаптивные сценарии (FSM):** При неполном ответе переводит пользователя в состояние follow-up, задавая до 3 уточняющих вопросов.
* **REST API Интеграция:** Позволяет загружать новые пачки вопросов в формате JSON.

##  Архитектура и как это работает

Проект спроектирован с упором на отказоустойчивость, высокую производительность и готовность к production-нагрузкам.

1.  **Связка FastAPI + Aiogram:** Бот работает не на медленном Long Polling, а на **Webhooks**. FastAPI поднимает сервер, который мгновенно принимает POST-запросы от серверов Telegram и передает их в диспетчер Aiogram.
2.  **Асинхронное ядро:** Вся работа с базой данных (SQLAlchemy) и внешними API (LLM, STT) выполняется полностью асинхронно, не блокируя Event Loop.
3.  **Dependency Injection:** Передача сессий БД и конфигураций в хендлеры реализована через middleware, что делает код чистым и легко тестируемым.

##  Технологический стек

* **Backend:** Python, FastAPI, Aiogram 3.x
* **База данных:** PostgreSQL, SQLAlchemy (Async), Alembic (миграции)
* **AI / ML:** LangChain, Deepgram API (для распознавания речи)
* **Инфраструктура:** Docker, Docker Compose

##  Деплой и Инфраструктура (Production)

Проект развернут на VPS с использованием современного подхода к оркестрации:

* **Dokploy (PaaS):** Используется для CI/CD и управления жизненным циклом контейнеров. При пуше в главную ветку происходит автоматическая пересборка и обновление сервиса (Zero-Downtime Deployment).
* **Traefik (Reverse Proxy):** Выступает в роли пограничного шлюза. Автоматически маршрутизирует трафик к контейнерам и управляет **Let's Encrypt SSL-сертификатами**, что критически важно для безопасной работы Webhooks от Telegram.

---
<h3 align="center"> Интерфейс бота</h3>
<p align="center">
  <img src="assets/screenshot_main.png" width="40%" title="Главное меню">
  <img src="assets/screenshot_main1.png" width="40%" title="Выбор режима">
  <img src="assets/screenshot_main2.png" width="40%" title="Выбор вопроса">
</p>
<p align="center">
  <img src="assets/screenshot_main3.png" width="40%" title="Превью вопроса">
  <img src="assets/screenshot_main4.png" width="40%" title="Ответ на вопрос">
  <img src="assets/screenshot_main5.png" width="40%" title="Доп вопрос">
</p>

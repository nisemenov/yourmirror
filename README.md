Добро пожаловать в репозиторий [yourmirror](https://yourmirror.ru).

[yourmirror](https://yourmirror.ru) — сервис, где пользователи могут вести вишлисты, делиться ими и подписываться на чужие списки.

Ключевые ценности:
- open source
- минимализм
- дружелюбный телеграм-бот
- никакой рекламы

## ⚙️ Tech stack

**TL;DR: uv, Django, PostgreSQL, Redis, Celery, Tailwind, MinIO**

При выборе стэка я отталкивался от своей экспертизы и максимальной простоты.

Основные моменты:
- здесь нет полноценного frontend'а, вместо этого используются стандартные джанго-шаблоны (DTL), а для пущей красоты и удобства — [Tailwind](https://tailwindcss.com/);
- для взаимодействия дополнительных сервисов на уровне менеджмента пакетов использую [супер быстрый uv](https://docs.astral.sh/uv/) и его [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/).

Feel free, если захотите улучшить UX/UI или backend. Я открыт к сотрудничеству и предложениям.

## 🚀 Установка и запуск

1. Установите [Docker](https://www.docker.com/get-started)

2. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/nisemenov/yourmirror.git
    cd yourmirror
    ```

3. Запустите проект:

    ```sh
    docker compose up
    ```

После запуска сервис со всеми необходимыми технологиями (postgres, queue, workers, redis) будет доступен в режиме разработчика по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 👨‍💻 Для разработчиков

- Live reload для Django и Tailwind
- Все конфиги в `.env` (используем `django-environ`)
- Celery и Redis подключаются по Docker Compose
- Хранилище медиа — MinIO (`localhost:9000`)

Подробнее см. в [docs/setup.md](docs/setup.md)

## ✅ Тестирование

- Используется `pytest-django`
- `pre-commit` хуки: `ruff`, `codespell`, `mypy`
- CI: GitHub Actions запускает тесты и форматтеры при каждом push'е

    ```sh
    Make test
    ```

## 🚢 Deployment

Никаких k8s и AWS, все через ssh и [docker-compose.prod.yml](docker-compose.production.yml).

Затем [Github Actions](.github/workflows/deploy.yml) должны взять на себя всю грязную работу. Они собирают, тестируют и развертывают изменения в производстве при каждом слиянии с мастером (это могут делать только официальные сопровождающие).

Изучите всю папку [.github](.github) для получения дополнительных сведений.

Мы открыты для предложений о том, как улучшить наши развертывания, не усложняя их современными devops-штуками.

## 🤝 Contributions

Contributions are welcome.

- Форкайте, предлагайте улучшения, создавайте pull requests
- Открывайте Issue, если нашли баг или есть идея
- Предпочтительный язык обсуждений — **русский**, но английский тоже ок

## 🔐 Безопасность

Если вы нашли уязвимость, не стоит тестировать её на проде. Напишите напрямую:

- telegram: [telegram](https://t.me/nikissem)
- email: [gmail](mailto:nasemenov726@gmail.com)

## 📜 Лицензия

[MIT License](LICENSE)

Можно использовать код в любых целях — с сохранением лицензии и упоминанием автора.

🕊️

# Проект: yourmirror

## Описание

Веб-сервис для создания, хранения и просмотра списков желаний. Пользователи могут делиться своими списками с другими и подписываться на чужие.

## Backend

- Python >= 3.13
- PostgreSQL >= 17
- Менеджер пакетов uv >= 0.6.14

#### Django backend

- Django >= 5.2
- django-minio-storage >= 0.5.7 (используется MinIO как S3-совместимое хранилище)
- celery[redis]>=5.5.2

## Frontend

- Django Templates (DTL)
- Tailwind CSS v4 (через django-tailwind >= 4.0.1)
  - Используется директива `@source` в файле `style.css` вместо `content` (нововведение Tailwind v4)

## Хранилище медиа

- Файлы в папке `media/` обслуживаются через MinIO (совместимое с S3)

## Модели

#### User

- Стандартная модель Django
- Используется для регистрации и авторизации

#### ProfileModel

- OneToOne связь с `User`
- Дополнительные поля (например, `telegram_id` — для будущей интеграции с Telegram-ботом)

#### FollowModel

- Подписка на вишлисты других пользователей
- Поля: `follower`, `following` (оба — ForeignKey на `ProfileModel`)

#### WishItemModel

- Элемент списка желаемого
- Поля:
  - `title`, `description`, `link`, `picture`
  - `profile` (FK на `ProfileModel`)
  - `is_private` — bool
  - `reserved` (FK на `ProfileModel`)

#### RegistrationTokenModel

- Промежуточная модель сохранения данных пользователя при регистрации
- Поля:
    - `email`, `first_name`, `password_hash`
    - `token` (UUIDField, для формирования временной ссылки)
    - `expires_at` (DateTimeField, срок действия ссылки)

## Аутентификация

- Регистрация по email, с подтверждением email через отправку временной ссылки (celery, redis)
- При регистрации: `username = email`
- Авторизация по email (email используется как username)

## Доступные страницы

#### Общие

- `register.html`, `login.html`, `logged_out.html`
- `base.html` (с включенными `footer.html`, `header.html`)
- `home.html` — главная страница
- Боковая панель (`side-bar`) содержит вкладку "Контакты" (внизу)

#### Для неавторизованных пользователей

- `/wishlist/{profile_id}/` — просмотр публичного вишлиста другого пользователя и возможность резервации желания

#### Для авторизованных пользователей

- `/wishlist/me/` — собственный вишлист
- `/following/` — подписки на чужие вишлисты
- `/settings/` — настройки профиля
- Боковая панель: вкладки "Вишлист", "Подписки", "Настройки", "Выйти"

### Тестирование и форматирование

- Pre-commit: `pre-commit-hooks`, `ruff`, `codespell`, `mypy`
- Тесты: `pytest-django`, юнит-тесты для логики MVC
- CI: GitHub Actions — пайплайн с форматированием и тестами

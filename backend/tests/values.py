import enum


class VarStr(enum.StrEnum):
    # MODEL FIELDS
    USER_NAME = "test_name"
    USER_EMAIL = "newuser@example.com"
    USER_PASSWORD = "testpass123"

    WISHITEM_TITLE = "test_title"
    WISHITEM_PRIVATE_TITLE = "test_private_title"
    WISHITEM_LINK = "https://example.com"
    WISHITEM_DESCRIPTION = "test_desc"

    REGISTRATION_TOKEN_TOKEN = "2a41af0d-4d14-49a7-963b-9c7ad7b403a8"

    # ERROR MESSAGES
    USER_REG_HAS_USABLE_PASSWORD = "Пользователь с таким email уже зарегистрирован"

    CONFIRM_EMAIL_EXPIRED = "Ссылка истекла."
    CONFIRM_EMAIL_INVALID_TOK = "Недействительная ссылка."

    CONFIRM_FIRST_RESERVATION_RACE_CONDITION = "кто-то уже зарезервировал это желание"

    USER_SETT_DUP_EMAIL = "Пользователь с таким email уже существует"
    USER_SETT_WRNG_CURR_PASS = "Неверный текущий пароль"
    USER_SETT_WRNG_SCND_PASS = "Пароли не совпадают"

    WISHITEM_MY_RESERVE_ERROR = "Вы не можете зарезервировать свое желание"
    WISHITEM_DOUBLE_RESERVE_ERROR = "Это желание уже кто-то зарезервировал"

    # TEMPLATE MESSAGES
    USER_REG_EMAIL_SENT = "Подтверждение регистрации"
    USER_REG_VIEW = "Регистрация"

    WISHITEM_FIRST_RESERVATION_EMAIL = "на вашу почту отправлено письмо"

    WISHILIST_PROFILE_EMPTY = "Этот вишлист пока пуст"
    WISHILIST_MY_EMPTY = "Ваш вишлист пока пуст"

    # BUTTONS
    WISHITEM_RESERVE = "зарезервировать"
    WISHITEM_RESERVED = "зарезервировано"
    WISHITEM_UPDATE = "Редактировать"
    WISHITEM_DELETE = "Удалить"
    WISHITEM_RESERVED_BY_USER = "отменить бронь"

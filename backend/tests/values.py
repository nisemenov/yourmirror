import enum


class VarStr(enum.StrEnum):
    USER_NAME = "test_name"
    USER_EMAIL = "newuser@example.com"
    USER_PASSWORD = "testpass123"

    USER_REG_HAS_USABLE_PASSWORD = "Пользователь с таким email уже зарегистрирован, "

    USER_SETT_DUP_EMAIL = "Пользователь с таким email уже существует"
    USER_SETT_WRNG_CURR_PASS = "Неверный текущий пароль"
    USER_SETT_WRNG_SCND_PASS = "Пароли не совпадают"

    WISHITEM_TITLE = "test_title"
    WISHITEM_PRIVATE_TITLE = "test_private_title"
    WISHITEM_LINK = "https://example.com"
    WISHITEM_DESCRIPTION = "test_desc"
    WISHITEM_RESERVED = "Зарезервировано"
    WISHITEM_UPDATE = "Редактировать"
    WISHITEM_DELETE = "Удалить"

    WISHILIST_PROFILE_EMPTY = "Этот вишлист пока пуст"
    WISHILIST_MY_EMPTY = "Ваш вишлист пока пуст"

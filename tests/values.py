import enum


class VarStr(enum.StrEnum):
    USER_EMAIL = "newuser@example.com"
    USER_PASSWORD1 = "SuperStrong123!"
    USER_PASSWORD2 = "SuperStrong123!"

    WISHITEM_TITLE = "test_title"
    WISHITEM_PRIVATE_TITLE = "test_private_title"
    WISHITEM_LINK = "https://example.com"
    WISHITEM_DESCRIPTION = "test_desc"

    WISHILIST_EMPTY = "Этот вишлист пока пуст."

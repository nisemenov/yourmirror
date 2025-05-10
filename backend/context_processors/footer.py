import datetime as dt

from django.http import HttpRequest


def year(request: HttpRequest) -> dict[str, int]:
    return {"year": dt.datetime.now().year}

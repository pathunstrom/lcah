from flask.json import http_date as _http_date

from lcah import app


@app.template_filter('http_date')
def http_date(datetime):
    return _http_date(datetime)

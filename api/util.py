import validators


def validate_url(url):
    if not validators.url(url):
        return False
    return True

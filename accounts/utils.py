import random
import string
from django.conf import settings


SHORTCODE_MIN = getattr(settings, 'SHORTCODE_MIN', 50)


def code_generator(size=SHORTCODE_MIN):
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(size)])

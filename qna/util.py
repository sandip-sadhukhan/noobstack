import string
from django.utils.text import slugify
import random

EXISTS_URLS = ['', 'new', 'about', 'register'] # put all your exists url here so that no urls clashes with each other

def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists or (slug in EXISTS_URLS):
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr = random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

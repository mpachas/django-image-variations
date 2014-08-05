=======================
django-image-variations
=======================

The image_variations Django application allows you to create different
variations of uploaded images that can be used as thumbnails or for any
another purposes.

Installation
============

You can install image_variations using pip::

    pip install django-image-variations

Alternatively, you can install it from source::

    git clone https://github.com/pisemsky/django-image-variations.git
    cd django-image-variations
    python setup.py install

After installing append ``image_variations`` to ``INSTALLED_APPS`` in
your project settings file.

Configuration
=============

Variations defined by setting up variable ``IMAGE_VARIATIONS`` in Django
project settings file. This is a dict where key is variation name and
value is a tuple of 2-tuples. Each of that 2-tuples describes one of
transforms that consequentially applied to the original image. The first
element of each 2-tuple is a transform name that is method in
``transforms.py`` file and second element is a dict with keyword
arguments to that method. Example configuration::

    IMAGE_VARIATIONS = {
        'small': (
            ('crop', {'width': 120, 'height': 90}),
            ('save', {'quality': 90}),
        ),
        'large': (
            ('resize', {'width': 640}),
            ('save', {'quality': 90, 'progressive': True}),
        ),
    }

Currently there are only two transforms implemented - ``resize`` and
``crop``. There is also a special transform called ``save`` that allows
you to specify image quality and another options suitable for PIL's
``Image.save`` method. This transfrom is not required, but if used, it
must be last in tuple.

Usage
=====

Application provides a field called ``ImageVariationsField`` that based
on standard Django ``ImageField`` and performs all magic. Use this field
in your models::

    from image_variations.fields import ImageVariationsField

    class Image(models.Model):
        image = ImageVariationsField(upload_to='images')

After that variations can be accessed as attributes of the image field
like so::

    object.image.small
    object.image.small.name
    object.image.small.width
    object.image.small.height
    object.image.small.path
    object.image.small.url

Each variation represented by ``ImageFile`` instance with two additional
attributes - ``path`` and ``url``.

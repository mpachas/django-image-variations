from distutils.core import setup

setup(
    name='django-image-variations',
    version='0.2.1',
    author='Evgeny Pisemsky',
    author_email='evgeny@pisemsky.com',
    url='https://github.com/pisemsky/django-image-variations',
    description='Django application for creating thumbnails and another variations of uploaded images.',
    long_description=open('README.rst').read(),
    platforms=['OS Independent'],
    license='LICENSE.txt',
    packages=['image_variations'],
)

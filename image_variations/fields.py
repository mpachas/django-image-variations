import os.path
import cStringIO
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from image_variations.transforms import Transforms
from image_variations.settings import IMAGE_VARIATIONS

class ImageVariationsFieldFile(ImageFieldFile):

    def save(self, name, content, save=True):
        super(ImageFieldFile, self).save(name, content, save)
        self._create_variations(content)

    def delete(self, save=True):
        for variation in IMAGE_VARIATIONS.iterkeys():
            try:
                self.storage.delete(self._variation_name(variation))
            except NotImplementedError:
                pass
        super(ImageFieldFile, self).delete(save)

    def __getattr__(self, variation):
        if variation in IMAGE_VARIATIONS:
            name = self._variation_name(variation)
            try:
                image = ImageFile(self.storage.open(name), name)
                try:
                    image.path = self.storage.path(image.name)
                except NotImplementedError:
                    image.path = None
                try:
                    image.url = self.storage.url(image.name)
                except NotImplementedError:
                    image.url = None
                return image
            except IOError:
                pass
        raise AttributeError

    def _variation_name(self, variation):
        root, ext = os.path.splitext(self.name)
        return root + '_' + variation + ext

    def _create_variations(self, content):
        for variation, transforms in IMAGE_VARIATIONS.iteritems():
            content.seek(0)
            io = cStringIO.StringIO()
            image = Transforms()
            image.open(content)
            for transform in transforms:
                method_name, kwargs = transform
                if method_name == 'save':
                    kwargs['path'] = io
                method = getattr(image, method_name)
                method(**kwargs)
            if not 'save' in transforms:
                image.save(io)
            image_file = ContentFile(io.getvalue())
            self.storage.save(self._variation_name(variation), image_file)

class ImageVariationsField(ImageField):
    attr_class = ImageVariationsFieldFile

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^image_variations\.fields\.ImageVariationsField"])

from PIL import Image, ImageOps

class Transforms:

    def open(self, path):
        self.img = Image.open(path)
        self.format = self.img.format
        if self.img.mode not in ('L', 'RGB', 'RGBA'):
            self.img = self.img.convert('RGB')

    def save(self, path):
        self.img.save(path, self.format, quality=90)

    def resize(self, width=False, height=False):
        size = False
        if width and height:
            size = (width, height)
        elif width or height:
            w, h = self.img.size
            ratio = float(w) / float(h)
            if width:
                size = (width, int(width/ratio))
            else:
                size = (int(height*ratio), height)
        if size:
            self.img = self.img.resize(size, Image.ANTIALIAS)

    def crop(self, width=False, height=False):
        if width and height:
            self.img = ImageOps.fit(self.img, (width, height), Image.ANTIALIAS)

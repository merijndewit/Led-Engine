import os
import urllib.request
import time
from PIL import Image

from LedPanel import LedPanel

class DisplayGif(LedPanel):
    
    def __init__(self):
        super().__init__()
        self.gifUrl = ""

    def UpdategifUrl(self, value):
        self.gifUrl = str(value)
        print("gif set to:", value)

    def ConvertGif(self):
        if self.gifUrl != "":
            imageName = "tmp.gif"
            path = os.path.dirname(os.path.realpath(__file__)) + "/../tmpImages/" + imageName
            try:
                urllib.request.urlretrieve(self.gifUrl, path)
            except:
                print("coudn't download gif")
                return
            self.resize_gif(path, None, (self.ledPanelsPixelWidth, self.ledPanelsPixelHeight))
            return path

    def PlayGif(self):
        self.ledPanelsPixelWidth
        self.ledPanelsPixelHeight
        print(self.ledPanelsPixelWidth)
        self.ConvertGif()
        gif = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../tmpImages/tmp.gif")
        
        while True:
            for i in range(gif.n_frames):
                gif.seek(i)
                rgb_im = gif.convert('RGB')
                for y in range(self.ledPanelsPixelHeight):
                    for x in range(self.ledPanelsPixelWidth):
                        pixel = int(self.getPixelNumber(x, y))
                        r, g, b = rgb_im.getpixel((x, y))  
                        self.pixels[pixel] = (r * ((self.Rpercentage / 100)*(self.ledBrightness / 100)), g * (self.Gpercentage / 100)*(self.ledBrightness / 100), b * (self.Bpercentage / 100)*(self.ledBrightness / 100))
                self.pixels.show()
                time.sleep(0.2)

    def resize_gif(self, path, save_as=None, resize_to=None):
        all_frames = self.extract_and_resize_frames(path, resize_to)

        if not save_as:
            save_as = path

        if len(all_frames) == 1:
            all_frames[0].save(save_as, optimize=True)
        else:
            all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)

    def extract_and_resize_frames(self, path, resize_to=None):
        im = Image.open(path)
        all_frames = []
        try:
            while True:
                im.convert('RGB')
                new_frame = im.resize((self.ledPanelsPixelWidth, self.ledPanelsPixelHeight))
                all_frames.append(new_frame)
                im.seek(im.tell() + 1)
        except EOFError:
            pass

        return all_frames

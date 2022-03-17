import os
import urllib
import time
from PIL import Image

from LedPanel import LedPanel

class DisplayGif(LedPanel):
    
    gifUrl = ""
    ledPanelsPixelWidth = 0
    ledPanelsPixelHeight = 0

    def UpdategifUrl(value):
        DisplayGif.gifUrl = str(value)

    def ConvertGif():
        if DisplayGif.gifUrl != "":
            imageName = "tmp.gif"
            path = os.path.dirname(os.path.realpath(__file__))+"/tmpImages/" + imageName
            try:
                urllib.request.urlretrieve(DisplayGif.gifUrl, path)
            except:
                return ""
            DisplayGif.resize_gif(path, None, (DisplayGif.ledPanelsPixelWidth, DisplayGif.ledPanelsPixelHeight))
            return path

    @classmethod
    def PlayGif(cls):
        DisplayGif.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        DisplayGif.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight
        print(DisplayGif.ledPanelsPixelWidth)
        DisplayGif.ConvertGif()
        gif = Image.open(os.path.dirname(os.path.realpath(__file__))+"/tmpImages/tmp.gif")
        
        while True:
            for i in range(gif.n_frames):
                gif.seek(i)
                rgb_im = gif.convert('RGB')
                for y in range(DisplayGif.ledPanelsPixelHeight):
                    for x in range(DisplayGif.ledPanelsPixelWidth):
                        pixel = int(LedPanel.getPixelNumber(x, y))
                        r, g, b = rgb_im.getpixel((x, y))  
                        LedPanel.pixels[pixel] = (r * ((cls.Rpercentage / 100)*(cls.ledBrightness / 100)), g * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), b * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
                LedPanel.pixels.show()
                time.sleep(0.2)

    def resize_gif(path, save_as=None, resize_to=None):
        all_frames = DisplayGif.extract_and_resize_frames(path, resize_to)

        if not save_as:
            save_as = path

        if len(all_frames) == 1:
            all_frames[0].save(save_as, optimize=True)
        else:
            all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)

    def extract_and_resize_frames(path, resize_to=None):
        print(DisplayGif.ledPanelsPixelWidth)
        im = Image.open(path)
        all_frames = []
        try:
            while True:
                im.convert('RGB')
                new_frame = im.resize((DisplayGif.ledPanelsPixelWidth, DisplayGif.ledPanelsPixelHeight))
                all_frames.append(new_frame)
                im.seek(im.tell() + 1)
        except EOFError:
            pass

        return all_frames

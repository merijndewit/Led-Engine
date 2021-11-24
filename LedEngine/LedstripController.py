from rpi_ws281x import Adafruit_NeoPixel, Color

# LED strip configuration:
LED_COUNT = 13       # Number of LED pixels.
LED_PIN = 12        # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

ledStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
ledStrip.begin()
for i in range(0, ledStrip.numPixels(), 1): #resets led's
    ledStrip.setPixelColor(i, Color(0, 0, 0))


def setColor(rgbColor):
    for i in range(0, ledStrip.numPixels(), 1): #resets led's
        ledStrip.setPixelColor(i, rgbColor)
    ledStrip.show()

import json
import os

import LedPanel as LedPanel
import LedStrip as LedStrip


class JsonHelper:
    jsonFile = os.path.dirname(os.path.realpath(__file__))+'/config.json'

    def WriteToJsonFile(key, value):
        if (os.path.exists(JsonHelper.jsonFile) != 1):
            data = {key:value}
            with open(JsonHelper.jsonFile, 'w') as json_file:
                json.dump(data, json_file)
            return

        with open(JsonHelper.jsonFile) as json_file:
            json_decoded = json.load(json_file)

        json_decoded[key] = value

        with open(JsonHelper.jsonFile, 'w') as json_file:
            json.dump(json_decoded, json_file)

    def GetDecodedJSON():
        with open(JsonHelper.jsonFile) as json_file:
            return json.load(json_file)

    def LoadJsonValues():
        import LedController as LedController

        with open(JsonHelper.jsonFile) as json_file:
            json_decoded = json.load(json_file)

        if not (json_decoded.get('redCalibration') is None):
            LedController.LedController.Rpercentage = int(json_decoded["redCalibration"])
        if not (json_decoded.get('greenCalibration') is None):
            LedController.LedController.Gpercentage = int(json_decoded["greenCalibration"])
        if not (json_decoded.get('blueCalibration') is None):
            LedController.LedController.Bpercentage = int(json_decoded["blueCalibration"])
        if not (json_decoded.get('LedCount') is None):
            LedStrip.LedStrip.pixelCount = int(json_decoded.get('LedCount'))
        if not (json_decoded.get('brightnessValue') is None):
            LedController.LedController.SetBrightness(int(json_decoded["brightnessValue"]))
        if not (json_decoded.get('amountOfPanelsInWidth') is None):
            LedPanel.LedPanel.amountOfPanelsInWidth = int(json_decoded["amountOfPanelsInWidth"])
        if not (json_decoded.get('amountOfPanelsInHeight') is None):
            LedPanel.LedPanel.amountOfPanelsInHeight = int(json_decoded["amountOfPanelsInHeight"])
        if not (json_decoded.get('LEDPanelWidth') is None):
            LedPanel.LedPanel.ledPanelWidth = int(json_decoded["LEDPanelWidth"])
        if not (json_decoded.get('LEDPanelHeight') is None):
            LedPanel.LedPanel.ledPanelHeight = int(json_decoded["LEDPanelHeight"])
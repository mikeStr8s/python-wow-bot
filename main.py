import numpy as np
import cv2
import imutils
import pyautogui
import pytesseract
from PIL import Image


def main():
    # Get the players name, current health, and current resource value
    while True:
        health, resource = get_bar_values()
        print(health, resource)


def get_bar_values():
    """
    This returns the values inside the player health and resource UI.
    It requires a 1080p screenshot of the monitor and default UI.
    Then strips the values using tesseract's OCR on a processed image.
    :return: health and resource list values
    """
    # Grab the screenshot
    pre_image = cv2.imread('wow_screenshot.jpg', 0)
    # Extract the entire character bar
    character_bar = pre_image[20:125, 25:300]
    coords = [character_bar[44:59, 100:266], character_bar[59:75, 100:266]]

    def get_value(ui):
        """
        This internal function is for getting bar values from screen coordinates
        :param ui: screenshot coordinates
        :return: string value found in the screenshot region
        """
        # Double the size of the image
        ui = cv2.resize(ui, (0, 0), fx=2, fy=2)
        # Create threshold of grayscale image. Anything from value 0-130 is white, > 130 is black
        ui = cv2.inRange(ui, 0, 130)
        # OCR on the threshold image
        return pytesseract.image_to_string(Image.fromarray(ui))

    # Return lists of parsed health and resource values
    return [int(x) for x in get_value(coords[0]).split('/ ')], [int(x) for x in get_value(coords[1]).split('/ ')]


def take_screenshot():
    """
    This function takes a screenshot of the main monitor
    """
    pyautogui.screenshot('wow_bot_screengrab.png')


if __name__ == "__main__":
    main()

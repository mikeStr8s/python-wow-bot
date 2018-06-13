import numpy as np
import cv2
import imutils
import pytesseract
from PIL import Image, ImageGrab


def main():
    get_bar_values()
    # # Get the players name, current health, and current resource value
    # while True:
    #     health, resource = get_bar_values()
    #     print(health, resource)


def get_bar_values():
    """
    This returns the values inside the player health and resource UI.
    It requires a 1080p screenshot of the monitor and default UI.
    Then strips the values using tesseract's OCR on a processed image.
    :return: health and resource list values
    """
    # Grab the screenshot
    game_window = np.array(ImageGrab.grab(bbox=(0, 100, 1600, 1280)))
    game_window = cv2.cvtColor(game_window, cv2.COLOR_BGR2GRAY)
    character_bar = game_window[25:130, 35:315]
    coords = [character_bar[32:50, 120:256], character_bar[50:68, 120:256]]

    # Extract the entire character bar
    def get_value(ui):
        """
        This internal function is for getting bar values from screen coordinates
        :param ui: screenshot coordinates
        :return: string value found in the screenshot region
        """
        # Double the size of the image
        ui = cv2.resize(ui, (0, 0), fx=3, fy=3)
        # Create threshold of grayscale image. Anything from value 0-130 is white, > 130 is black
        ui = cv2.inRange(ui, 0, 145)
        ui = cv2.medianBlur(ui, 3)
        cv2.imshow('win', ui)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # OCR on the threshold image
        return pytesseract.image_to_string(Image.fromarray(ui))

    # Return lists of parsed health and resource values
    return [int(x) for x in get_value(coords[0]).split('/ ')], [int(x) for x in get_value(coords[1]).split('/ ')]


if __name__ == "__main__":
    main()

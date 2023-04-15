import os

from PIL import Image


class AssetHelper:
    @staticmethod
    def get_image_poker_table() -> Image:
        root_path = os.path.abspath(os.path.dirname(__file__))
        try:
            return Image.open(root_path + '/../../assets/poker_table.jpeg')
        except FileNotFoundError:
            raise FileNotFoundError('Poker table image not found')

    @staticmethod
    def get_image_avatar_anonymous() -> Image:
        root_path = os.path.abspath(os.path.dirname(__file__))
        try:
            return Image.open(root_path + '/../../assets/anonymous.png')
        except FileNotFoundError:
            raise FileNotFoundError('Anonymous avatar image not found')


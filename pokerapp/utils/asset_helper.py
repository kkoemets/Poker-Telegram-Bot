import os

from PIL import Image, ImageFont

from pokerapp.constants import IMAGE_SMALL, FONT_SIZE_MEDIUM


class AssetHelper:
    @staticmethod
    def get_image_poker_table() -> Image:
        return AssetHelper.__get_image_from_asset_collection('poker_table.jpeg')

    @staticmethod
    def get_image_avatar_anonymous() -> Image:
        return AssetHelper.__get_image_from_asset_collection('anonymous.png')

    @staticmethod
    def get_font_free_mono(size=FONT_SIZE_MEDIUM) -> ImageFont:
        return AssetHelper.__get_font_from_asset_collection('FreeMono.ttf', size)

    @staticmethod
    def resize_square(image, new_size=IMAGE_SMALL) -> Image:
        return image.resize((new_size, new_size))

    @staticmethod
    def __get_image_from_asset_collection(name: str) -> Image:
        root_path = os.path.abspath(os.path.dirname(__file__))
        try:
            return Image.open(f'{root_path}/../../assets/{name}')
        except FileNotFoundError:
            raise FileNotFoundError('Image asset not found')

    @staticmethod
    def __get_font_from_asset_collection(name: str, size: int) -> ImageFont:
        root_path = os.path.abspath(os.path.dirname(__file__))
        try:
            return ImageFont.truetype(f'{root_path}/../../assets/{name}', size)
        except FileNotFoundError:
            raise FileNotFoundError('Font asset not found')

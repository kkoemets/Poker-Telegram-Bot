#!/usr/bin/env python3
from io import BytesIO
from typing import Union
from PIL import Image, ImageDraw
from telegram import (
    Message,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Bot,
    InputMediaPhoto,
)
from telegram.utils.types import FileInput

from pokerapp.constants import COLOR_WHITE, COLOR_BLACK, FONT_SIZE_MEDIUM, FRAME_STROKE
from pokerapp.entity.cards import Cards
from pokerapp.entity.entities import (
    MessageId,
    ChatId,
    Mention,
    Money,
)
from pokerapp.entity.game import Game
from pokerapp.entity.player import Player
from pokerapp.entity.playeraction import PlayerAction
from pokerapp.entity.poker_table_info import PokerTableInfo, COMMON_CARD_WIDTH, COMMON_CARD_HEIGHT, \
    COMMON_CARD_WIDTH_SMALL, COMMON_CARD_HEIGHT_SMALL
from pokerapp.utils.asset_helper import AssetHelper
from pokerapp.view.deskimagegenerator import DeskImageGenerator


class PokerBotViewer:
    def __init__(self, bot: Bot):
        self._bot = bot
        self._desk_generator = DeskImageGenerator()

    def send_message(
            self,
            chat_id: ChatId,
            text: str,
            reply_markup: ReplyKeyboardMarkup = None,
    ) -> None:
        self._bot.send_message(
            chat_id=chat_id,
            parse_mode=ParseMode.MARKDOWN,
            text=text,
            reply_markup=reply_markup,
            disable_notification=True,
            disable_web_page_preview=True,
        )

    def send_photo(self, chat_id: ChatId, photo: Union[FileInput]) -> None:
        self._bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
        )

    def send_dice_reply(
        self,
        chat_id: ChatId,
        message_id: MessageId,
        emoji='🎲',
    ) -> Message:
        return self._bot.send_dice(
            reply_to_message_id=message_id,
            chat_id=chat_id,
            disable_notification=True,
            emoji=emoji,
        )

    def send_message_reply(
        self,
        chat_id: ChatId,
        message_id: MessageId,
        text: str,
    ) -> None:
        self._bot.send_message(
            reply_to_message_id=message_id,
            chat_id=chat_id,
            parse_mode=ParseMode.MARKDOWN,
            text=text,
            disable_notification=True,
        )

    def send_desk_cards_img(
        self,
        chat_id: ChatId,
        cards: Cards,
        caption: str = "",
        disable_notification: bool = True,
    ) -> MessageId:
        im_cards = self._desk_generator.generate_desk(cards)
        bio = BytesIO()
        bio.name = 'desk.png'
        im_cards.save(bio, 'PNG')
        bio.seek(0)
        return self._bot.send_media_group(
            chat_id=chat_id,
            media=[
                InputMediaPhoto(
                    media=bio,
                    caption=caption,
                ),
            ],
            disable_notification=disable_notification,
        )[0]

    @ staticmethod
    def _get_cards_markup(cards: Cards) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[cards],
            selective=True,
            resize_keyboard=True,
        )

    @staticmethod
    def _get_turns_markup(
            check_call_action: PlayerAction
    ) -> InlineKeyboardMarkup:

        def create_inline_kb_btn_text(action: PlayerAction) -> str:
            return f"{action.value}$ " \
                   f"({'{:.1f}'.format(action.value / PlayerAction.BIG_BLIND.value).rstrip('0').rstrip('.')} BB)"

        def create_inline_keyboard_buttons(actions):
            return [
                InlineKeyboardButton(text=create_inline_kb_btn_text(action), callback_data=str(action.value))
                for action in actions
            ]

        keyboard = [
            [
                InlineKeyboardButton(text=PlayerAction.FOLD.value, callback_data=PlayerAction.FOLD.value),
                InlineKeyboardButton(text=PlayerAction.ALL_IN.value, callback_data=PlayerAction.ALL_IN.value),
                InlineKeyboardButton(text=check_call_action.value, callback_data=check_call_action.value),
            ],
            create_inline_keyboard_buttons([
                PlayerAction.BIG_BLIND,
                PlayerAction.BET_TWENTY_FIVE,
            ]),
            create_inline_keyboard_buttons([
                PlayerAction.BET_FIFTY,
                PlayerAction.BET_ONE_HUNDRED,
            ]),
            create_inline_keyboard_buttons([
                PlayerAction.BET_TWO_HUNDRED_FIFTY,
                PlayerAction.BET_FIVE_HUNDRED,
            ]),
        ]

        return InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )

    def send_cards(
            self,
            chat_id: ChatId,
            cards: Cards,
            mention_markdown: Mention,
            ready_message_id: str,
    ) -> None:
        markup = PokerBotViewer._get_cards_markup(cards)
        self._bot.send_message(
            chat_id=chat_id,
            text="Showing cards to " + mention_markdown,
            reply_markup=markup,
            reply_to_message_id=ready_message_id,
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
        )

    @ staticmethod
    def define_check_call_action(
        game: Game,
        player: Player,
    ) -> PlayerAction:
        if player.round_rate == game.max_round_rate:
            return PlayerAction.CHECK
        return PlayerAction.CALL

    def send_turn_actions(
            self,
            chat_id: ChatId,
            game: Game,
            player: Player,
            money: Money,
    ) -> None:
        if len(game.cards_table) == 0:
            cards_table = "no cards"
        else:
            cards_table = " ".join(game.cards_table)
        text = (
            f"Turn of {player.mention_markdown}\n"
            f"{cards_table}\n"
            f"Money: *{money}$* "
            f"({'{:.1f}'.format(money / PlayerAction.BIG_BLIND.value).rstrip('0').rstrip('.')} BB)\n"
            f"Pot size: *{sum(bet.amount for bet in game.players_bets)}$*\n"
            f"Your $ in pot: "
            f"*{sum(bet.amount for bet in game.players_bets if bet.user_id == player.user_id)}$*\n"
            f"Tap /cards to show cards"
        )

        check_call_action = PokerBotViewer.define_check_call_action(
            game, player
        )
        markup = PokerBotViewer._get_turns_markup(check_call_action)
        self._bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
        )

    def remove_markup(
        self,
        chat_id: ChatId,
        message_id: MessageId,
    ) -> None:
        self._bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
        )

    def remove_message(
        self,
        chat_id: ChatId,
        message_id: MessageId,
    ) -> None:
        self._bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )

    def show_poker_table_with_players(self, chat_id: ChatId, poker_table_info: PokerTableInfo) -> Image:
        image_poker_table = AssetHelper.get_image_poker_table()
        table_width, table_height = image_poker_table.size
        avatar_width, avatar_height = poker_table_info.avatar_max_size

        # Create new image with the size of the table, make some extra room for avatars
        new_image_width, new_image_height = table_width, table_height + avatar_height * 2
        new_image = Image.new('RGB', (new_image_width, new_image_height), COLOR_WHITE)
        new_image.paste(image_poker_table, (0, avatar_height))

        # Get draw mode. It enables adding text as well as drawing shapes.
        draw = ImageDraw.Draw(new_image)

        # Draw 5 cards in the center of the table
        unknown_card = AssetHelper.get_unknown_card()
        unknown_card = AssetHelper.resize(unknown_card, COMMON_CARD_WIDTH, COMMON_CARD_HEIGHT)
        for location in poker_table_info.common_card_locations:
            new_image.paste(unknown_card, location)

        # Draw all players
        player_name_font = AssetHelper.get_font_free_mono(FONT_SIZE_MEDIUM)
        player_unknown_card = AssetHelper.get_unknown_card()
        player_unknown_card = AssetHelper.resize(player_unknown_card, COMMON_CARD_WIDTH_SMALL, COMMON_CARD_HEIGHT_SMALL)
        for player in poker_table_info.players:
            x, y = player.image_position_for_player
            width_offset, height_offset = 80, 10  # used for measuring  relative distance between avatar, name & money

            # Draw avatars
            new_image.paste(player.avatar, (x, y))

            # Draw player's name
            draw.text((x - width_offset, y + avatar_height + height_offset), player.name, font=player_name_font, fill=COLOR_BLACK)

            # Draw player's money
            draw.text((x + 10, y + avatar_height + height_offset * 4), f'{player.money} $', font=player_name_font, fill=COLOR_BLACK, stroke_width=1)

            # Draw a red frame around active player
            if player.is_current_turn:
                frame_x0 = x - FRAME_STROKE
                frame_y0 = y - FRAME_STROKE
                frame_x1 = frame_x0 + avatar_width + FRAME_STROKE * 2
                frame_y1 = frame_y0 + avatar_height + FRAME_STROKE * 2
                draw.rectangle((frame_x0, frame_y0, frame_x1, frame_y1), outline="red", width=5)

            # draw player's cards
            player_card_1_pos, player_card_2_pos = player.card_positions_for_player
            new_image.paste(player_unknown_card, player_card_1_pos)
            new_image.paste(player_unknown_card, player_card_2_pos)

        # Finalize combined image. Convert the image into bytearray to keep it in memory and avoiding saving it to disk
        with BytesIO() as output:
            new_image.save(output, format='JPEG')
            image_poker_table_with_players = output.getvalue()

        self._bot.send_photo(
            chat_id=chat_id,
            photo=image_poker_table_with_players,
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
        )

from dataclasses import dataclass, field
from typing import List, Tuple

from PIL import Image

from pokerapp.constants import MAX_PLAYERS

"""
Coordinates of the players.

        P1              P2              P3               P4
===================================================================
|                                                                 |
|                                                                 |
|                                                                 |
|                                                                 |
|                                                                 |
===================================================================
        P5              P6              P7               P8
"""
CHAIR_POSITIONS = {
    0: (500, 100),
    1: (800, 100),
    2: (1100, 100),
    3: (1400, 100),
    4: (500, 1150),
    5: (800, 1150),
    6: (1100, 1150),
    7: (1400, 1150),
}

"""
Coordinates of the cards of the players. There are 2 cards at every coordinate with SPACING between them.

===================================================================
|                                                                 |
|                         COMMON CARDS:                           |
|                       [0] [1] [2] [3] [4]                       |
|                                                                 |
|                                                                 |
===================================================================
"""
COMMON_CARD_WIDTH = 100
COMMON_CARD_WIDTH_SMALL = 50
COMMON_CARD_HEIGHT = 130
COMMON_CARD_HEIGHT_SMALL = 65
COMMON_CARD_LOCATION = {
    0: (770, 620),
    1: (880, 620),
    2: (990, 620),
    3: (1100, 620),
    4: (1210, 620),
}

"""
Coordinates of the cards of the players. There are 2 cards at every coordinate with SPACING between them.

===================================================================
|  (row1, col1)    (row1, col2)    (row1, col3)     (row1, col4)  |
|                                                                 |
|                                                                 |
|                                                                 |
|  (row1, col1)    (row1, col2)    (row1, col3)     (row1, col4)  |
===================================================================
"""
ROW1 = 350
ROW2 = 950
COL1, COL2, COL3, COL4 = 500, 800, 1100, 1400
SPACING = 68

PLAYER_CARD_LOCATIONS = {
    0: ((COL1, ROW1), (COL1 + SPACING, ROW1)),
    1: ((COL2, ROW1), (COL2 + SPACING, ROW1)),
    2: ((COL3, ROW1), (COL3 + SPACING, ROW1)),
    3: ((COL4, ROW1), (COL4 + SPACING, ROW1)),
    4: ((COL1, ROW2), (COL1 + SPACING, ROW2)),
    5: ((COL2, ROW2), (COL2 + SPACING, ROW2)),
    6: ((COL3, ROW2), (COL3 + SPACING, ROW2)),
    7: ((COL4, ROW2), (COL4 + SPACING, ROW2)),
}


@dataclass(frozen=True)
class PokerTablePlayerInfo:
    """
    Responsible for keeping coordinate info of individual player of the table. Use only with PokerTableInfo class.
    """

    avatar: Image
    name: str
    money: int
    chair_id: int  # on which chair is the player sitting
    is_current_turn: bool = False  # is it the player's turn

    @property
    def image_position_for_player(self) -> Tuple[int, int]:
        assert 0 <= self.chair_id < MAX_PLAYERS

        return CHAIR_POSITIONS[self.chair_id]

    @property
    def card_positions_for_player(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        assert 0 <= self.chair_id < MAX_PLAYERS

        return PLAYER_CARD_LOCATIONS[self.chair_id]


@dataclass(frozen=True)
class PokerTableInfo:
    """
    Responsible for keeping coordinate info of where players & cards are located.
    """

    players: List[PokerTablePlayerInfo] = field(default_factory=list)

    @property
    def avatar_max_size(self) -> Tuple[int, int]:
        assert len(self.players) > 0

        return max(player.avatar.size for player in self.players)

    @property
    def common_card_locations(self) -> List[Tuple[int, int]]:
        return list(COMMON_CARD_LOCATION.values())

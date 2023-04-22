from dataclasses import dataclass, field
from typing import List, Tuple

from PIL import Image

from pokerapp.constants import MAX_PLAYERS

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

COMMON_CARD_LOCATION = {
    0: (500, 500),
    1: (600, 500),
    2: (700, 500),
    3: (800, 500),
    4: (900, 500),
}

ROW_UP = 200
ROW_DOWN = 1100
COL1, COL2, COL3, COL4 = 500, 800, 1100, 1400
DIFF = 50

PLAYER_CARD_LOCATIONS = {
    0: ((COL1, ROW_UP), (COL1 + DIFF, ROW_UP)),
    1: ((COL2, ROW_UP), (COL2 + DIFF, ROW_UP)),
    2: ((COL3, ROW_UP), (COL3 + DIFF, ROW_UP)),
    3: ((COL4, ROW_UP), (COL4 + DIFF, ROW_UP)),
    4: ((COL1, ROW_DOWN), (COL1 + DIFF, ROW_DOWN)),
    5: ((COL2, ROW_DOWN), (COL2 + DIFF, ROW_DOWN)),
    6: ((COL3, ROW_DOWN), (COL3 + DIFF, ROW_DOWN)),
    7: ((COL4, ROW_DOWN), (COL4 + DIFF, ROW_DOWN)),
}


@dataclass(frozen=True)
class PokerTablePlayerInfo:
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
    players: List[PokerTablePlayerInfo] = field(default_factory=list)

    @property
    def avatar_max_size(self) -> Tuple[int, int]:
        assert len(self.players) > 0

        return max(player.avatar.size for player in self.players)

    @property
    def common_card_locations(self) -> List[Tuple[int, int]]:
        return list(COMMON_CARD_LOCATION.values())


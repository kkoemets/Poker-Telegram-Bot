import os
from dataclasses import dataclass, field
from typing import List, Tuple

from PIL import Image


CHAIR_POSITIONS = {
    0: (500, 100),
    1: (900, 100),
    2: (1300, 100),
    3: (500, 1200),
    4: (900, 1200),
    5: (1300, 1200),
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
        return CHAIR_POSITIONS[self.chair_id]


@dataclass(frozen=True)
class PokerTableInfo:
    players: List[PokerTablePlayerInfo] = field(default_factory=list)

    @property
    def avatar_max_size(self) -> Tuple[int, int]:
        return max(player.avatar.size for player in self.players)



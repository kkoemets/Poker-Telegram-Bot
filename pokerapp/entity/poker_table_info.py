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


@dataclass(frozen=True)
class PokerTableInfo:
    players: List[PokerTablePlayerInfo] = field(default_factory=list)

    @property
    def avatar_max_size(self) -> Tuple[int, int]:
        assert len(self.players) > 0

        return max(player.avatar.size for player in self.players)



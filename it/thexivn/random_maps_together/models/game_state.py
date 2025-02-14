from dataclasses import dataclass
import time as py_time
from .enums.game_stage import GameStage


@dataclass
class GameState:
    start_time = None
    map_start_time = None
    total_time_gained = None
    stage: GameStage = GameStage.HUB
    current_map_completed: bool = False
    map_is_loading: bool = False
    free_skip_available: bool = False
    game_is_in_progress: bool = False
    skip_medal_player = None
    skip_medal = None
    is_paused = False

    def is_hub_stage(self) -> bool:
        return GameStage.HUB == self.stage

    def is_game_stage(self) -> bool:
        return GameStage.RMT == self.stage

    def skip_command_allowed(self):
        return self.is_game_stage() and not self.current_map_completed

    def set_start_new_state(self):
        self.current_map_completed = True
        self.stage = GameStage.RMT
        self.free_skip_available = True
        self.skip_medal = None
        self.map_is_loading = False
        self.game_is_in_progress = True
        self.is_paused = False
        self.start_time = None
        self.map_start_time = None
        self.total_time_gained = 0

    def set_new_map_in_game_state(self):
        self.current_map_completed = False
        self.game_is_in_progress = True
        self.map_is_loading = False

    def set_map_completed_state(self):
        self.current_map_completed = True

    def set_hub_state(self):
        self.stage = GameStage.HUB
        self.game_is_in_progress = False
        self.free_skip_available = False
        self.skip_medal = False
        self.is_paused = False

    def map_played_time(self):
        if not self.game_is_in_progress or self.map_is_loading or self.current_map_completed:
            return 0
        return int(py_time.time() - self.map_start_time - 1)

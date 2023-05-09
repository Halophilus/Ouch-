import enum

class PollResult(enum.Enum):
    SHOULD_RESTART = enum.auto()
    CONTINUE = enum.auto()
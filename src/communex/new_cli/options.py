from typing import Any, Optional

class Options:
    pass

class CLIOptions(Options):
    use_json: bool = False
    use_colors: bool = True
    use_testnet: bool = False
    use_yes_to_all: bool = False

class Option:
    short_name: str
    long_name: str
    default: Optional[Any]
    require_argument: bool

    def __init__(
        self,
        short_name: str,
        long_name: str,
        default: Optional[Any],
        require_value: bool,
    ): pass

    def execute(
        self,
        value: Optional[Any],
        options: Options
    ): pass

    def help(self): pass

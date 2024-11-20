from typing import Any, Optional

class Options:
    pass

class Option:
    short_name: str
    long_name: str
    default: Optional[Any]
    require_value: bool

    def __init__(
        self,
        short_name: str,
        long_name: str,
        default: Optional[Any],
        require_value: bool,
    ):
        self.short_name = short_name
        self.long_name = long_name
        self.default = default
        self.require_value = require_value

    def execute(
        self,
        value: Optional[Any],
        options: Options
    ) -> Any: pass

    def help(self) -> Any: pass

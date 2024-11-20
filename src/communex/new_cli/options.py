from typing import Any, Optional, cast

class Options:
    pass

class OptionsWithHelp:
    show_help: bool = False

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

class ShowHelpOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'h',
            long_name = 'help',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        options_with_help = cast(OptionsWithHelp, options)
        options_with_help.show_help = True
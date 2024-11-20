from typing import Any, Optional, cast

from communex.new_cli.options import Options
from ..arguments import Option

DEFAULT_TESTNET_URL = "wss://testnet.api.communeai.net"

class AppOptions(Options):
    json: bool = False
    testnet: bool = False
    yes_to_all: bool = False

    interactive: bool = True
    no_color: Optional[bool] = None

    testnet_url: str = DEFAULT_TESTNET_URL

    show_help: bool = False
    show_version: bool = False


class UseJSONOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'j',
            long_name = 'json',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)
        app_options.json = True

class UseNoColorsOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'nc',
            long_name = 'no-color',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)
        app_options.no_color = True

class UseTestnetOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 't',
            long_name = 'test-net',
            default = DEFAULT_TESTNET_URL,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)

        app_options.testnet = True
        app_options.testnet_url = cast(str, value)

class UseYesToAllOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'y',
            long_name = 'yes',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)
        app_options.yes_to_all = True

class NoInteractiveOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'ni',
            long_name = 'no-interactive',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)
        app_options.interactive = False

class ShowHelpOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'h',
            long_name = 'help',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)
        app_options.show_help = True

class ShowVersionOption(Option):
    def __init__(self):
        super().__init__(
            short_name = 'vr',
            long_name = 'version',
            default = None,
            require_value = False
        )

    def execute(self, value: Optional[Any], options: Options):
        app_options = cast(AppOptions, options)
        app_options.show_version = True

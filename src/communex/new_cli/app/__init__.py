import sys

from communex import __version__
from typing import Optional
from communex.client import CommuneClient
from communex.new_cli.command import Command

from .options import DEFAULT_TESTNET_URL, AppOptions, ShowHelpOption, ShowVersionOption, UseNoColorsOption, UseJSONOption, UseTestnetOption, UseYesToAllOption
from .console import AppConsole
from ..arguments import parse_arguments
from ..options import Option

APP_OPTIONS: list[Option] = [
    UseJSONOption(),
    UseNoColorsOption(),
    UseTestnetOption(),
    UseYesToAllOption(),
    ShowHelpOption(),
    ShowVersionOption()
]

APP_SUBCOMMANDS: dict[str, Command] = {}

class App(Command):
    options: AppOptions = AppOptions()
    _client: Optional[CommuneClient] = None

    console: AppConsole

    def __init__(self) -> None:
        if not sys.stdin.isatty():
            self.options.interactive = False

        if not sys.stdout.isatty() or not sys.stderr.isatty():
            self.options.no_color = False

        self.console = AppConsole(self.options)

    async def client(self) -> CommuneClient:
        if self._client is not None:
            return self._client

        # TODO: Connect to the Commune Client
        _client = None


        self._client = _client
        raise RuntimeError("TODO")

    async def execute(self, args: list[str]) -> int:
        argument_list_end = parse_arguments(
            definitions = APP_OPTIONS,
            options = self.options,
            arguments = args
        )

        if self.options.show_help:
            self.help()
            return 0

        if self.options.show_version:
            self.version()
            return 0

        self.console.reconfigure(self.options)

        args = args[argument_list_end:]

        if len(args) <= 0:
            self.console.error("[red]error:[/red] there is no subcommand provided", markup = True, highlight = False)
            self.help()

            return 1

        name, args = args[0].lower(), args[1:]

        subcommand = APP_SUBCOMMANDS.get(name)

        if not subcommand:
            self.console.error(f"[red]error:[/red] the subcommand [italic]{name}[/italic] doesn't exist!", markup = True)
            self.help()

            return 1

        return subcommand.execute(args)

    def help(self):
        self.console.info("communex [bold]v{}[/bold]".format(__version__), markup = True, highlight = False)
        self.console.info("", markup = True, highlight = False)
        self.console.info("[bold]Usage:[/bold] [dim]cx[/dim] [[italic]...options[/italic]] [bold]<subcommand>[/bold]", markup = True, highlight = False)
        self.console.info("", markup = True, highlight = False)
        self.console.info("[bold]Subcommands:[/bold]", markup = True, highlight = False)
        self.console.info("  [bold][magenta]key[/magenta][/bold]                     Manage keys", highlight = False)
        self.console.info("  [bold][magenta]balance[/magenta][/bold]                 Manage balance", highlight = False)
        self.console.info("  [bold][magenta]misc[/magenta][/bold]                    Manage misc", highlight = False)
        self.console.info("  [bold][magenta]module[/magenta][/bold]                  Manage modules", highlight = False)
        self.console.info("  [bold][magenta]network[/magenta][/bold]                 Manage networks", highlight = False)
        self.console.info("  [bold][magenta]subnet[/magenta][/bold]                  Manage subnets", highlight = False)
        self.console.info("", markup = True, highlight = False)
        self.console.info("[bold]Options:[/bold]", markup = True, highlight = False)
        self.console.info("  [bold]-j[/bold], [bold]--json[/bold]              Enable JSON output", markup = True, highlight = False)
        self.console.info("  [bold]-nc[/bold], [bold]--no-color[/bold]         Forcefully enable colors on consoles that doesn't support them", markup = True, highlight = False)
        self.console.info("  [bold]-t[/bold], [bold]--test-net=<uri>[/bold]    Use the testnet instead of the main network. (default: {})".format(DEFAULT_TESTNET_URL), markup = True, highlight = False)
        self.console.info("  [bold]-y[/bold], [bold]--yes[/bold]               Use yes on all confirmation prompts", markup = True, highlight = False)
        self.console.info("  [bold]-ni[/bold], [bold]--no-interactive[/bold]   Disable interactive mode", markup = True, highlight = False)

    def version(self):
        self.console.info(
            "communex [bold]v{}[/bold]".format(__version__),
            highlight = False,
            markup = True
        )

    @staticmethod
    def get():
        global _app_instance

        if not _app_instance:
            _app_instance = App()

        return _app_instance

_app_instance: Optional[App] = None

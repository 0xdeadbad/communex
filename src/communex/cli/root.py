from typing import Annotated, Optional

import typer
import sys

from communex import __version__

from ._common import ExtraCtxData
from .balance import balance_app
from .key import key_app
from .misc import misc_app
from .module import module_app
from .network import network_app
from .subnet import subnet_app

import rich

interactive = True
color = True

if not sys.stdin.isatty():
    interactive = False

if not sys.stdout.isatty() or not sys.stderr.isatty():
    color = False

rich.reconfigure(no_color = not color)

app = typer.Typer(
    no_args_is_help = True
)

app.add_typer(
    key_app,
    name = "key",
    help = "Key operations"
)
app.add_typer(
    balance_app,
    name = "balance",
    help = "Balance operations"
)
app.add_typer(
    typer_instance = misc_app,
    name = "misc",
    help = "Other operations"
)
app.add_typer(
    module_app,
    name = "module",
    help = "Module operations"
)
app.add_typer(
    network_app,
    name = "network",
    help = "Network operations"
)
app.add_typer(
    subnet_app,
    name = "subnet",
    help = "Subnet operations"
)

def _version_callback(value: bool):
    if value:
        print(f"CommuneX {__version__}")
        raise typer.Exit()

def flag_option(
    flag: str,
    flag_envvar: str,
    flag_help: str,
    flag_short: str | None = None,
):
    flag_long = f"--{flag}"
    flag_short = f"-{flag[0]}" if flag_short is None else f"-{flag_short}"
    return typer.Option(
        flag_long,
        flag_short,
        is_flag = True,
        envvar = flag_envvar,
        help = flag_help
    )


@app.callback()
def main(
    ctx: typer.Context,
    json: Annotated[
        bool,
        flag_option(
            "json", "COMX_OUTPUT_JSON", "Output machine-readable JSON."
        ),
    ] = False,
    testnet: Annotated[
        bool,
        flag_option("testnet", "COMX_USE_TESTNET", "Use testnet endpoints."),
    ] = False,
    yes_to_all: Annotated[
        bool,
        flag_option(
            "yes", "COMX_YES_TO_ALL", "Say yes to all confirmation inputs."
        ),
    ] = False,
    no_interactive: Annotated[
        bool,
        flag_option(
            "no-interactive", "COMX_NO_INTERACTIVE", "Disable interactive mode", "i"
        )
    ] = False,
    no_color: Annotated[
        bool,
        flag_option(
            "no-color", "COMX_NO_COLOR", "Disable output colors", "c"
        )
    ] = False,
    version: Annotated[
        Optional[bool], typer.Option(callback=_version_callback)
    ] = None,
):
    """
    CommuneX CLI {version}

    This command line interface is under development and subject to change.
    """
    global interactive
    global color

    if no_interactive:
        interactive = False

    if no_color:
        color = False

    # Pass the extra context data to the subcommands.
    ctx.obj = ExtraCtxData(
        output_json = json,
        use_testnet = testnet,
        yes_to_all = yes_to_all,
        color = color,
        interactive = interactive
    )


assert main.__doc__
main.__doc__ = main.__doc__.format(version = __version__)

from typing import Any
from rich.console import Console
from communex.new_cli.app.options import AppOptions
import rich
import json

class AppConsole():
    options: AppOptions

    stdout: Console
    stderr: Console

    def __init__(self, options: AppOptions):
        self.reconfigure(options)

    def reconfigure(self, options: AppOptions):
        self.options = options

        no_color = False

        if options.no_color is not None and options.no_color:
            no_color = True

        rich.reconfigure(no_color = no_color)
        self.stdout = Console(no_color = no_color)
        self.stderr = Console(stderr = True, no_color = no_color)

    def info(
        self,
        message: Any,
        use_stderr: bool = False,
        *args: Any,
        **kwargs: Any
    ):
        final_message: str = message
        print_options: dict[str, Any] = {}

        if self.options.json:
            final_message = json.dumps({
                'type': 'log',
                'kind': 'info',
                'message': message
            })

            print_options['crop'] = False
            print_options['overflow'] = 'ignore'
            print_options['soft_wrap'] = False

        if use_stderr:
            self.stderr.print(
                final_message,
                *args,
                **kwargs,
                **print_options
            )
        else:
            self.stdout.print(
                final_message,
                *args,
                **kwargs,
                **print_options
            )


    def error(self, message: Any, *args: Any, **kwargs: Any):
        final_message: str = message
        print_options: dict[str, Any] = {}

        if self.options.json:
            final_message = json.dumps({
                'type': 'log',
                'kind': 'error',
                'message': message
            })

            print_options['crop'] = False
            print_options['overflow'] = 'ignore'
            print_options['soft_wrap'] = False

        self.stderr.print(
            final_message,
            *args,
            **kwargs,
            **print_options
        )

    def data(self, data: Any, *args: Any, **kwargs: Any):
        final_message = data
        print_options: dict[str, Any] = {}

        if self.options.json:
            final_message = json.dumps({
                'type': 'data',
                'data': data
            })

            print_options['crop'] = False
            print_options['overflow'] = 'ignore'
            print_options['soft_wrap'] = False

        self.stderr.print(final_message, *args, **kwargs, **print_options)

    def json_data(self, **kwargs: Any):
        self.stderr.print(
            json.dumps({
                'type': 'data',
                'data': { **kwargs }
            }),

            crop = False,
            overflow = 'ignore',
            soft_wrap = False
        )

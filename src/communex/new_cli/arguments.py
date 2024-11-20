import sys
import inspect
import asyncio
from .options import Option, Options

def parse_arguments(
    definitions: list[Option],
    arguments: list[str],
    options: Options,
):
    """
    Parse the defined arguments in `definitions` that are found in `arguments` array
    """

    len_args = len(arguments)
    last_opt_index = len_args

    for index, arg in enumerate(arguments):
        if arg == '--': # Reached stop indicator: --
            last_opt_index = index
            break

        if not arg.startswith('-'): # Reached positional arguments
            last_opt_index = index
            break

        long_argument = arg.startswith('--')

        if long_argument:
            raw_option = arg[2:]
            name = None
            value = None

            if raw_option.find('=') != -1:
                name, value = raw_option.split('=', 1)
            else:
                name = raw_option

            matches = list(filter(lambda x: x.long_name == name, definitions))

            if len(matches) <= 0:
                continue

            if len(matches) > 1:
                sys.stderr.write(f'FATAL: More than two flags with the same long-name were provided.\n')
                sys.stderr.write(f'       Please contact the developer to fix this, this isn\'t supposed to happen.\n')
                sys.exit(1)

            first = matches[0]

            if first.require_value and not value:
                sys.stderr.write(f'ERROR: The flag {name} requires an value, but none were provided.')
                sys.exit(1)

            if inspect.iscoroutinefunction(first.execute):
                # Run asynchronous function as sync,
                # as we want to wait for the option to run it's code.
                asyncio.run(first.execute(
                    value = first.default if value is None else value,
                    options = options
                ))
            else:
                first.execute(
                    value = first.default if value is None else value,
                    options = options
                )
        else:
            raw_option = arg[1:]
            name = None
            value = None

            if raw_option.find('=') != -1:
                name, value = raw_option.split('=', 1)
            else:
                name = raw_option

            matches = list(filter(lambda x: x.short_name == name, definitions))

            if len(matches) <= 0:
                continue

            if len(matches) > 1:
                sys.stderr.write(f'FATAL: More than two flags with the same short-name were provided.')
                sys.stderr.write(f'       Please contact the developer to fix this, this isn\'t supposed to happen.')
                sys.exit(1)

            first = matches[0]

            if first.require_value and not value:
                sys.stderr.write(f'ERROR: The flag {name} requires an value, but none were provided.')
                sys.exit(1)

            if inspect.iscoroutinefunction(first.execute):
                # Run asynchronous function as sync,
                # as we want to wait for the option to run it's code.
                asyncio.run(first.execute(
                    value = first.default if value is None else value,
                    options = options
                ))
            else:
                first.execute(
                    value = first.default if value is None else value,
                    options = options
                )

    return last_opt_index

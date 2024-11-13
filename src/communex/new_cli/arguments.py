from .options import Option, Options

def parse_arguments(
    definitions: list[Option],
    arguments: list[str],
    options: Options,
):
    """
    Parse the defined arguments in `definitions` that are found in `arguments` array
    """
    for index, arg in enumerate(arguments):
        if arg == '--': # Reached stop indicator: --
            break

        if not arg.startswith('-'): # Reached positional arguments
            break

        long_argument = arg.startswith('--')

        if long_argument:
            name = arg[2:]

            matches = list(filter(lambda x: x.long_name == name, definitions))

            if len(matches) < 0:
                continue

        else:
            name = arg[1:]

            matches = list(filter(lambda x: x.short_name == name, definitions))

            if len(matches) < 0:
                continue

        index += 1

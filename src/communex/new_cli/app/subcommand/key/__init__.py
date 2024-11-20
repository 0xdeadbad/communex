from typing import Any
from communex.new_cli.options import Option
from ....command import Command

# Subcommands:
# balances                           Gets balances of all keys.
# create                             Generates a new key and stores it on a disk with the given name.
# list                               Lists all keys stored on disk.
# power-delegation                   Gets power delegation of a key.
# regen                              Stores the given key on a disk. Works with private key or mnemonic.
# show                               Show information about a key.
# stakefrom                          Gets what keys is key staked from.
# staketo                            Gets stake to a key.
# total-balance                      Returns total tokens of all keys on a d
# total-free-balance                 Returns total balance of all keys on a d
# total-staked-balance               Returns total stake of all keys on a d

KEY_OPTIONS: list[Option] = [

]

KEY_SUBCOMMANDS: dict[str, Command] = {}

class KeyCommand(Command):
    def __init__(self):
        super().__init__('key', 'Manage keys')

    async def execute(self, args: list[str]) -> Any:
        pass



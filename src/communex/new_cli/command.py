from typing import Any

class Command():
    name: str
    description: str

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(
        self,
        args: list[str]
    ) -> Any: pass

    def help(self) -> Any: pass

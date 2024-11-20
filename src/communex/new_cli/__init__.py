import asyncio
import sys
from .app import App

async def main(args: list[str]) -> int:
    app = App.get()

    return await app.execute(args = args)

def entrypoint() -> int:
    args = sys.argv[1:]

    return asyncio.run(main(args))

if __name__ == '__main__':
    entrypoint()

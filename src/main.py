import asyncio
from src.cli import cli


def main():
    """ Точка входа """
    asyncio.run(cli())


if __name__ == "__main__":
    main()

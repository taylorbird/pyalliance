# pylint: disable=missing-function-docstring

import time
from argparse import ArgumentParser, Namespace
from typing import Optional, Dict, Any, List

from replbuilder import ReplCommand, ReplRunner

from pytelink import Controller, Light


class Cli:
    """
    The primary Cli class
    """

    @staticmethod
    def basic_parser() -> ArgumentParser:
        parser = ArgumentParser()
        return parser

    @staticmethod
    def light_parser() -> ArgumentParser:
        parser = ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "light",
            type=int,
            nargs="?",
            help="a light address",
        )
        group.add_argument("--all", "-a", help="all lights", action="store_true")
        return parser

    @staticmethod
    def color_parser() -> ArgumentParser:
        parser = Cli.light_parser()
        parser.add_argument("r", type=int)
        parser.add_argument("g", type=int)
        parser.add_argument("b", type=int)
        return parser

    @staticmethod
    def temperature_parser() -> ArgumentParser:
        parser = Cli.light_parser()
        parser.add_argument("temperature", type=int)
        return parser

    @staticmethod
    def brightness_parser() -> ArgumentParser:
        parser = Cli.light_parser()
        parser.add_argument("brightness", type=int)
        return parser

    def __init__(self) -> None:
        self.controller = Controller("FF:00:05:08:0A:8B", "Back", "2846")
        self.controller.start()
        self.controller.process_notifications(5)

    def list(self, _args: Any) -> None:
        print("\n".join(str(x) for x in self.controller.lights().values()))

    def show(self, args: Namespace) -> None:
        for light in self.select_lights(args):
            print(light)

    def on(self, args: Namespace) -> None:
        for light in self.select_lights(args):
            light.turn_on()

    def off(self, args: Namespace) -> None:
        for light in self.select_lights(args):
            light.turn_off()

    def color(self, args: Namespace) -> None:
        for light in self.select_lights(args):
            light.set_color(args.r, args.g, args.b)

    def temp(self, args: Namespace) -> None:
        for light in self.select_lights(args):
            light.set_temperature(args.temperature)

    def brightness(self, args: Namespace) -> None:
        for light in self.select_lights(args):
            light.set_brightness(args.brightness)

    def select_lights(self, args: Namespace) -> List[Light]:
        if args.all:
            return [self.controller.all()]
        return [self.controller.light(args.light)]


def main(_args: Optional[Dict[str, str]] = None) -> None:
    """
    The main routine.
    """

    cli = Cli()

    list_cmd = ReplCommand("list", Cli.basic_parser(), cli.list, "Show a list of detected lights")
    show_cmd = ReplCommand("show", Cli.light_parser(), cli.show, "Show the status of a light")
    on_cmd = ReplCommand("on", Cli.light_parser(), cli.on, "Turn a light on")
    off_cmd = ReplCommand("off", Cli.light_parser(), cli.off, "Turn a light off")
    color_cmd = ReplCommand("color", Cli.color_parser(), cli.color, "Set a light's color")
    temp_cmd = ReplCommand("temp", Cli.temperature_parser(), cli.temp, "Set a light's color temperature")
    brightness_cmd = ReplCommand("brightness", Cli.brightness_parser(), cli.brightness, "Set a light's brightness")

    runner = ReplRunner("pytelinkcli", vi_mode=True)
    runner.add_commands(
        [list_cmd, show_cmd, on_cmd, off_cmd, color_cmd, temp_cmd, brightness_cmd], namespace="Control lights"
    )
    # runner.add_aliases({"cs": "cowsay -w", "fac": "factorial"})
    runner.run()

    time.sleep(900)

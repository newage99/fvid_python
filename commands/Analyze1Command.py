import sys
from commands.Command import Command


class Analyze1Command(Command):

    @staticmethod
    def str_to_execute_command():
        return "analyze1"

    @staticmethod
    def description():
        return "Analyzes degree and diameter properties of topologies."

    @staticmethod
    def print_help():
        pass

    @staticmethod
    def execute(arguments):
        pass


if __name__ == '__main__':
    Analyze1Command.execute(sys.argv[1:])

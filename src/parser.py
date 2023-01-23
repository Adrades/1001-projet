import argparse


class pyNvPDParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(
            prog="pyNvPD",
            description="Python Implementation of NvPD algorithm",
            epilog="See in pyproject.toml for more informations",
        )
        self.define_args()

    def define_args(self):
        self.add_argument(
            "-f",
            "--fasta",
            default=[],
            action="append",
            help="Load a sequence from fasta file path.",
        )

        self.add_argument(
            "-t",
            "--text",
            default=[],
            action="append",
            help="Input a sequence directly",
        )

        self.add_argument(
            "-v", "--verbose", action="store", help="Print more logging messages"
        )

        self.add_argument(
            "-e",
            "--edt",
            "--edit_distance_table",
            action="store",
            help="Output the full distance table",
        )

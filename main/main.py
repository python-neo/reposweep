from pathlib import Path
from argparse import ArgumentParser, REMAINDER
import sys
from typing import Optional

MARKER_FILE = "reposweep.yml"

class Commands :
    def __init__ (self) -> None :
        self.commands = {
            "init" : {"func" : self.init, "subcmd" : False, "rest" : False}
        }
        self.project_root : Path | None = None

    def init (self) -> str | None :
        ...

def require_project_root () -> Path :
    current = Path.cwd ().resolve ()
    root = next ((p for p in [current, *current.parents] if (p / "reposweep.yml").exists ()), None)
    if root is None : 
        sys.exit ("Not inside a RepoSweep project (run: 'reposweep init').")
    return root

def parse_tokens (tokens : list [str]) -> tuple :
    if not tokens :
        return "help", None, None
    command = tokens [0].strip () or "help"
    subcmd = tokens [1] if len (tokens) > 1 else None
    rest = " ".join (tokens [2:]) if len (tokens) > 2 else None
    return command, subcmd, rest

def run_command (commands : Commands, command : str, subcmd : Optional [str], rest : Optional [str]) -> None :
    
    entry = commands.commands.get (command, {})
    if not entry :
        sys.exit (f"ERROR: Unknown command '{command}'.")

    if command != "init" :
        commands.project_root = require_project_root ()

    func = entry.get ("func")
    if not func :
        sys.exit (f"ERROR: Command '{command}' is not implemented.")

    want_subcmd = entry.get ("subcmd", False)
    want_rest = entry.get ("rest", False)
    args : list = []

    if want_subcmd is True :
        if not subcmd :
            sys.exit (f"ERROR: '{command}' missing arguments.")
        args.append (subcmd)
    elif want_subcmd is None :
        args.append (subcmd if subcmd else None)
    else :
        if subcmd :
            sys.exit (f"ERROR: '{command}' does not accept a subcommand.")

    rest_exists = bool (rest)
    if want_rest is True :
        if not rest_exists :
            sys.exit (f"ERROR: '{command}' missing arguments.")
        args.append (rest)
    elif want_rest is None :
        args.append (rest if rest_exists else None)
    else :
        if rest_exists :
            sys.exit (f"ERROR: '{command}' does not accept extra arguments.")

if __name__ == "__main__" :
    argparser = ArgumentParser (add_help = False)
    argparser.add_argument ("command", nargs = REMAINDER, help = "RepoSweep commands")
    args = argparser.parse_args ()

    commands = Commands ()
    command, subcmd, rest = parse_tokens (args.command)
    run_command (commands, command, subcmd, rest)
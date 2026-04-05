from pathlib import Path
from argparse import ArgumentParser, REMAINDER
import sys
from typing import Optional
from yaml import safe_dump, safe_load

MARKER_FILE = "reposweep.yml"

class Commands :
    def __init__ (self) -> None :
        self.commands = {
            "init" : {"func" : self.init, "subcmd" : False, "rest" : False},
            "scan" : {"func" : self.scan, "subcmd" : False, "rest" : False}
        }
        self.project_root : Path | None = require_project_root ()

    def init (self) -> str | None :
        if self.project_root is not None :
            sys.exit (f"Config file 'reposweep.yml' already exists in {self.project_root}.")
        data = {
            "roots" : ["."],
            "ignore" : [
                ".git", "node_modules", ".venv", "__pycache__", ".pytest_cache",
                ".mypy_cache", ".ruff_cache", ".tox", "venv", "dist",
                "build", ".eggs", ".idea"
                ],
            "max_depth" : 4}
        
        with open ("reposweep.yml", "w", encoding = "utf-8") as f :
            safe_dump (data, f, indent = 2, sort_keys = False)
        sys.exit ("Initialized reposweep.yml")

    def scan (self) -> None :
        if self.project_root is None :
            sys.exit ("Not inside a RepoSweep project (run: 'reposweep init').")
        config_path = self.project_root / MARKER_FILE
        with open (config_path, "r") as f :
            data = safe_load (f) or {}

        roots = data.get ("roots", ["."])
        if isinstance (roots, str) :
            roots = [roots]
        ignore = set (data.get ("ignore", []))

        base_dirs : list [Path] = []
        for item in roots :
            if str (item) == "." :
                p = self.project_root
            else :
                p = Path (item).resolve ()
            if p.exists () :
                base_dirs.append (p)
            else :
                print (f"WARNING: root path not found: {p}")

        found : list [Path] = []
        for base in base_dirs :
            stack : list [tuple [Path, int]] = [(base, 0)]
            while stack :
                current, depth = stack.pop ()
                if current.name in ignore :
                    continue

                if (current / ".git").exists () :
                    found.append (current)
                    continue
                if depth >= int (data.get ("max_depth", 4)) :
                    continue

                try :
                    children = [p for p in current.iterdir () if p.is_dir ()]
                except OSError :
                    continue

                for child in sorted (children, key = lambda p: p.name) :
                    if child.name in ignore :
                        continue
                    stack.append ((child, depth + 1))

        if not found :
            print ("No repos found.")
        for repo in sorted (set (found)) :
            print (repo)


def require_project_root () -> Optional [Path] :
    base_dir = Path.cwd ().resolve ()
    if exit :
        return next ((p for p in [base_dir, *base_dir.parents] if (p / MARKER_FILE).exists ()), None)
    return next ((p for p in [base_dir, *base_dir.parents] if (p / MARKER_FILE).exists ()), None)


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

    func (*args)

if __name__ == "__main__" :
    argparser = ArgumentParser (add_help = False)
    argparser.add_argument ("command", nargs = REMAINDER, help = "RepoSweep commands")
    args = argparser.parse_args ()

    commands = Commands ()
    command, subcmd, rest = parse_tokens (args.command)
    run_command (commands, command, subcmd, rest)
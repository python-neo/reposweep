from pathlib import Path
from argparse import ArgumentParser, REMAINDER
import sys
from typing import Optional
from yaml import safe_dump, safe_load
from subprocess import run
from rich.panel import Panel
from .console import get_console

MARKER_FILE = "reposweep.yml"
VERSION = "0.4.0"

class Commands :
    def __init__ (self, no_color : bool = False) -> None :
        self.commands = {
            "init" : {"func" : self.init, "subcmd" : False, "rest" : False},
            "scan" : {"func" : self.scan, "subcmd" : False, "rest" : False}
        }
        self.console = get_console (no_color)
        self.project_root : Path | None = require_project_root (exit = False)

    def init (self) -> None :
        if self.project_root is not None :
            self.console.print (f"[error]ERROR[/]: config already exists in [path]{self.project_root}[/]")
            sys.exit (1)
        data = {
            "roots" : ["."],
            "ignore" : [
                ".git", "node_modules", ".venv", "__pycache__", ".pytest_cache",
                ".mypy_cache", ".ruff_cache", ".tox", "venv", "dist",
                "build", ".eggs", ".idea"
            ],
            "max_depth" : 4
        }
        with open ("reposweep.yml", "w", encoding = "utf-8") as f :
            safe_dump (data, f, indent = 2, sort_keys = False)
        self.console.print ("[success]Initialized reposweep.yml[/]")
        sys.exit (0)

    def list_repos (self) -> list [Path] :
        if self.project_root is None :
            self.console.print ("[error]ERROR[/]: not inside a RepoSweep project (run: 'reposweep init').")
            sys.exit (1)
        data = load_config (self.project_root)
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
                self.console.print (f"[warning]WARNING[/]: root path not found: [path]{p}[/]")
        found : list [Path] = []
        max_depth = int (data.get ("max_depth", 4))
        for base in base_dirs :
            stack : list [tuple [Path, int]] = [(base, 0)]
            while stack :
                current, depth = stack.pop ()
                if current.name in ignore :
                    continue
                if (current / ".git").exists () :
                    found.append (current)
                    continue
                if depth >= max_depth :
                    continue
                try :
                    children = [p for p in current.iterdir () if p.is_dir ()]
                except OSError :
                    continue
                for child in sorted (children, key = lambda p: p.name) :
                    if child.name in ignore :
                        continue
                    stack.append ((child, depth + 1))
        return sorted (set (found))

    def scan (self) -> None :
        repos = self.list_repos ()
        if not repos :
            self.console.print ("[info]No repos found.[/]")
            return
        groups : dict [str, list [str]] = {"Dirty" : [], "Behind" : [], "Ahead" : [], "Clean" : []}
        for repo in repos :
            dirty_flag = git_dirty (repo)
            ahead, behind = git_ahead_behind (repo)
            detail = ", ".join ([f"ahead {ahead}" if ahead else "", f"behind {behind}" if behind else ""]).strip (", ").strip ()
            suffix = f" [info]({detail})[/]" if detail and dirty_flag else ""
            if dirty_flag :
                groups ["Dirty"].append (f"[path]{repo}[/]{suffix}")
            elif behind :
                groups ["Behind"].append (f"[path]{repo}[/] [info](behind {behind})[/]")
            elif ahead :
                groups ["Ahead"].append (f"[path]{repo}[/] [info](ahead {ahead})[/]")
            else :
                groups ["Clean"].append (f"[path]{repo}[/]")
        panels = [
            Panel.fit ("\n".join (groups ["Dirty"]) or "-", title = "Dirty", border_style = "warning"),
            Panel.fit ("\n".join (groups ["Behind"]) or "-", title = "Behind", border_style = "error"),
            Panel.fit ("\n".join (groups ["Ahead"]) or "-", title = "Ahead", border_style = "info"),
            Panel.fit ("\n".join (groups ["Clean"]) or "-", title = "Clean", border_style = "success")
        ]
        for panel in panels : self.console.print (panel)

def load_config (project_root : Path) -> dict :
    config_path = project_root / MARKER_FILE
    with open (config_path, "r", encoding = "utf-8") as f :
        return safe_load (f) or {}

def git_capture (repo : Path, args : list [str]) -> tuple [int, str] :
    result = run (["git", "-C", str (repo), *args], capture_output = True, text = True)
    return result.returncode, result.stdout.strip ()

def git_dirty (repo : Path) -> bool :
    code, out = git_capture (repo, ["status", "--porcelain"])
    return code == 0 and bool (out)

def git_ahead_behind (repo : Path) -> tuple [int, int] :
    code, _ = git_capture (repo, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if code != 0 :
        return 0, 0
    code, out = git_capture (repo, ["rev-list", "--left-right", "--count", "HEAD...@{u}"])
    if code != 0 :
        return 0, 0
    parts = out.split ()
    if len (parts) != 2 :
        return 0, 0
    return int (parts [0]), int (parts [1])

def require_project_root (exit : bool = True) -> Optional [Path] :
    base_dir = Path.cwd ().resolve ()
    root = next ((p for p in [base_dir, *base_dir.parents] if (p / MARKER_FILE).exists ()), None)
    if root is None and exit :
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
        commands.console.print (f"[error]ERROR[/]: unknown command '{command}'.")
        sys.exit (1)
    if command != "init" :
        commands.project_root = require_project_root ()
    func = entry.get ("func")
    if not func :
        commands.console.print (f"[error]ERROR[/]: command '{command}' is not implemented.")
        sys.exit (1)
    want_subcmd = entry.get ("subcmd", False)
    want_rest = entry.get ("rest", False)
    args : list = []
    if want_subcmd is True :
        if not subcmd :
            commands.console.print (f"[error]ERROR[/]: '{command}' missing arguments.")
            sys.exit (1)
        args.append (subcmd)
    elif want_subcmd is None :
        args.append (subcmd if subcmd else None)
    else :
        if subcmd :
            commands.console.print (f"[error]ERROR[/]: '{command}' does not accept a subcommand.")
            sys.exit (1)
    rest_exists = bool (rest)
    if want_rest is True :
        if not rest_exists :
            commands.console.print (f"[error]ERROR[/]: '{command}' missing arguments.")
            sys.exit (1)
        args.append (rest)
    elif want_rest is None :
        args.append (rest if rest_exists else None)
    else :
        if rest_exists :
            commands.console.print (f"[error]ERROR[/]: '{command}' does not accept extra arguments.")
            sys.exit (1)
    func (*args)

if __name__ == "__main__" :
    raw = sys.argv [1:]
    no_color = False
    if "--no-color" in raw :
        no_color = True
        raw = [arg for arg in raw if arg != "--no-color"]
    if "--version" in raw :
        print (VERSION)
        raise SystemExit (0)
    argparser = ArgumentParser (add_help = False)
    argparser.add_argument ("command", nargs = REMAINDER, help = "RepoSweep commands")
    args = argparser.parse_args (raw)
    commands = Commands (no_color = no_color)
    command, subcmd, rest = parse_tokens (args.command)
    run_command (commands, command, subcmd, rest)
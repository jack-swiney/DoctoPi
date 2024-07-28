"""DoctoPi main entrypoint"""
# Built-in imports
import argparse
import importlib
import importlib.resources
import os
import shutil
import sys
from typing import Dict, List, Type

# This package imports
from doctopi.cli import cli, parse_settings, DoctoPiConfigError
from doctopi.formatter.markdown.markdown_builder import MarkdownBuilder
from doctopi.formatter.markdown.cmd import *  # pylint: disable = wildcard-import # noqa F403


MARKDOWN_CMDS: Dict[str, Type] = {
    "classes": MarkdownClassCommand,  # noqa: F405
    "functions": MarkdownFunctionCommand,  # noqa: F405
    "constructor": MarkdownConstructorCommand,  # noqa: F405
    "inner_classes": MarkdownInnerClassCommand,  # noqa: F405
    "class_variables": MarkdownClassVarCommand,  # noqa: F405
    "instance_variables": MarkdownInstanceVarCommand,  # noqa: F405
    "methods": MarkdownMethodsCommand,  # noqa: F405
    "arguments": MarkdownArgsCommand,  # noqa: F405
    "raises": MarkdownRaisesCommand,  # noqa: F405
    "returns": MarkdownReturnsCommand  # noqa: F405
}
"""Map INI config strings for commands to MarkdownCommand types"""


def main(raw_args: List[str]):
    """Main method for DoctoPi

    Args:
        raw_args (List[str]): System args

    Raises:
        NotImplementedError: Running a command that isn't implemented
    """
    args = cli(raw_args)

    if args.command == "markdown":
        # Combine args with ini config
        args = parse_settings(args)

        if args.recursive:
            # Disable the all-in-one recursion style
            args.recursive_all_in_one = False

            # Walk through the directories and generate a readme for each
            for dirpath, _, _ in os.walk(args.input):
                args.title = os.path.basename(dirpath)
                args.input = dirpath
                # Modify output to point to a file in the dirpath
                args.output = os.path.join(dirpath, os.path.basename(args.output))

                markdown(args)

        else:
            markdown(args)

    # Generate a default INI file
    elif args.command == "generate-ini":

        # Copy default.ini to destination
        shutil.copy(importlib.resources.files("doctopi.cli") / "default.ini", args.output)

    else:
        raise NotImplementedError(args.command)


def markdown(args: argparse.Namespace):
    """Build and execute a MarkdownBuilder

    Args:
        args (argparse.Namespace): CLI arguments

    Raises:
        DoctoPiConfigError: If a command from the ini doesn't exist
    """
    # Instantiate a MarkdownBuilder
    builder = MarkdownBuilder() \
        .configure_metadata(args.title, args.author) \
        .align_tables(args.table_align) \
        .configure_src(args.src_language, args.docstring_style) \
        .configure_io(args.input, args.output, args.recursive_all_in_one)

    # Toggle markdown settings
    for config in ["constructors", "class_vars", "instance_vars", "methods",
                   "inner_classes", "file_overview", "public_only"]:
        if not getattr(args, config, True):
            builder.toggle(config)

    # Toggle a table of contents
    if args.table_of_contents:
        builder.enable_toc(args.toc_depth, args.toc_title)

    # Add commands to the Builder to organize documentation for files
    for cmd in args.file_cmds.split(","):
        try:
            builder.add_file_command(MARKDOWN_CMDS[cmd])
        except KeyError as exc:
            raise DoctoPiConfigError from exc

    # Add commands to the Builder to organize documentation for classes
    for cmd in args.class_cmds.split(","):
        try:
            builder.add_class_commands(MARKDOWN_CMDS[cmd])
        except KeyError as exc:
            raise DoctoPiConfigError from exc

    # Add commands to the Builder to organize documentation for functions
    for cmd in args.func_cmds.split(","):
        try:
            builder.add_function_commands(MARKDOWN_CMDS[cmd])
        except KeyError as exc:
            raise DoctoPiConfigError from exc

    # Generate the documentation
    builder.build()


if __name__ == "__main__":
    main(sys.argv[1:])

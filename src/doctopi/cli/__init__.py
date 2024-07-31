"""Command-Line Interface (CLI). Defines the entrypoint for DoctoPi."""
# Built-in imports
import argparse
import configparser
import os
from typing import List


class DoctoPiConfigError(Exception):
    """Error occurred while configuration DoctoPi"""


def cli(sys_args: List[str]) -> argparse.Namespace:
    """Command-Line Interface (CLI)

    Args:
        sys_args (List[str]): Arguments from the command line

    Returns:
        argparse.Namespace: Parsed arguments from CLI
    """
    parser = argparse.ArgumentParser(description="Generate documentation in various formats.")
    subparsers = parser.add_subparsers(dest="command", help="Output language commands")

    # Generate INI command
    generate_ini_parser = subparsers.add_parser(
        "generate-ini",
        help="Generate DoctoPi default INI configuration file.")
    generate_ini_parser.add_argument("-o", "--output", default="doctopi.ini",
                                     help="Output a default DoctoPi INI config file")

    # Markdown command
    markdown_parser = subparsers.add_parser("markdown", help="Generate Markdown documentation")

    markdown_parser.add_argument("-i", "--input", required=True,
                                 help="Source file or directory to parse")
    markdown_parser.add_argument("-o", "--output", default="README.md",
                                 help="Output Markdown file")
    markdown_parser.add_argument("-c", "--config", default="./doctopi.ini",
                                 help="Path to doctopi ini configuration file.")
    markdown_parser.add_argument("-l", "--src-language", choices=["python", "java", "cpp"],
                                 required=False,
                                 help="Programming language of source code")
    markdown_parser.add_argument("-d", "--docstring-style", required=False,
                                 help="Docstring flavor (E.g. Sphinx, Google, JavaDoc)")
    markdown_parser.add_argument("-r", "--recursive", action="store_true",
                                 help="Recursively create a markdown file in each parsed directory")
    markdown_parser.add_argument("--recursive-all-in-one", action="store_true",
                                 help="Create a single markdown file with contents of files and "
                                      "directories parsed recursively.")
    markdown_parser.add_argument("-t", "--title", required=False,
                                 help="Title of the Markdown document")
    markdown_parser.add_argument("-a", "--author", required=False,
                                 help="Author of the Markdown document")
    markdown_parser.add_argument("--toc-depth", type=int, required=False,
                                 help="Heading depth of the table of contents")
    markdown_parser.add_argument("--toc-title", required=False,
                                 help="Title for the table of contents")
    markdown_parser.add_argument("--table-align", choices=["left", "center", "right"],
                                 required=False,
                                 help="Text alignment for all markdown tables")

    # Enable content toggles
    toggle_group = markdown_parser.add_argument_group("Content Toggles")

    toggle_group.add_argument("--no-table-of-contents", action="store_false",
                              dest="table_of_contents",
                              help="Don't render a table of contents")
    toggle_group.add_argument("--no-constructors", action="store_false", dest="constructors",
                              help="Do not document constructors")
    toggle_group.add_argument("--no-class-vars", action="store_false", dest="class_vars",
                              help="Do not document class variables")
    toggle_group.add_argument("--no-instance-vars", action="store_false", dest="instance_vars",
                              help="Do not document instance variables")
    toggle_group.add_argument("--no-inner-classes", action="store_false", dest="inner_classes",
                              help="Do not document inner classes")
    toggle_group.add_argument("--no-methods", action="store_false", dest="methods",
                              help="Do not document class methods")
    toggle_group.add_argument("--no-file-overview", action="store_false", dest="file_overview",
                              help="Do not document file overview")
    toggle_group.add_argument("--public-only", action="store_true",
                              help="Document only public class methods")

    return parser.parse_args(sys_args)


def parse_settings(cli_args: argparse.Namespace) -> argparse.Namespace:
    """Combine INI config settings with parsed arguments from CLI

    Args:
        cli_args (argparse.Namespace): Parsed CLI arguments

    Returns:
        argparse.Namespace: Combined INI config and CLI arguments
    """

    # Read the default configuration
    default_config = configparser.ConfigParser()
    default_config.read(os.path.join(os.path.dirname(__file__), "default.ini"))

    # Read the provided configuration
    config = configparser.ConfigParser()
    try:
        config.read(cli_args.config)
    except AttributeError:
        pass

    # Combine provided config with defaults
    config = combine_configs(default_config, config)

    # Set source language
    cli_args.src_language = cli_args.src_language \
        if cli_args.src_language else config["MAIN"]["src_language"]

    # Set docstring style
    cli_args.docstring_style = cli_args.docstring_style \
        if cli_args.docstring_style else config["MAIN"]["docstring_style"]

    # Set file commands
    setattr(cli_args, "file_cmds", config["ORGANIZATION"]["file_docs"])

    # Set class commands
    setattr(cli_args, "class_cmds", config["ORGANIZATION"]["class_docs"])

    # Set function commands
    setattr(cli_args, "func_cmds", config["ORGANIZATION"]["function_docs"])

    # Set Markdown title
    cli_args.title = cli_args.title if cli_args.title else config["MARKDOWN"]["title"]

    # Set Markdown author
    cli_args.author = cli_args.author if cli_args.author else config["MARKDOWN"]["author"]

    # Toggle a table of contents
    cli_args.table_of_contents = \
        cli_args.table_of_contents and ini_to_bool(config["TABLE_OF_CONTENTS"]["enabled"])

    # Set Markdown table of contents depth
    cli_args.toc_depth = cli_args.toc_depth \
        if cli_args.toc_depth else int(config["TABLE_OF_CONTENTS"]["depth"])

    # Set Markdown table of contents title
    cli_args.toc_title = cli_args.toc_title \
        if cli_args.toc_title else config["TABLE_OF_CONTENTS"]["title"]

    # Set Markdown table alignment
    cli_args.table_align = cli_args.table_align \
        if cli_args.table_align else config["MARKDOWN"]["table_align"]

    # Toggle content for constructors
    cli_args.constructors = cli_args.constructors and ini_to_bool(config["CONTENT"]["constructors"])

    # Toggle content for class variables
    cli_args.class_vars = cli_args.class_vars and ini_to_bool(config["CONTENT"]["class_vars"])

    # Toggle content for instance variables
    cli_args.instance_vars = \
        cli_args.instance_vars and ini_to_bool(config["CONTENT"]["instance_vars"])

    # Toggle content for methods
    cli_args.methods = cli_args.methods and ini_to_bool(config["CONTENT"]["methods"])

    # Toggle content for inner classes
    cli_args.inner_classes = \
        cli_args.inner_classes and ini_to_bool(config["CONTENT"]["inner_classes"])

    # Toggle content for constructors
    cli_args.file_overview = cli_args.file_overview and ini_to_bool(config["CONTENT"]["overview"])

    # Toggle content for public methods only
    cli_args.public_only = cli_args.public_only or ini_to_bool(config["CONTENT"]["public_only"])

    return cli_args


def combine_configs(default_config: configparser.ConfigParser,
                    override_config: configparser.ConfigParser) -> configparser.ConfigParser:
    """Combine two config parsers, favoring the `override_config`

    Args:
        default_config (configparser.ConfigParser): Config containing
            default values. Any args in the `override_config` will
            override these args.
        override_config (configparser.ConfigParser): Config will be
            combined with the `default_config`, overriding any common
            arguments.

    Raises:
        DoctoPiConfigError: If the `override_config` contains any
            sections or keys not in `default_config`.

    Returns:
        configparser.ConfigParser: _description_
    """
    # Initialize a combined config object
    combined_config = configparser.ConfigParser()
    combined_config.read_dict(default_config)

    for section in override_config.sections():
        # Verify it is a valid section
        if not combined_config.has_section(section):
            raise DoctoPiConfigError(f"Unknown section in config '{section}'")

        # Add each key/value to the combined config
        for key, value in override_config.items(section):

            # Verify the key is valid
            if key not in [key for key, _ in combined_config.items(section)]:
                raise DoctoPiConfigError(f"Unknown key '{key}' in section '{section}'")

            combined_config.set(section, key, value)

    return combined_config


def ini_to_bool(ini_str: str) -> bool:
    """Convert ini value to python bool

    Args:
        ini_str (str): value from ini

    Raises:
        ValueError: provided value was not "yes" or "no"

    Returns:
        bool: yes or no
    """
    if ini_str.lower() == "yes":
        return True
    if ini_str.lower() == "no":
        return False

    raise ValueError

"""Tests for `doctopi` package."""
import os

import pytest

from doctopi.cli import cli, parse_settings, DoctoPiConfigError


class TestCLI:

    @pytest.mark.parametrize("ini", ["content_only", "default"])
    @pytest.mark.parametrize("raw_args,settings,expecteds", [
        (["markdown", "--no-constructors", "--toc-depth=5"], ["constructors", "toc_depth", "toc_title"], [False, 5, "Contents"]),
        (["markdown", "--author=jack-swiney", "--public-only"], ["author", "public_only", "methods"], ["jack-swiney", True, True]),
        (["markdown", "--no-methods", "--title=MyTitle"], ["methods", "title", "file_overview"], [False, "MyTitle", True]),
    ])
    def test_parse_settings_nominal(self, raw_args, settings, expecteds, ini):
        """Verify arguments are parsed correctly"""
        # Add ini to CLI args
        ini_path = os.path.join(os.path.dirname(__file__), f"examples/config/nominal/{ini}.ini")
        raw_args.append(f"--config={ini_path}")

        # Add required arg to CLI args
        raw_args.append("--input=test_file.py")

        # Parse CLI
        args = cli(raw_args)

        # Combine CLI with INI config
        args = parse_settings(args)

        for setting, expected in zip(settings, expecteds):
            assert getattr(args, setting) == expected

    @pytest.mark.parametrize("ini", ["extra_key", "extra_section"])
    def test_parse_settings_off_nominal(self, ini):
        """Verify when the ini is bad, an exception is raised"""
        # Add required args
        ini_path = os.path.join(os.path.dirname(__file__), f"examples/config/off_nominal/{ini}.ini")
        raw_args = ["markdown", f"--config={ini_path}", "--input=test_file.py"]

        # Verify an exception is raised when parsing the bad ini config file
        with pytest.raises(DoctoPiConfigError):
            # Combine CLI with INI config
            parse_settings(cli(raw_args))

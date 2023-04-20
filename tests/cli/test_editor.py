import os
from unittest.mock import patch, mock_open, call
from cli import editor
import pytest


@patch("os.path.isfile")
@patch("subprocess.run")
def test_open_config_calls_subprocess_run_with_correct_args(mock_run, mock_isfile):
    mock_isfile.return_value = True
    config = {"key1": "value1", "key2": "value2"}

    with patch("builtins.open", mock_open()) as mock_file:
        with patch("os.remove") as mock_file_remove:
            editor.open_config(config)

    mock_file.assert_has_calls(
        [
            call(".k4_config.tmp", "w"),
            call().__enter__(),
            call().write("key1=value1\n"),
            call().write("key2=value2\n"),
            call().__exit__(None, None, None),
        ]
    )

    mock_run.assert_called_once_with([os.environ.get("EDITOR", "vim"), ".k4_config.tmp", "+0"])
    mock_file_remove.assert_called_once_with(".k4_config.tmp")

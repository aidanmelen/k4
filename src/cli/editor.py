import os
import subprocess
from typing import Dict


def open_config(config: Dict[str, str], filepath: str = ".k4_config.tmp") -> Dict[str, str]:
    """
    Opens the configuration file in the system's terminal editor and returns the updated configuration.
    If the user exits the editor without saving any changes, the original configuration is returned.

    Args:
        config (Dict[str, str]): The configuration dictionary to be opened in the editor.
        filepath (str): The file path of the named temporary file to be created.

    Returns:
        Dict[str, str]: The updated configuration dictionary after the user has saved their changes.
    """
    # write topic config to a named temporary file
    with open(filepath, "w") as f:
        for key, value in sorted(config.items()):
            f.write(f"{key}={value}\n")

    # open the named temporary file in terminal editor
    editor = os.environ.get("EDITOR", "vim")

    if os.path.isfile(filepath):
        subprocess.run([editor, filepath, "+0"])
    else:
        # the named temporary file edit were not saved. return the original config
        return config

    # read the named temporary file edits
    new_config = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                new_config[key] = value

    # remove the temporary file
    os.remove(filepath)
    return new_config

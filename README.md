# Relic Tool - Core
[![PyPI](https://img.shields.io/pypi/v/relic-tool-core)](https://pypi.org/project/relic-tool-core/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/relic-tool-core)](https://www.python.org/downloads/)
[![PyPI - License](https://img.shields.io/pypi/l/relic-tool-core)](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/blob/main/LICENSE.txt)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pytest](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/actions/workflows/pytest.yml/badge.svg)](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/actions/workflows/pytest.yml)
[![Pylint](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/actions/workflows/pylint.yml/badge.svg)](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/actions/workflows/pylint.yml)
[![MyPy](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/actions/workflows/mypy.yml/badge.svg)](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/actions/workflows/mypy.yml)

### Description
The core library used by other Relic-Tool packages.

------

## Usage
### From the Command Line Interface
While the core library does not define any commands; it does define the command line. To discover installed commands, run the following.

```console
relic -h
```

### From Python Code
Commands can also be run directly from the library; To discover installed commands, run the following.
```python
from relic.core import CLI

exit_status = CLI.run_with('-h')
```
### Troubleshooting
#### No Commands are installed!
The core package does not define any CLI functionality itself.

If no options are specified, check to see if other Relic-Tool packages are installed that offer command line integration.

You can do this by running the following:
```console
python -m pip list
```
And looking for `relic-tool-...` in the command's output.

If you only see `relic-tool-core`, you need to install the desired Relic-Tool package the command belongs to.


------

# Installation (Pip)
### Installing from PyPI (Recommended)
```
pip install relic-tool-core
```
### Installing from GitHub
For more information, see [pip VCS support](https://pip.pypa.io/en/stable/topics/vcs-support/#git)
```
pip install git+https://github.com/MAK-Relic-Tool/Relic-Tool-Core
```

------

## [I Have an Issue / Found a Bug](https://github.com/MAK-Relic-Tool/Issue-Tracker/issues)
Click the link above, to visit the Issue Tracker

------

## Disclaimer
Not affiliated with Sega, Relic Entertainment, or THQ.

# Apologies Python Library

This is a Python library that implements a game similar to the Sorry
board game.  It includes a rudimentary way to play the game, intended
for use by developers and not by end users.

## Developer Notes

### Version and Dependencies

The current released version is tracked in [`version.py`](version.py).  Runtime
and test dependencies are tracked in [`dependencies.py`](dependencies.py).  If
you adjust the dependencies, re-build the virtual environment as described
below.

### Developer Script

The [`dev`](dev) script handles various different command-line tasks.

#### env - Virtual Environment

To set up the Python virtual environment for development purposes, run:

```shell
dev env
```

This installs a Python 3.7 virtual environment and all of the required
dependencies.  Activate the virtual environment like this:

```shell
source .python/bin/activate
```

If you change any of the runtime or test dependencies, then rebuild the
virtual environment:

```shell
dev env rebuild
```

That will remove the existing environment and rebuild it from scratch.

#### test - Run unit tests

The unit test suite is written using PyTest.  To run the test suite,
use:

```shell
dev test
```

Any arguments after `test` are passed to the `pytest` executable.

#### pylint - Run the Pylint style checker

Before committing code, it must be lint-clean.  To check the code,
use:

```shell
dev pylint
```

#### render - Visualizing the state of a game

Game state is maintained in the `Game` class.  However, it's hard to look at a
`Game` object and really understand the game.  The `render` module renders game
state to the terminal, so you can see the state of the game board.  

The `render` script dumps out an empty board, which is stored for reference in
[`doc/rendered.txt`](doc/rendered.txt).  Rebuild that rendered board like this:

```shell
dev render
```

If you want, you can adjust the `render` script to change the game state.  This
script is not distributed.

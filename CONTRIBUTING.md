# Contributing

## Development setup

```bash
python -m pip install "OctoPrint==1.11.8"
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

## Tests

```bash
python -m pytest
```

The tests use a fake settings object, so no running OctoPrint instance is
required. OctoPrint itself only has to be importable.

## Code style

- Follow the existing style: tabs for indentation, `from __future__` imports
  where the OctoPrint plugin template uses them.
- Keep the gcode rewriting in `octoprint_swapxyz/__init__.py`.
- Support Python 3.7 and newer; no new runtime dependencies without a good
  reason.

## Translations

```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
pybabel compile -d octoprint_swapxyz/translations
```

## Pull requests

- One topic per pull request.
- Add an entry to `CHANGELOG.md`.
- CI (tests, lint, CodeQL) has to pass.

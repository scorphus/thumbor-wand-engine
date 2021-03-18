# thumbor-wand-engine

[![Build Status][build-badge]][build-link] [![Coverage Status][codecov-badge]][codecov-link] [![Code Quality][codacy-badge]][codacy-link] [![Maintainability][codeclimate-badge]][codeclimate-link]

thumbor-wand-engine is an [ImageMagick][] imaging engine for [thumbor][].

## Installation

You can install the package from [PyPI][] with `pip`:

    $ pip install thumbor-wand-engine

### Requirements

-   Python 3.6 or higher
-   MagickWand library
    -   `libmagickwand-dev` for APT on Debian/Ubuntu
    -   `ImageMagick-devel` for Yum on CentOS
    -   `imagemagick` for MacPorts/Homebrew on Mac

## Why another engine

Thumbor ships with a builtin engine, however with thumbor-wand-engine you get:

-   Smaller images ⏳ 💲
-   Better image quality 🤩
-   Support to animated WEBP ⏳ 💲
-   Support to AVIF and HEIC 🖼
-   IPTC/XMP data preservation 📜
-   Smoother blur ✨
-   Sharper resizing 📐
-   Better watermarking 🏷

## Usage

To use this engine with thumbor, define `thumbor_wand_engine` as the imaging
engine in `thumbor.conf`:

```python
# imaging engine to use to process images
ENGINE = "thumbor_wand_engine"
```

## Development

### Requirements

-   Python 3.6 or higher
-   An activated virtual environment
-   [pre-commit][]

### Create a development environment

1.  Start by creating a new Python virtual environment with the tool of your
    choice (we recommend [pyenv][])

2.  Install pre-commit (we recommend [installing][pre-commit-install] it not as
    part of the virtual environment — use your system's package manager)

3.  Install wand-engine in editable mode with all required dependencies:

        $ make setup

### Run tests

Once you have a working development environment:

1.  Code!

        🤓 🤔 💡 ⚡️ 🖼

2.  Run tests

        $ make test

3.  Check code coverage

        $ make coverage-html
        $ open htmlcov/index.html

4.  Lint the code:

        $ make lint

5.  Repeat!

Have fun!

## License

Code in this repository is distributed under the terms of the MIT License.

See [LICENSE][] for details.

[build-badge]: https://github.com/scorphus/thumbor-wand-engine/workflows/build/badge.svg
[build-link]: https://github.com/scorphus/thumbor-wand-engine/actions/workflows/build.yml
[codacy-badge]: https://app.codacy.com/project/badge/Grade/a09b9a77c55749dca1e9dde3edb7f808
[codacy-link]: https://www.codacy.com/gh/scorphus/thumbor-wand-engine/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=scorphus/thumbor-wand-engine&amp;utm_campaign=Badge_Grade
[codeclimate-badge]: https://api.codeclimate.com/v1/badges/1a6687203d55505d015d/maintainability
[codeclimate-link]: https://codeclimate.com/github/scorphus/thumbor-wand-engine/maintainability
[codecov-badge]: https://codecov.io/gh/scorphus/thumbor-wand-engine/branch/main/graph/badge.svg?token=DsYnnMtO6b
[codecov-link]: https://codecov.io/gh/scorphus/thumbor-wand-engine
[imagemagick]: https://imagemagick.org
[license]: LICENSE
[pre-commit-install]: https://pre-commit.com/#install
[pre-commit]: https://pre-commit.com
[pyenv]: https://github.com/pyenv/pyenv
[pypi]: https://pypi.python.org/pypi/wand_engine
[thumbor]: http://thumbor.org

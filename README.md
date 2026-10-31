-----

<div align="center">

[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)
[![Poetry](https://img.shields.io/badge/packaging-poetry-cyan.svg)](https://python-poetry.org/)
[![GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

</div>

<hr>

# Alpha TradingBot

A Streamlit application for exploring market data, building trading strategies, running backtests, and optimizing strategy parameters.

[WebApp Link](https://alpha-tradingbot.streamlit.app/)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Application workflow](#application-workflow)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before setting up the project, ensure that you have the following prerequisites installed on your machine:

- Python (version 3.10.10):
  (https://www.python.org/downloads/)
- Poetry (version 1.4.0):
  (https://python-poetry.org/docs/#installation)

## Installation

1. Clone the project repository:

```
git clone https://github.com/ataturhan21/Alpha-Trading-Bot.git
```

2. Navigate to the project directory:

```
cd Alpha-Trading-Bot
```

3. Install project dependencies using Poetry:

```
poetry install --no-root
```

This installs the dependencies from `pyproject.toml` and `poetry.lock` without trying to package the Streamlit application.

## Usage

1. Activate the virtual environment created by Poetry:

```
poetry shell
```

2. Run the project:

```
streamlit run "app/🤖Welcome.py"
```

On Windows, you can also use `start.bat`.


## Application workflow

Run commands from the repository root so that local data, styles, and images resolve correctly.

| Module | Purpose | Implementation |
| --- | --- | --- |
| Data | Retrieve and inspect price data | [Data preparation](app/create_data.py) |
| Strategy | Build trading signals | [Strategy functions](app/create_strategy.py) |
| Backtest | Evaluate a strategy on historical data | [Backtesting](app/create_backtest.py) |
| Optimization | Compare strategy parameters | [Optimization](app/optimization.py) |

The Streamlit pages are in [`app/pages/`](app/pages/); the ticker workbook is in [`data/Tickers/`](data/Tickers/). Market-data retrieval requires network access. Start with a small dataset and inspect a strategy's trades before increasing the optimization search.

The repository preserves its original Python and dependency constraints. Historical backtests and parameter optimization do not establish out-of-sample performance; evaluate a separate period when comparing strategies.

## Contributing

If you would like to contribute to this project, follow the guidelines below:

1. Fork the repository and clone it locally.

2. Create a new branch for your feature or bug fix:
   ```
   git checkout -b feature/your-feature
   ```

3. Make your changes and commit them with descriptive commit messages.

4. Push your changes to your forked repository:
   ```
   git push origin feature/your-feature
   ```

5. Open a pull request in the original repository, describing your changes in detail.


## License

GPL v3

---

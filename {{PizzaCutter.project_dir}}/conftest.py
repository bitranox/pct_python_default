import pytest
from typing import List

collect_ignore: List[str] = {{PizzaCutter.pytest.collect_ignore}}


def pytest_load_initial_conftests(early_config: pytest.Config, parser: pytest.Parser, args: List[str]) -> None:
    # PizzaCutter Template can add here additional pytest args
    additional_pytest_args: List[str] = {{PizzaCutter.pytest.additional_args}}
    args[:] = list(set(args + additional_pytest_args))

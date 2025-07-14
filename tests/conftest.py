import pytest
from src.whist.game import WhistGame

@pytest.fixture
def whist():
    whist = WhistGame()
    return whist
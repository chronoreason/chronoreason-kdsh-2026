"""Shared test fixtures and configuration."""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# Fixtures for sample data
import pytest

@pytest.fixture
def sample_text():
    """Sample text for chunking tests."""
    return """
    Lord Edward Glenarvan was born into an aristocratic family with substantial wealth and influence.
    From his earliest childhood, he was groomed to value caution and political pragmatism.
    He developed a profound fear of maritime travel during a turbulent voyage as a boy.
    Throughout his formative years, he was taught that personal intervention in rescue missions was reckless.
    By adulthood, he had consolidated these teachings into a personal philosophy of safety first.
    """ * 5  # Repeat to create longer text


@pytest.fixture
def empty_text():
    """Empty text for edge case tests."""
    return ""


@pytest.fixture
def sample_backstory():
    """Sample backstory with claims."""
    return """
    Glenarvan was a cautious man who feared the sea.
    He believed government should handle all crises.
    He preferred comfort and safety over adventure.
    He never took personal risks for others.
    """


@pytest.fixture
def contradictory_backstory():
    """Backstory that contradicts another."""
    return """
    Glenarvan was a brave and decisive leader.
    He personally led dangerous rescue expeditions.
    He believed in immediate action during emergencies.
    He was willing to risk his life for others.
    """


@pytest.fixture
def validations_mixed():
    """Mixed validation results."""
    return ["support", "support", "contradict", "neutral", "support"]


@pytest.fixture
def validations_all_support():
    """All support validations."""
    return ["support", "support", "support"]


@pytest.fixture
def validations_all_contradict():
    """All contradict validations."""
    return ["contradict", "contradict", "contradict"]


@pytest.fixture
def sample_timeline():
    """Sample timeline for visualization."""
    return [
        {"event": "The search for Captain Grant begins", "time": "event_0", "effect": "under_review"},
        {"event": "The ship sets sail across the ocean", "time": "event_1", "effect": "under_review"},
        {"event": "Crew encounters storms and hardship", "time": "event_2", "effect": "under_review"},
        {"event": "Captain Grant is discovered on an island", "time": "event_3", "effect": "under_review"},
    ]


@pytest.fixture
def empty_timeline():
    """Empty timeline."""
    return []


@pytest.fixture
def short_timeline():
    """Timeline with only one event."""
    return [
        {"event": "First event", "time": "event_0", "effect": "unknown"}
    ]

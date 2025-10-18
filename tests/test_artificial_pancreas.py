
import pytest
from main.artificial_pancreas import (
    ArtificialPancreasSystem as ArPS,
    ActionFactory,
    DeliverInsulin,
    WarnLowGlucose,
    Maintain
)


# ---------- FIXTURE ----------
@pytest.fixture
def system():
    """Returns a fresh ArtificialPancreasSystem instance for each test."""
    return ArPS()


# ---------- GROUP 1: GLUCOSE REGULATION ----------
class TestGlucoseRegulation:

    def test_glucose_increases_after_meal(self, system):
        start = system.glucose_level
        end = system.meal(10)
        assert end > start

    def test_glucose_never_below_min(self, system):
        # Test 1: Initialize with low glucose
        low_init = ArPS(glucose_level=5.0)
        assert low_init.glucose_level >= low_init.GLUCOSE_MIN_RESET

        # Test 2: Extreme exercise should not go below minimum
        system.glucose_level = 80.0
        system.exercise(100000)
        assert system.glucose_level >= system.GLUCOSE_MIN_RESET

    def test_glucose_decreases_after_exercise(self, system):
        start = system.glucose_level
        end = system.exercise(100)
        assert end < start


# ---------- GROUP 2: PREDICTIVE ACTIONS ----------
class TestPredictiveActions:

    def test_insulin_delivery_action(self, system):
        system.glucose_level = 180.0
        action, level = system.predict_action()
        assert action == "deliver_insulin"
        assert 100 <= level < 180.0

    def test_warn_low_glucose_action(self, system):
        system.glucose_level = 65.0
        action, level = system.predict_action()
        assert action == "warn_low_glucose"
        assert level == 65.0

    def test_maintain_action(self, system):
        system.glucose_level = 100.0
        action, level = system.predict_action()
        assert action == "maintain"
        assert level == 100.0


# ---------- GROUP 3: ERROR HANDLING ----------
class TestErrorHandling:

    def test_negative_carbs_input(self, system):
        with pytest.raises(ValueError):
            system.meal(-10)

    def test_negative_exercise_input(self, system):
        with pytest.raises(ValueError):
            system.exercise(-15)

    def test_negative_glucose_initialization(self):
        with pytest.raises(ValueError):
            ArPS(glucose_level=-50.0)

    def test_non_numerical_glucose_initialization(self):
        with pytest.raises(TypeError):
            ArPS(glucose_level="high")

    def test_non_numerical_meal_input(self, system):
        with pytest.raises(TypeError):
            system.meal("twenty")

    def test_non_numerical_exercise_input(self, system):
        with pytest.raises(TypeError):
            system.exercise("thirty")

    def test_total_insulin_delivered(self, system):
        system.glucose_level = 200.0
        initial_insulin = system.total_insulin_delivered
        system.predict_action()
        assert system.total_insulin_delivered > initial_insulin

    def test_action_factory(self):
        deliver_insulin_action = ActionFactory.create("deliver_insulin")
        assert isinstance(deliver_insulin_action, DeliverInsulin)

        warn_low_glucose_action = ActionFactory.create("warn_low_glucose")
        assert isinstance(warn_low_glucose_action, WarnLowGlucose)

        maintain_action = ActionFactory.create("maintain")
        assert isinstance(maintain_action, Maintain)

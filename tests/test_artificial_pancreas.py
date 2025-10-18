import pytest
from main.artificial_pancreas import ArtificialPancreasSystem as ArPS, ActionFactory, DeliverInsulin, WarnLowGlucose, Maintain

class TestGlucoseRegulation:
    """Group of tests for core glucose regulation methods."""

    def setup_method(self):
        """Run before each test in this class."""
        self.system = ArPS()

    def test_glucose_increases_after_meal(self):
        start = self.system.glucose_level
        end = self.system.meal(40)
        assert end > start

    def test_glucose_decreases_after_exercise(self):
        start = self.system.glucose_level
        end = self.system.exercise(30)
        assert end < start

    def test_glucose_never_below_min(self):
            min_value = self.system.GLUCOSE_MIN_RESET
            by_init = ArPS(glucose_level=5.0)              
            by_exercise = self.system.exercise(100000)          
            assert min_value == by_exercise
            assert min_value == by_init.glucose_level
            
    
class TestPredictiveActions:
    """Group of tests for predictive action methods."""
    
    def setup_method(self):
        """Run before each test in this class."""
        self.system = ArPS()
        
    def test_insulin_delivery_action(self):
        self.system.glucose_level = 180.0                # Set high glucose level to trigger insulin delivery
        action, level = self.system.predict_action()
        assert action == "deliver_insulin"
        assert self.system.healthy_lower_bound < level < self.system.healthy_upper_bound                             # Glucose level should decrease after insulin delivery
        
    def test_warn_low_glucose_action(self):
        self.system.glucose_level = 65.0                 # Set low glucose level to trigger warning
        action, level = self.system.predict_action()
        assert action == "warn_low_glucose"
        assert level == 65.0                             # Glucose level should remain the same
        
    def test_maintain_action(self):
        self.system.glucose_level = 100.0              # Set normal glucose level to trigger maintain action
        action, level = self.system.predict_action()
        assert action == "maintain"
        assert level == 100.0                          # Glucose level should remain the same


class TestErrorHandling:    
    
    def setup_method(self):
        """Run before each test in this class."""
        self.system = ArPS()
        
    def test_negative_carbs_input(self):
        with pytest.raises(ValueError):
            self.system.meal(-10)

    def test_negative_exercise_input(self):
        with pytest.raises(ValueError):
            self.system.exercise(-15)    

    def test_negative_glucose_initialization(self):
        with pytest.raises(ValueError):
            self.system = ArPS(glucose_level=-50.0)
            
    def test_non_numerical_glucose_initialization(self):
        with pytest.raises(TypeError):
            self.system(glucose_level="high")
            
    def test_non_numerical_meal_input(self):
        with pytest.raises(TypeError):
            self.system.meal("twenty")
            
    def test_non_numerical_exercise_input(self):
        with pytest.raises(TypeError):
            self.system.exercise("thirty")

    def test_total_insulin_delivered_updates(self):
        self.system.glucose_level = 200.0                    # High glucose level to trigger insulin delivery
        initial_insulin_delivered = self.system.total_insulin_delivered
        self.system.predict_action()
        assert self.system.total_insulin_delivered > initial_insulin_delivered
            

class TestActionFactory:
    """Group of tests for ActionFactory to see that the factory calls the right test."""
     
    def test_deliver_insulin(self):
        deliver_insulin_action = ActionFactory.create("deliver_insulin")
        assert isinstance(deliver_insulin_action, DeliverInsulin)
    
    def test_warn_low_glucose_action(self):
        warn_low_glucose_action = ActionFactory.create("warn_low_glucose")
        assert isinstance(warn_low_glucose_action, WarnLowGlucose)
    
    def test_maintain_action(self):
        maintain_action = ActionFactory.create("maintain")
        assert isinstance(maintain_action, Maintain)

    def test_maintain_action(self):
        with pytest.raises(KeyError):
            ActionFactory.create("call_the_doctor")
        

   

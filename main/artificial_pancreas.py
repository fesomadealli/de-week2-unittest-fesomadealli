
from abc import ABC, abstractmethod

class ArtificialPancreasSystem:
        """
        A  simplified  model  for  data-driven  glucose  regulation.
        """
             
        GLUCOSE_PER_CARB  =  0.5        #  fixed  increase  per  carb  unit
        GLUCOSE_BURN_PER_MIN  =  0.3    #  fixed  decrease  per  minute  of  exercise
        DEFAULT_GLUCOSE_LVL = 100.0
        GLUCOSE_MIN_RESET = 50          # incase threshold changes later, initialize here for all instances
        action = None
        
        def  __init__(self,  
                      glucose_level:float=DEFAULT_GLUCOSE_LVL,       # initialized as target_glucose level assuming equal balanced reading for all patients
                      insulin_sensitivity:float=1.0,  # insulin sensitivity default
                      target_glucose:float=100.0,     # healthy reading for glucose_level
                      tolerance:float=10.0):          # upper and lower tolerance rnages estimator for patient's glucose level
                
                self.glucose_level = glucose_level or self.GLUCOSE_MIN_RESET
                
                if not isinstance(self.glucose_level, (int,float)):
                        raise TypeError("Please use the Numerical Keys")
                elif self.glucose_level < 0:
                        raise ValueError("Glucose level cannot be negative.")
                elif self.glucose_level < self.GLUCOSE_MIN_RESET:
                        self.glucose_level = self.GLUCOSE_MIN_RESET
                else:
                        self.glucose_level = glucose_level or self.GLUCOSE_MIN_RESET        
                             
                self.insulin_sensitivity = insulin_sensitivity
                self.target_glucose = target_glucose
                self.tolerance = tolerance 
                self.healthy_lower_bound =  self.target_glucose - self.tolerance
                self.healthy_upper_bound =  self.target_glucose + self.tolerance
                self.total_insulin_delivered = 0.0

        def  meal(self,  carbs:  float):
                """Simulate  a  meal  event."""
                if not isinstance(carbs, (int,float)):
                        raise TypeError("Please use the Numerical Keys")
                
                if carbs < 0:
                        raise ValueError("Carbs intake cannot be negative.")
                else:                        
                        self.glucose_level += round(carbs * self.GLUCOSE_PER_CARB, 2)
                        print(f"Meal Carbs Raised Patient's Glucose Level to {self.glucose_level:.2f}")
                        return self.glucose_level

        def  exercise(self,  duration:  float):
                """Simulate  physical  activity  (input  feature:  duration)."""
                if not isinstance(duration, (int,float)):
                        raise TypeError("Please use the Numerical Keys")
                
                if duration < 0:
                        raise ValueError("Exercise duration cannot be negative.")
                else:
                        self.glucose_level -= round(duration * self.GLUCOSE_BURN_PER_MIN, 2)
                        
                        if self.glucose_level < self.GLUCOSE_MIN_RESET:
                                self.glucose_level = self.GLUCOSE_MIN_RESET
                        
                print(f"Exercising for {duration} Minutes Reduced Patient's Glucose Level to {self.glucose_level:.2f}")
                return self.glucose_level
        
        @property
        def doc_action(self):
                return self.action
        
        def  predict_action(self):
                """
                Predict  and  apply  an  appropriate  system  action.
                Acts  like  a  decision  function  in  a  model.
                
                USAGE:
                This is the system's decision-making part:
                If glucose is too high (above target_glucose + tolerance):
                       - The system should "deliver_insulin".
                       - Insulin dosage is based on how much above the target the glucose is.
                       - After giving insulin, subtract the dose from the current glucose level.
                       
                If glucose is too low (below target_glucose - tolerance):
                       - The system should "warn_low_glucose".
                
                If glucose is within the target range:
                       - "maintain" (do nothing).
                
                OUTPUT:
                System returns both the action name ("deliver_insulin", "warn_low_glucose", "maintain") and the new glucose level.
                """
                       
                if self.glucose_level < self.healthy_lower_bound:
                       self.action = "warn_low_glucose"
                       
                elif self.glucose_level > self.healthy_upper_bound:
                       self.action = "deliver_insulin"
                else:
                       self.action = "maintain"
                       
                pancreas_doc = ActionFactory.create(self.action)
                return pancreas_doc.take_action(self)


@abstractmethod                
class Action(ABC):
        """Compulsory method all Design Factory classes must implement"""
        def take_action(self, doc: ArtificialPancreasSystem):
                pass
         
class DeliverInsulin(Action):
    def take_action(self, doc: ArtificialPancreasSystem):
        dosage = round((doc.glucose_level - doc.target_glucose) * doc.insulin_sensitivity, 2)
        doc.glucose_level -= dosage
        doc.total_insulin_delivered += dosage
        print(f"Action: deliver_insulin | Dose: {dosage:.2f} | New Glucose level: {doc.glucose_level:.2f}")
        return doc.doc_action, doc.glucose_level

class WarnLowGlucose(Action):
    def take_action(self, doc: ArtificialPancreasSystem):
        print(f"Action: warn_low_glucose | Low Glucose level : {doc.glucose_level:.2f}")
        return doc.doc_action, doc.glucose_level

class Maintain(Action):
    def take_action(self, doc: ArtificialPancreasSystem):
        print(f"Action: maintain | Glucose stable at {doc.glucose_level:.2f}")
        return doc.doc_action, doc.glucose_level

class ActionFactory:
    """Factory that returns the correct action handler."""
    @staticmethod
    def create(action: str) -> Action:
        actions = {
            "deliver_insulin": DeliverInsulin(),
            "warn_low_glucose": WarnLowGlucose(),
            "maintain": Maintain()
        }
        if action not in actions:
            raise KeyError(f"Action '{action}' is not recognized, try either of these: {list(actions.keys())}.")
        return actions[action]
       
 
if __name__ == "__main__":
        
    system = ArtificialPancreasSystem()
    print("\nWelcome to glucoseDoc Application!\n")

    while True:
        try:
            # Meal input
            carbs = float(input("Enter carbs consumed (grams): "))
            system.meal(carbs)

            # Exercise input
            minutes = float(input("Enter exercise duration (minutes): "))
            system.exercise(minutes)

            # Predict and print action
            action, level = system.predict_action()
            print(f"Treatment: {action}, New Glucose Level: {level:.2f}")

        except ValueError as e:
            print(f"ValueError: {e}")
            continue
        except TypeError as e:
            print(f"TypeError: {e}")
            continue
        except KeyError as e:
            print(f"KeyError: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

        # Ask if user wants to exit
        update_run = input("\nDo you want to close glucoseDoc? (y/n): ").strip().lower()
        if update_run == "y":
            print("\nExiting glucoseDoc. Goodbye!\n")
            break
        elif update_run != "n":
            print("Invalid input. Please type 'y' or 'n'.")

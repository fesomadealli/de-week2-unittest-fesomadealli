# Artificial Pancreas System - Glucose Regulation Simulator

> **Bringing Data-Driven Intelligence to Diabetes Management**

## 🌟 Project Overview

**It’s 7:00 a.m.** Somewhere in the world, a person with diabetes scans their glucose monitor before breakfast. The numbers flicker on the screen, slightly above normal. They pause, thinking: *"Should I eat now? Should I wait? Should I take more insulin?"*

This moment of quiet uncertainty happens **every single day** for millions of people. Each meal, each workout, each night's sleep brings a new equation to solve. **Too much insulin**, and blood sugar could crash dangerously low. **Too little**, and it could soar, causing fatigue, blurred vision, or worse.

This project represents a step toward easing that burden through smart algorithms and data-driven insights.

## 🎯 Learning Objectives

- **Practice Object-Oriented Programming (OOP)** to structure real-world data logic
- **Understand how data inputs** (meals, exercise) affect system states
- **Apply algorithmic reasoning** to maintain values within safe boundaries
- **Write comprehensive unit tests** using pytest to ensure model stability

## How to Run

### Running the Application
To start the **glucoseDoc** artificial pancreas system from the root directory (**pancreas-app**):

```
poetry run python main/artificial_pancreas.py
```

This will launch the interactive application where you can:
- Enter carbs consumed (grams)
- Enter exercise duration (minutes) 
- See the system's recommended treatment action
- Monitor glucose level changes

### Running Tests
To execute the test suite from the root directory (**pancreas-app**):

```
poetry run pytest
```

### Prerequisites
- Python 3.7+
- Poetry package manager
- Dependencies installed via `poetry install`

## 🏗️ System Architecture

### Core Class: `ArtificialPancreasSystem`

A simplified model for data-driven glucose regulation that simulates basic glucose control mechanisms.

#### Key Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `glucose_level` | Current glucose reading | Required |
| `insulin_sensitivity` | How strongly insulin affects glucose drop | 1.0 |
| `target_glucose` | Ideal glucose level to maintain | 100 |
| `tolerance` | Acceptable range around target | 10 |

#### Core Methods

**`meal(carbs: float)`**
- Increases glucose based on carb intake
- Formula: `glucose_level += carbs * GLUCOSE_PER_CARB`

**`exercise(duration: float)`**
- Decreases glucose based on exercise duration
- Formula: `glucose_level -= duration * GLUCOSE_BURN_PER_MIN`
- **Safety Feature**: Glucose never drops below minimum threshold (50)

**`predict_action()`**
- Decision engine that returns appropriate actions:
  - `"deliver_insulin"` when glucose is too high
  - `"warn_low_glucose"` when glucose is too low  
  - `"maintain"` when within target range

## 🧪 Testing Strategy

### Key Testing Principles
- **Boundary Testing**: Verify glucose never falls below safe minimum
- **State Consistency**: Ensure sequential operations maintain correct state
- **Edge Cases**: Test with extreme values and invalid inputs
- **Behavior Validation**: Confirm correct actions for different glucose levels
---

### Test Summary for `test_artificial_pancreas.py`

### **1️⃣ TestGlucoseRegulation**

**Total:** 3 tests
**Tests:**

1. `test_glucose_increases_after_meal`
2. `test_glucose_decreases_after_exercise`
3. `test_glucose_never_below_min`

---

### **2️⃣ TestPredictiveActions**

**Total:** 3 tests
**Tests:**

1. `test_insulin_delivery_action`
2. `test_warn_low_glucose_action`
3. `test_maintain_action`

---

### **3️⃣ TestErrorHandling**

**Total:** 7 tests
**Tests:**

1. `test_negative_carbs_input`
2. `test_negative_exercise_input`
3. `test_negative_glucose_initialization`
4. `test_non_numerical_glucose_initialization`
5. `test_non_numerical_meal_input`
6. `test_non_numerical_exercise_input`
7. `test_total_insulin_delivered_updates`

---

### **4️⃣ TestActionFactory**

**Total:** 3 tests (one duplicate name — only the *last one* runs)
**Tests:**

1. `test_deliver_insulin`
2. `test_warn_low_glucose_action`
3. `test_maintain_action` *(KeyError test — last definition overwrites the earlier one)*

---

### ✅ **Overall Total**

**16 tests executed**

---


## 📁 Project Structure

```
main/
    __init__.py
    artificial_pancreas.py        # Core implementation
tests/
    __init__.py
    test_artificial_pancreas.py   # Comprehensive test suite
README.md                         # This file
requirements.txt                  # Dependencies
.gitignore                       # Git configuration
```

## 🚀 Getting Started

### Installation
```bash
git clone https://github.com/<user>/de-week2-unittest-<yourname>
cd de-week2-unittest-<yourname>
pip install -r requirements.txt
```

### Running Tests
```bash
pytest tests/ -v                 # Run all tests
pytest tests/ -k "test_glucose"  # Run specific tests
pytest --cov=main tests/         # With coverage reporting
```

### Basic Usage
```python
from main.artificial_pancreas import ArtificialPancreasSystem

# Initialize system
controller = ArtificialPancreasSystem(glucose_level=100)

# Simulate daily activities
controller.meal(40)              # Breakfast
controller.exercise(30)          # Morning workout
action, level = controller.predict_action()

print(f"Action: {action}, Glucose: {level}")
```

## 🔬 Example Scenarios

### Scenario 1: Post-Meal Management
```python
system = ArtificialPancreasSystem(glucose_level=90)
system.meal(60)  # Large meal
action, level = system.predict_action()
# Expected: "deliver_insulin" with elevated glucose
```

### Scenario 2: Exercise Impact
```python
system = ArtificialPancreasSystem(glucose_level=110)
system.exercise(45)  # Intense workout
action, level = system.predict_action()  
# Expected: "maintain" or "warn_low_glucose" depending on result
```

### Scenario 3: Boundary Protection
```python
system = ArtificialPancreasSystem(glucose_level=55)
system.exercise(120)  # Extreme exercise
# Glucose will decrease but never drop below minimum safe level (50)
```

## 📊 Constants & Formulas

| Constant | Value | Description |
|----------|-------|-------------|
| `GLUCOSE_PER_CARB` | 0.5 | Glucose increase per carb unit |
| `GLUCOSE_BURN_PER_MIN` | 0.3 | Glucose decrease per exercise minute |
| `GLUCOSE_MIN_RESET` | 50.0 | Absolute minimum glucose level |

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/week2-unittest`
3. **Commit** changes: `git commit -m "Add meaningful message"`
4. **Push** to branch: `git push origin feature/week2-unittest`
5. **Open** a Pull Request

## 📋 Submission Checklist

- [ ] Complete `ArtificialPancreasSystem` implementation
- [ ] Write comprehensive pytest test suite
- [ ] All core test cases passing
- [ ] Proper error handling for invalid inputs
- [ ] Clear documentation and code comments
- [ ] Repository follows required structure
- [ ] README.md with usage examples

## 🎓 Learning Outcomes

After completing this project, I understood:
- How to model real-world biological processes in code
- The importance of boundary conditions in healthcare applications
- Writing tests that validate both expected behavior and safety constraints
- Building systems that maintain state across multiple operations

## ⚠️ Important Notes

This is a **simplified educational model** and should not be used for actual medical decisions. Real artificial pancreas systems involve complex algorithms, continuous monitoring, and medical supervision.

---

## 📞 Support

For questions or issues, please open an issue in the GitHub repository.

---

**Built with care for better healthcare technology** 💙
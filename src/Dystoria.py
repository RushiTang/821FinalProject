"""This is our Dytoria Game."""

import random
from typing import Dict, List


class NamedObject:
    """Base class for any object with a name."""

    def __init__(self, name: str):
        """Initialize with a name."""
        self.name = name

    def get_name(self) -> str:
        """Return the object's name."""
        return self.name


class Component:
    """Base class for components that can be attached to objects."""

    def update(self, owner: "NamedObject") -> None:
        """Update the component based on the owner's status."""
        pass


class HealthComponent(Component):
    """Component that manages health-related attributes and methods."""

    def __init__(self, health: int):
        """Initialize with health."""
        self.health = health

    def reduce_health(self, amount: int) -> None:
        """Decrease health by a specified amount."""
        self.health = max(0, self.health - amount)


class StealthComponent(Component):
    """Component that manages visibility-related attributes and methods."""

    def __init__(self, visibility: int):
        """Initialize with visibility level."""
        self.visibility = visibility

    def modify_visibility(self, amount: int) -> None:
        """Modify visibility by a specified amount."""
        self.visibility = max(0, self.visibility + amount)


class ArcaneWeapon(NamedObject):
    """Class representing a magical weapon with damage range."""

    def __init__(self, name: str, min_dmg: int, max_dmg: int):
        """Initialize with name and damage range."""
        super().__init__(name)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def damage(self) -> int:
        """Calculate random damage within the range."""
        return random.randint(self.min_dmg, self.max_dmg)


class MysticQuiver(NamedObject):
    """Class representing a quiver that can hold arrows."""

    def __init__(self, name: str, qty: int):
        """Initialize with name and quantity of arrows."""
        super().__init__(name)
        self.qty = qty

    def get_quantity(self) -> int:
        """Return the quantity of arrows."""
        return self.qty

    def remove_all(self) -> int:
        """Remove all arrows from the quiver."""
        self.qty = 0
        return self.qty


class SpellcasterBow(ArcaneWeapon):
    """Class representing a bow that can use special arrows."""

    def __init__(self, name: str, min_dmg: int, max_dmg: int):
        """Initialize with name and damage range, set initial shot count."""
        super().__init__(name, min_dmg, max_dmg)
        self.shots = 0

    def load(self, ammo: "MysticQuiver") -> None:
        """Load the bow with arrows from a given quiver."""
        if ammo.get_name() == self.get_name():
            self.shots += ammo.get_quantity()
            ammo.remove_all()

    def damage(self) -> int:
        """Calculate damage if there are shots available."""
        if self.shots > 0:
            self.shots -= 1
            return super().damage()
        return 0


class Sanctuary(NamedObject):
    """Class representing a sanctuary where mages can gather."""

    def __init__(self, name: str):
        """Initialize with a name."""
        super().__init__(name)
        self.mages: List["Mage"] = []

    def add_mage(self, mage: "Mage") -> None:
        """Add a mage to the sanctuary."""
        self.mages.append(mage)


class Mage(NamedObject):
    """Class representing a mage with health and stealth components."""

    def __init__(self, name: str):
        """Initialize with a name and default components."""
        super().__init__(name)
        self.components: Dict[str, Component] = {
            "health": HealthComponent(100),
            "stealth": StealthComponent(50),
        }
        self.inventory: List[NamedObject] = []

    def perform_action(self) -> None:
        """Print the current action being taken by the mage."""
        health_component = self.components.get("health")
        if isinstance(health_component, HealthComponent):
            print(
                f"{self.name} is taking action with current health: "
                f"{health_component.health}"
            )
        else:
            print(f"No health component found for {self.name}.")


class ArcaneChampion(Mage):
    """A specialized mage class with enhanced abilities & hunger management."""

    def __init__(self, name: str, health: int):
        """Initialize with a name and specific health."""
        super().__init__(name)
        self.components["health"] = HealthComponent(health)
        self.components["stealth"] = StealthComponent(50)
        self.hunger = 100

    def reduce_hunger(self, amount: int) -> None:
        """Reduce hunger by a specified amount."""
        self.hunger = max(0, self.hunger - amount)

    def increase_hunger(self, amount: int) -> None:
        """Increase hunger by a specified amount."""
        self.hunger = min(100, self.hunger + amount)

    def eat(self, food: NamedObject) -> None:
        """Consume food to reduce hunger, if available in the inventory."""
        if food in self.inventory:
            # Assuming a method get_food_value exists in the food class
            if hasattr(food, "get_food_value"):
                self.reduce_hunger(food.get_food_value())
                self.inventory.remove(food)
            else:
                print(f"{food.get_name()} does not have food value.")
        else:
            print(f"{food.get_name()} is not in inventory.")

    def attack(self, target: "Mage", weapon: ArcaneWeapon) -> None:
        """Attack a target with a weapon if conditions are met."""
        if weapon in self.inventory and isinstance(weapon, ArcaneWeapon):
            stealth_component = self.components.get("stealth")
            if (
                isinstance(stealth_component, StealthComponent)
                and stealth_component.visibility < 30
            ):
                damage = weapon.damage()
                health_component = target.components.get("health")
                if isinstance(health_component, HealthComponent):
                    health_component.reduce_health(damage)
                    if health_component.health <= 0:
                        print(f"{target.get_name()} has been defeated.")
                else:
                    print(
                        f"No health component found for {target.get_name()}."
                    )
            else:
                print("Too visible to attack stealthily.")
        else:
            print(f"{weapon.get_name()} not found in inventory.")

"""This is our Dytoria Game."""

import csv
import random
import sys
from typing import Any, Dict, List, Optional


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


class SpellcasterBow(NamedObject):
    """Class representing a magical bow use arrows with damage range."""

    def __init__(self, name: str, min_dmg: int, max_dmg: int):
        """Initialize with name, damage range, and set initial shot count."""
        super().__init__(name)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.shots = 8

    def load(self, ammo: "MysticQuiver") -> None:
        """Load the bow with arrows from a given quiver."""
        self.shots = ammo.get_quantity()
        ammo.remove_all()

    def damage(self) -> int:
        """Calculate damage if there are shots available, else return zero."""
        if self.shots > 0:
            self.shots -= 1
            return random.randint(self.min_dmg, self.max_dmg)
        return 0


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


class Sanctuary(NamedObject):
    """Class representing a sanctuary where mages can gather."""

    def __init__(
        self,
        name: str,
        bows: List[SpellcasterBow],
        quivers: List[MysticQuiver],
        enemies: List["Enemy"],
    ):
        """Initialize with a name and lists of bows, quivers, and enemies."""
        super().__init__(name)
        self.bows: List[SpellcasterBow] = bows
        self.quivers: List[MysticQuiver] = quivers
        self.enemies: List[Enemy] = enemies
        self.mages: List[Mage] = []

    def add_mage(self, mage: "Mage") -> None:
        """Add a mage to the sanctuary."""
        self.mages.append(mage)


class Mage(NamedObject):
    """Class representing a mage with health and stealth components."""

    def __init__(self, name: str):
        """Initialize with a name and default components."""
        super().__init__(name)
        self.health: HealthComponent = HealthComponent(100)
        self.stealth: StealthComponent = StealthComponent(50)
        self.inventory: List[NamedObject] = []
        self.sanctuary: Optional[Sanctuary] = None

    def perform_action(self) -> None:
        """Safe access to the health component."""
        print(
            f"{self.name} is taking action with current health: "
            f"{self.health.health}"
        )


class Enemy(NamedObject):
    """Enemy class for combat interaction."""

    def __init__(self, name: str, health: int, damage: int):
        """Initialize an enemy."""
        super().__init__(name)
        self.health = HealthComponent(health)
        self.damage = damage

    def attack(self, target: Mage) -> None:
        """Attempt to attack a target mage."""
        target.health.reduce_health(self.damage)
        print(
            f"{self.name} attacks {target.name} for {self.damage} damage. "
            f"{target.name}'s health: {target.health.health}"
        )


class ArcaneChampion(Mage):
    """A specialized mage class with enhanced abilities & hunger management."""

    def __init__(self, name: str, health: int):
        """Initialize with a name and specific health."""
        super().__init__(name)
        self.health = HealthComponent(health)
        self.damage_multiplier = 1.0

    def attack(self, target: Enemy, weapon: SpellcasterBow) -> None:
        """Attempt to attack a target with a bow."""
        if not isinstance(target, Enemy):
            print("The target is not an enemy.")
            return
        if weapon not in self.inventory:
            print(f"{weapon.get_name()} not found in inventory.")
            return

        if self.stealth.visibility < 60:
            damage = int(weapon.damage() * self.damage_multiplier)
            if damage > 0:
                target.health.reduce_health(damage)
                print(
                    f"{target.get_name()} was hit for {damage} damage, "
                    f"{target.health.health} health remaining."
                )
                if target.health.health <= 0:
                    print(f"{target.get_name()} has been defeated.")
            else:
                print("No arrows left, reloading...")
                quiver = next(
                    (
                        item
                        for item in self.inventory
                        if isinstance(item, MysticQuiver)
                    ),
                    None,
                )
                if quiver:
                    weapon.load(quiver)  # Reload the bow
                    print("Arrows reloaded.")
                else:
                    print("No quiver available to reload arrows.")
        else:
            print("Too visible to attack stealthily.")
            self.offer_stealth_options()

        self.stealth.modify_visibility(random.randint(5, 15))
        print(
            f"{self.name}'s visibility increased to {self.stealth.visibility}."
        )

    def offer_stealth_options(self) -> None:
        """Provide the player with options to reduce visibility."""
        print(
            "You are too visible to attack stealthily. "
            "Choose a stealth tactic:"
        )
        print("1. Move Behind a Rock")
        print("2. Move Up to Hill")
        print("3. Hide in Grass")
        tactic = input("Choose a tactic (1-3): ")

        if tactic == "1":
            self.stealth.modify_visibility(-30)
            self.health.reduce_health(5)
            self.damage_multiplier = 1.5
            print(
                f"Moved behind a rock but almost hit by the enemy! "
                f"Current visibility: {self.stealth.visibility}, "
                f"Health: {self.health.health}. "
                f"You've found a good attacking angle behind the rock! "
                f"Damage enhanced by 50%."
            )
        elif tactic == "2":
            self.stealth.modify_visibility(-40)
            self.damage_multiplier = 0.85  # Reduce damage output by 15%
            print(
                f"Moved up to hill. "
                f"Current visibility: {self.stealth.visibility}, "
                f"Damage reduced by 15%."
            )
        elif tactic == "3":
            self.stealth.modify_visibility(-15)
            self.damage_multiplier = 1.05
            print(
                f"Hidden in grass. "
                f"Current visibility: {self.stealth.visibility}, "
                f"Damage enhanced by 5%."
            )
        else:
            print("Invalid tactic. No changes made.")


def load_data_tsv(filename: str) -> List[Dict[str, Any]]:
    """Load data from a specified TSV file."""
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            return [dict(row) for row in reader]
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


class Game:
    """Play game."""

    def __init__(self) -> None:
        """Initialize game components and load data."""
        # Load data
        self.bows = {
            bow["Name"]: SpellcasterBow(
                bow["Name"], int(bow["MinDmg"]), int(bow["MaxDmg"])
            )
            for bow in load_data_tsv("data/spellcaster_bows.tsv")
        }
        self.quivers = {
            quiver["Name"]: MysticQuiver(quiver["Name"], int(quiver["Qty"]))
            for quiver in load_data_tsv("data/mystic_quivers.tsv")
        }
        self.enemies = {
            enemy["Name"]: Enemy(
                enemy["Name"], int(enemy["Health"]), int(enemy["Damage"])
            )
            for enemy in load_data_tsv("data/enemies.tsv")
        }
        self.sanctuaries = self.initialize_sanctuaries()

        # Randomly select a sanctuary to start the game
        self.current_sanctuary = random.choice(self.sanctuaries)

        # Setup player
        self.player = ArcaneChampion("Hero", 200)
        self.enemies_defeated = False

    def initialize_sanctuaries(self) -> list[Sanctuary]:
        """Initialize sanctuaries from data file."""
        sanctuary_data = load_data_tsv("data/sanctuaries.tsv")
        sanctuaries = []
        for data in sanctuary_data:
            bows = [self.bows[name] for name in data["Bows"].split(", ")]
            quivers = [
                self.quivers[name] for name in data["Quivers"].split(", ")
            ]
            enemies = [
                self.enemies[name] for name in data["Enemies"].split(", ")
            ]
            sanctuaries.append(Sanctuary(data["Name"], bows, quivers, enemies))
        return sanctuaries

    def run(self) -> None:
        """Run the main game loop."""
        while True:
            print(f"\nWelcome to {self.current_sanctuary.get_name()}!")
            print(f"Your health: {self.player.health.health}")
            print("Available actions:")
            print("1. Explore (fight an enemy)")
            print("2. Check Inventory")
            print("3. Select Equipment (Should be done before fight)")
            print("4. Exit Game")
            choice = input("Choose an action (1-4): ")

            if choice == "1":
                self.explore()
                if self.enemies_defeated:
                    print(
                        "Congratulations! You have defeated all the enemies!"
                    )
                    break
            elif choice == "2":
                self.check_inventory()
            elif choice == "3":
                self.select_equipment()
            elif choice == "4":
                print("Exiting game...")
                sys.exit(0)
            else:
                print("Invalid input, please choose a valid action.")

    def explore(self) -> None:
        """Handle exploration and combat."""
        enemy = random.choice(self.current_sanctuary.enemies)
        print(f"You encounter a {enemy.get_name()}!")
        while enemy.health.health > 0:
            action = input(
                f"Do you want to attack the {enemy.get_name()}? (yes/no): "
            )
            if action.lower() == "yes":
                weapon = next(
                    (
                        item
                        for item in self.player.inventory
                        if isinstance(item, SpellcasterBow)
                    ),
                    None,
                )
                if weapon:
                    self.player.attack(enemy, weapon)
                    if enemy.health.health > 0:
                        print(
                            f"{enemy.get_name()} has "
                            f"{enemy.health.health} health left."
                        )
                    else:
                        print(f"You defeated the {enemy.get_name()}!")
                        self.current_sanctuary.enemies.remove(enemy)
                        if not self.current_sanctuary.enemies:
                            self.enemies_defeated = True
                        break
                else:
                    print("No weapon to attack with!")
            elif action.lower() == "no":
                print("You choose to avoid the fight.")
                break
            else:
                print("Invalid choice, please respond with 'yes' or 'no'.")

            if self.player.stealth.visibility >= 60:
                enemy.attack(self.player)

            if self.player.health.health <= 0:
                print("You have been defeated.")
                sys.exit(0)

    def check_inventory(self) -> None:
        """Display player's inventory."""
        if not self.player.inventory:
            print("Your inventory is empty.")
        for item in self.player.inventory:
            if isinstance(item, SpellcasterBow):
                print(f"Bow: {item.get_name()}, Shots left: {item.shots}")
            elif isinstance(item, MysticQuiver):
                print(f"Quiver: {item.get_name()}, Arrows left: {item.qty}")

    def select_equipment(self) -> None:
        """Allow the player to select equipment from the current sanctuary."""
        # Selection of bows
        while True:
            print("Select your Bow:")
            for idx, bow in enumerate(self.current_sanctuary.bows):
                print(f"{idx + 1}. {bow.get_name()}")

            try:
                bow_choice = int(input("Enter the number for your choice: "))
                if 0 < bow_choice <= len(self.current_sanctuary.bows):
                    bow_choice -= 1  # Convert to zero-index
                    self.player.inventory.append(
                        self.current_sanctuary.bows[bow_choice]
                    )
                    print(
                        f"You have selected the "
                        f"{self.current_sanctuary.bows[bow_choice].get_name()}."
                    )
                    break  # Exit the loop if choice is valid
                else:
                    print("Invalid choice, please select a valid number.")
            except ValueError:
                print("Incompatible type, please enter a valid integer.")

        # Selection of quivers
        while True:
            print("Select your Quiver:")
            for idx, quiver in enumerate(self.current_sanctuary.quivers):
                print(f"{idx + 1}. {quiver.get_name()}")

            try:
                quiver_choice = int(
                    input("Enter the number for your choice: ")
                )
                if 0 < quiver_choice <= len(self.current_sanctuary.quivers):
                    quiver_choice -= 1  # Convert to zero-index
                    self.player.inventory.append(
                        self.current_sanctuary.quivers[quiver_choice]
                    )
                    print(
                        f"You have selected the "
                        f"{self.current_sanctuary.quivers[quiver_choice].get_name()}."
                    )
                    break  # Exit the loop if choice is valid
                else:
                    print("Invalid choice, please select a valid number.")
            except ValueError:
                print("Incompatible type, please enter a valid integer.")


# Example of starting the game
if __name__ == "__main__":
    game = Game()
    game.run()

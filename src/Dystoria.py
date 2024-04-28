"""This is our Dytoria Game."""

import random
from typing import List


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
        self.health: HealthComponent = HealthComponent(100)
        self.stealth: StealthComponent = StealthComponent(50)
        self.inventory: List[NamedObject] = []

    def perform_action(self) -> None:
        """Safe access to the health component."""
        print(
            f"{self.name} is taking action with current health: {self.health.health}"
        )


class ArcaneChampion(Mage):
    """A specialized mage class with enhanced abilities & hunger management."""

    def __init__(self, name: str, health: int):
        """Initialize with a name and specific health."""
        super().__init__(name)
        self.health = HealthComponent(health)
        self.stealth = StealthComponent(50)
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
            if self.stealth.visibility < 30:  # Directly use stealth attribute
                damage = weapon.damage()
                target.health.reduce_health(
                    damage
                )  # Directly use health attribute of target
                if target.health.health <= 0:
                    print(f"{target.get_name()} has been defeated.")
            else:
                print("Too visible to attack stealthily.")
        else:
            print(f"{weapon.get_name()} not found in inventory.")


class Enemy(NamedObject):
    """Enemy class for combat interaction."""

    def __init__(self, name: str, health: int):
        """Initialize an enemy."""
        super().__init__(name)
        self.health = HealthComponent(health)


def create_mage():
    """Create a mage when the game starts."""
    name = input("Enter the name of your mage: ")
    health = int(
        input(
            "Enter the starting health of your mage (50-100, recommended 100 for beginners): "
        )
    )
    return ArcaneChampion(name, max(50, min(100, health)))


def choose_sanctuary():
    """Create a sanctury  when the game starts."""
    sanctuary_name = input(
        "Enter the name of your sanctuary or press enter to default to 'Mystic Grove': "
    )
    return Sanctuary(sanctuary_name if sanctuary_name else "Mystic Grove")


def find_item():
    """Explore in the game."""
    items = [
        SpellcasterBow("Mystic Bow", 15, 25),
        MysticQuiver("Basic Arrows", 20),
    ]
    found_item = random.choice(items)
    print(f"You found a {found_item.get_name()}!")
    return found_item


def create_enemy():
    """Randomly creates an enemy."""
    enemies = [Enemy("Goblin", 50), Enemy("Orc", 80)]
    return random.choice(enemies)


def display_enemies(enemies):
    """Displays a list of enemies."""
    for i, enemy in enumerate(enemies, 1):
        print(f"{i}. {enemy.get_name()} - Health: {enemy.health.health}")


def initiate_attack(champion, enemies):
    """Initiates an attack sequence."""
    print("Choose an enemy to attack:")
    display_enemies(enemies)
    choice = int(input("Select an enemy (number): ")) - 1
    enemy = enemies[choice]
    weapon = champion.inventory[
        0
    ]  # Simplified: using the first weapon in the inventory
    if attack_target(champion, enemy, weapon):
        enemies.remove(enemy)  # Remove defeated enemy


def attack_target(player, enemy, weapon):
    """Handles the attack mechanics."""
    if weapon in player.inventory:
        print(f"Attacking {enemy.get_name()} with {weapon.get_name()}...")
        damage = weapon.damage()
        enemy.health.reduce_health(damage)
        print(
            f"Dealt {damage} damage to {enemy.get_name()}. Remaining health: {enemy.health.health}"
        )
        if enemy.health.health <= 0:
            print(f"{enemy.get_name()} has been defeated!")
            return True
    else:
        print("You do not have that weapon in your inventory.")
    return False


def play_game():
    """Start and play the game."""
    print("Welcome to Dystoria: Shadows of Magic!")
    champion = create_mage()
    sanctuary = choose_sanctuary()
    sanctuary.add_mage(champion)

    # Starting inventory
    bow = SpellcasterBow("Starter Bow", 10, 20)
    champion.inventory.append(bow)
    print(f"Starting with {bow.get_name()} in your inventory.")

    # List of enemies
    enemies = [create_enemy() for _ in range(3)]

    actions = {
        "explore": lambda: champion.inventory.append(find_item()),
        "inventory": lambda: ", ".join(
            [item.get_name() for item in champion.inventory]
        ),
        "status": lambda: f"Health: {champion.health.health}, Stealth: {champion.stealth.visibility}, Hunger: {champion.hunger}",
        "attack": lambda: initiate_attack(champion, enemies),
    }

    while True:
        command = input(
            "Enter a command (explore, attack, inventory, status, exit): "
        ).lower()

        if command == "exit":
            print("Exiting the game. Goodbye!")
            break
        elif command in actions:
            result = actions[command]()
            print(result() if callable(result) else result)
        else:
            print("Unknown command. Try again.")


play_game()

"""This is our Dytoria Game."""

"""Introduction to the Dystoria Universe

Welcome to the Dystoria Universe, a realm where the echoes of ancient magic 
clash with the oppressive forces of a technocratic regime. This world, once 
brimming with mystical energies and vibrant life, has been subdued under the 
iron grip of the Dystorian Order, a powerful government that has outlawed the 
old ways in pursuit of control through technology.

The Setting
Dystoria is a world divided between the remnants of arcane wisdom and the stark
realities of a monitored society. The land is scattered with hidden 
sanctuaries, secret places where the last guardians of magic, known as the 
Arcane Champions, train in the mystical arts away from prying eyes. These 
champions are the heirs to the forgotten spells and ancient rites capable of 
bending the very fabric of reality.

Outside these sanctuaries, the cities of Dystoria pulse with a different kind 
of energy—mechanical and digital. Surveillance drones sweep the skies, and 
citizens lead monitored lives, their every action observed and recorded by the 
Order. Magic is a crime punishable by disappearance and death, and those 
suspected of harboring arcane abilities are relentlessly hunted.

The Conflict
The Dystorian Order's rise to power was swift and brutal. Magic was deemed 
chaotic and dangerous—a threat to the order and progress promised by 
technology. Books were burned, mages were executed, and ancient sites were 
razed. In response, the remaining magical practitioners retreated into the 
shadows, forming clandestine networks to preserve their knowledge and 
traditions.

Now, as the grip of the Order tightens, tensions are reaching a breaking point.
Small acts of rebellion have begun to ignite the fires of resistance, and 
whispers of a major uprising are spreading. The Arcane Champions, trained in 
both the arcane arts and the skills necessary to survive in a hostile 
environment, stand at the heart of this brewing storm. They are not only 
defenders of the old ways but also symbols of hope for freedom and change.

The Gameplay
In "Dystoria: Shadows of Magic," players take on the role of an Arcane 
Champion. The game combines elements of RPGs and strategic simulations, 
allowing players to explore a richly detailed world, develop their magical 
abilities, engage in both stealth and combat, and make choices that will 
influence the outcome of the story.

Key Features:
Character Development: Players can customize their champions, develop their 
magical and combat skills, and choose their paths through skill trees and 
arcane research.
Exploration and Discovery: Uncover hidden sanctuaries, lost artifacts, and 
secret truths as you navigate through the Dystorian landscape.
Stealth and Combat: Use stealth to evade the Order's forces or engage them 
directly with a combination of magic and weaponry. Manage resources such as 
mystic quivers and spellcaster bows to maintain an edge in combat.
Dynamic Storytelling: Your decisions matter. The alliances you form, the 
enemies you make, and the secrets you uncover will shape the future of Dystoria.
Survival Elements: Manage your resources wisely, from food and magical 
ingredients to the mystical artifacts that enhance your powers.
"""
import random


class NamedObject:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Component:
    def update(self, owner):
        pass


class HealthComponent(Component):
    def __init__(self, health):
        self.health = health

    def add_health(self, amount):
        self.health = min(100, self.health + amount)

    def reduce_health(self, amount):
        self.health = max(0, self.health - amount)


class StealthComponent(Component):
    def __init__(self, visibility):
        self.visibility = visibility

    def modify_visibility(self, amount):
        self.visibility = max(0, self.visibility + amount)


class ArcaneWeapon(NamedObject):
    def __init__(self, name, min_dmg, max_dmg):
        super().__init__(name)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def damage(self):
        return random.randint(self.min_dmg, self.max_dmg)


class MysticQuiver(NamedObject):
    def __init__(self, name, qty):
        super().__init__(name)
        self.qty = qty

    def get_quantity(self):
        return self.qty

    def remove_all(self):
        self.qty = 0
        return self.qty


class SpellcasterBow(ArcaneWeapon):
    def __init__(self, name, min_dmg, max_dmg):
        super().__init__(name, min_dmg, max_dmg)
        self.shots = 0

    def load(self, ammo):
        if ammo.get_name() == self.get_name():
            self.shots += ammo.get_quantity()
            ammo.remove_all()

    def damage(self):
        if self.shots > 0:
            self.shots -= 1
            return super().damage()
        return 0


class Sanctuary(NamedObject):
    def __init__(self, name):
        super().__init__(name)
        self.mages = []

    def add_mage(self, mage):
        self.mages.append(mage)


class Mage(NamedObject):
    def __init__(self, name):
        super().__init__(name)
        self.components = {
            "health": HealthComponent(100),
            "stealth": StealthComponent(50),
        }
        self.inventory = []

    def perform_action(self):
        print(
            f"{self.name} is taking action with current health: {self.components['health'].health}"
        )


class ArcaneChampion(Mage):
    def __init__(self, name, health):
        super().__init__(name)
        self.components["health"] = HealthComponent(health)
        self.components["stealth"] = StealthComponent(50)
        self.hunger = 100
        self.inventory = []

    def reduce_hunger(self, amount):
        self.hunger -= amount
        if self.hunger < 0:
            self.hunger = 0

    def increase_hunger(self, amount):
        self.hunger += amount
        if self.hunger > 100:
            self.hunger = 100

    def eat(self, food):
        if food in self.inventory:
            self.reduce_hunger(food.get_food_value())
            self.inventory.remove(food)
        else:
            print(f"{food.get_name()} is not in inventory.")

    def attack(self, target, weapon):
        if weapon in self.inventory and isinstance(weapon, ArcaneWeapon):
            if self.components["stealth"].visibility < 30:
                damage = weapon.damage()
                target.components["health"].reduce_health(damage)
                if target.components["health"].health <= 0:
                    print(f"{target.get_name()} has been defeated.")
            else:
                print("Too visible to attack stealthily.")
        else:
            print(f"{weapon.get_name()} not found in inventory.")


sanctuary = Sanctuary("Dystoria Safe Haven")
champion = ArcaneChampion("Hero", 90)
sanctuary.add_mage(champion)
bow = SpellcasterBow("Enchanted Longbow", 20, 40)
arrows = MysticQuiver("Enchanted Longbow", 15)
champion.inventory.append(bow)
champion.inventory

"""Other features to add:
1. Dynamic World Events
Seasonal Changes: Implement seasons that affect game mechanics, such as different resources available, changes in enemy behavior, and special seasonal events.
Random Encounters: Introduce random events like ambushes by regime forces, mystical anomalies, or chance meetings with other characters that can offer quests or trade.
2. Crafting and Enchantment System
Alchemy and Potion Making: Allow players to collect ingredients during their explorations to brew potions with various effects, enhancing combat or survival abilities.
Weapon and Armor Crafting: Players can craft and customize their gear, choosing materials and magical enhancements that affect the properties of the final item.
3. Complex Relationship and Faction Dynamics
Reputation System: Your actions affect how different factions view your character. High reputation with a faction could unlock unique missions, discounts at merchants, or assistance in battles.
Companion Characters: Introduce characters that can join the player's quest, each with unique stories, abilities, and personal quests. Their loyalty could change based on the player's decisions and actions.
4. Skill-Based Dialogue Options
Persuasion and Intimidation: Depending on the player's skills or knowledge, different dialogue options can be unlocked that allow for persuasion, intimidation, or deception, influencing the game's narrative and outcomes.
5. In-depth Lore and Interactive Storytelling
Books and Scrolls: Discovering ancient texts that the player can actually read, offering deep lore that enriches the world and may hint at hidden locations or secrets.
Branching Quests: Quests with multiple outcomes based on player choices, affecting the world state and how NPCs react to the player.
6. Magical Research and Development
Spell Creation: Allow players to research and create their own spells by combining spell components in a magical "lab". This could be a trial and error process with potentially explosive results.
Magical Experiments: Engage in experiments that can lead to unique magical abilities or catastrophic failures, influencing the player's reputation and magical prowess.
7. Advanced Survival Mechanics
Resource Scarcity and Management: Make resources scarce and management crucial, including food, water, and magical energy, adding a layer of survival challenge.
Environmental Hazards: Implement hazards like toxic areas, magic-disturbed zones that require specific gear or spells to navigate.
8. Base Building and Defense
Sanctuary Upgrades: Allow players to build and upgrade their sanctuaries, adding defensive structures, magical wards, or resource-producing buildings.
Defensive Scenarios: Organize and defend against raids by the regime forces, using both combat and strategic planning."""

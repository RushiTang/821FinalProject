# Dytoria Game

Welcome to Dytoria, a mystical realm where magic and stealth govern the balance of power. In this game, players take on the roles of mages, navigating through sanctuaries, engaging in combat, and managing resources like health and stealth to achieve supremacy over their rivals.

## Features
- **Dynamic Characters:** Play as a Hero with unique abilities and components like health and stealth.
- **Magical Weapons:** Utilize a variety of arcane weapons, each with different damage potentials.
- **Strategic Gameplay:** Manage health, visibility and inventory to strategically defeat your opponents.

## For End Users: How to Play

### Setup
 ```bash
 git clone https://github.com/RushiTang/821FinalProject
 cd 821FinalProject
 ```

### Start the Game
 ```bash
 python src/Dystoria.py 
 ```

### Gameplay Mechanics
- **Health and Stealth:** Manage your character’s health and stealth levels to protect them from being defeated and to sneak up on enemies.
- **Weapons and Combat:** Engage in battles by using weapons. Calculate damage based on the weapon's damage range and your current stealth level.
- **Resource Management:** Keep an eye on your inventory and manage resources such as arrows in your Mystic Quiver.

#### Playing as a Mage
1. **Initiate with Basic Setup:** Start with predefined health and stealth levels.
2. **Perform Actions:** Take actions based on your strategic decisions, managing health and stealth to optimize survival and attack capabilities.

#### Encountering enemies
- **Combat Encounters:** Confront enemies with varying health and damage. Use your weapons to reduce their health while managing your own survival.

### Winning the Game
The objective is to navigate through sanctuaries, strategically managing health, stealth, and resources to outlast and defeat other players or enemies. Form alliances or tactically use the game's mechanics to gain advantages.

### Sample Interactive session
Yixuans-MacBook-Air:821FinalProject yixuan$ python src/Dystoria.py
Welcome to Mystic Forest!
Your health: 200
Available actions:
1. Explore (fight an enemy)
2. Check Inventory
3. Select Equipment (Should be done before fight)
4. Exit Game
Choose an action (1-4): 3
Select your Bow:
1. Fire Bow
2. Lightning Bow
Enter the number for your choice: 1
You have selected the Fire Bow.
Select your Quiver:
1. Small Quiver
2. Large Quiver
Enter the number for your choice: 2
You have selected the Large Quiver.

Welcome to Mystic Forest!
Your health: 200
Available actions:
1. Explore (fight an enemy)
2. Check Inventory
3. Select Equipment (Should be done before fight)
4. Exit Game
Choose an action (1-4): 1
You encounter a Goblin!
Do you want to attack the Goblin? (yes/no): yes
Goblin was hit for 35 damage, 15 health remaining.
Hero's visibility increased to 65.
Goblin has 15 health left.
Goblin attacks Hero for 10 damage. Hero's health: 190
Do you want to attack the Goblin? (yes/no): yes
Too visible to attack stealthily.
You are too visible to attack stealthily. Choose a stealth tactic:
1. Move Behind a Rock
2. Move Up to Hill
3. Hide in Grass
Choose a tactic (1-3): 3
Hidden in grass. Current visibility: 50Damage enhanced by 5%.
Hero's visibility increased to 64.
Goblin has 15 health left.
Goblin attacks Hero for 10 damage. Hero's health: 180
Do you want to attack the Goblin? (yes/no): yes
Too visible to attack stealthily.
You are too visible to attack stealthily. Choose a stealth tactic:
1. Move Behind a Rock
2. Move Up to Hill
3. Hide in Grass
Choose a tactic (1-3): 2
Moved up to hill. Current visibility: 24, Damage reduced by 15%.
Hero's visibility increased to 37.
Goblin has 15 health left.
Do you want to attack the Goblin? (yes/no): yes
Goblin was hit for 20 damage, 0 health remaining.
Goblin has been defeated.
Hero's visibility increased to 52.
You defeated the Goblin!

Welcome to Mystic Forest!
Your health: 180
Available actions:
1. Explore (fight an enemy)
2. Check Inventory
3. Select Equipment (Should be done before fight)
4. Exit Game
Choose an action (1-4): 1
You encounter a Troll!
Do you want to attack the Troll? (yes/no): yes
Troll was hit for 29 damage, 71 health remaining.
Hero's visibility increased to 59.
Troll has 71 health left.
Do you want to attack the Troll? (yes/no): yes
Troll was hit for 34 damage, 37 health remaining.
Hero's visibility increased to 65.
Troll has 37 health left.
Troll attacks Hero for 20 damage. Hero's health: 160
Do you want to attack the Troll? (yes/no): yes
Too visible to attack stealthily.
You are too visible to attack stealthily. Choose a stealth tactic:
1. Move Behind a Rock
2. Move Up to Hill
3. Hide in Grass
Choose a tactic (1-3): 1
Moved behind a rock but almost hit by the enemy! Current visibility: 35, Health: 155You've found a good attacking angle behind the rock!Damage enhanced by 50%.
Hero's visibility increased to 41.
Troll has 37 health left.
Do you want to attack the Troll? (yes/no): yes
Troll was hit for 34 damage, 3 health remaining.
Hero's visibility increased to 52.
Troll has 3 health left.
Do you want to attack the Troll? (yes/no): yes
Troll was hit for 39 damage, 0 health remaining.
Troll has been defeated.
Hero's visibility increased to 61.
You defeated the Troll!
Congratulations! You have defeated all the enemies!

## For Developers:
Given the context of your game and its implementation, the "For Developers" section of the README could include details on how to set up the development environment, run tests, and contribute to the game's codebase. Below is a proposed outline and content for this section:

### For Developers

#### Running Tests
To ensure that your modifications do not break existing functionality, run the following command to execute the test suite:
```bash
pytest tests/Test_Dystroria
```
Make sure all tests pass before pushing any changes.

#### Code Structure
- **Modules and Classes:**
  The game is organized into several Python classes each handling different aspects of the game such as characters (`Mage`, `Enemy`), components (`HealthComponent`, `StealthComponent`), and game management (`Game`).
  
- **Data Files:**
  Game data is loaded from TSV files stored in the `data` directory. Here's a brief overview of what each file contains:
  - `enemies.tsv`: Information about different enemies in the game.
  - `mystic_quivers.tsv`: Details on various quivers available.
  - `sanctuaries.tsv`: Configuration of different sanctuaries.
  - `spellcaster_bows.tsv`: Specifications of different spellcaster bows.

#### Contributing
We welcome contributions to the Dytoria game. Here's how you can contribute:
- **Bug Fixes:** If you find a bug, feel free to fork the repository, fix the bug, and submit a pull request.
- **Feature Requests:** Have ideas for new features? Open an issue to discuss them or propose them via pull requests.
- **Improving Documentation:** Help us improve our documentation or translate it into different languages.

#### Documentation
- **Code Comments:** Use comments to explain the purpose of complex sections of code.
- **Docstrings:** Each function and class should have a Python docstring providing a description of its function.

### Conclusion
Dytoria offers a world of magical battles and strategic resource management, perfect for players who enjoy deep, engaging gameplay intertwined with fantasy elements. Whether you're sneaking through the shadows and launching a full-scale magical assault, Dytoria promises thrilling adventures and intense tactical battles.

Feel free to tailor the content above to fit the specifics of your game project or repository structure. This section aims to guide new developers through the setup process and encourage them to contribute effectively.


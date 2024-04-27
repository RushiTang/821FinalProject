"""Tests."""

from Dystoria import (
    ArcaneChampion,
    ArcaneWeapon,
    HealthComponent,
    Mage,
    MysticQuiver,
    NamedObject,
    Sanctuary,
    SpellcasterBow,
    StealthComponent,
)


def test_named_object_initialization() -> None:
    """Test the initialization of a NamedObject to ensure it stores.

    and returns the correct name.
    """
    obj = NamedObject("Test Object")
    assert obj.get_name() == "Test Object", "NamedObject initialization failed"


def test_health_component() -> None:
    """Test the HealthComponent for correct initialization, health reduction.

    and non-negative health enforcement.
    """
    health = HealthComponent(100)
    assert health.health == 100, "Health not initialized correctly"
    health.reduce_health(30)
    assert health.health == 70, "Health not reduced correctly"
    health.reduce_health(90)
    assert health.health == 0, "Health should not go below zero"


def test_stealth_component() -> None:
    """Test the StealthComponent for proper initialization.

    and modification of visibility,
    ensuring visibility does not drop below zero.
    """
    stealth = StealthComponent(50)
    assert stealth.visibility == 50, "Visibility not initialized correctly"
    stealth.modify_visibility(-20)
    assert stealth.visibility == 30, "Visibility not reduced correctly"
    stealth.modify_visibility(-50)
    assert stealth.visibility == 0, "Visibility should not go below zero"


def test_arcane_weapon_damage() -> None:
    """Test the ArcaneWeapon generates damage within the expected range."""
    weapon = ArcaneWeapon("Magic Sword", 10, 20)
    damage = weapon.damage()
    assert 10 <= damage <= 20, "Damage out of expected range"


def test_mystic_quiver() -> None:
    """Test the MysticQuiver for correct initialization of quantity.

    and its removal functionality.
    """
    quiver = MysticQuiver("Basic Quiver", 5)
    assert quiver.get_quantity() == 5, "Quiver quantity incorrect"
    quiver.remove_all()
    assert quiver.get_quantity() == 0, "Quiver not emptied correctly"


def test_spellcaster_bow() -> None:
    """Test the SpellcasterBow to ensure it loads from a quiver correctly.

    and that damage calculation and shot decrement work as expected.
    """
    bow = SpellcasterBow("Elven Bow", 15, 25)
    quiver = MysticQuiver("Elven Bow", 3)
    bow.load(quiver)
    assert bow.shots == 3, "Bow not loaded correctly"
    damage = bow.damage()
    assert 15 <= damage <= 25, "Bow damage out of range"
    assert bow.shots == 2, "Shots not decremented"


def test_sanctuary() -> None:
    """Test the Sanctuary can add mages and store them correctly."""
    sanctuary = Sanctuary("Safe Haven")
    mage = Mage("Gandalf")
    sanctuary.add_mage(mage)
    assert mage in sanctuary.mages, "Mage not added to sanctuary"


def test_arcane_champion() -> None:
    """Test the ArcaneChampion for correct initialization.

    and functionality of hunger management.
    """
    champion = ArcaneChampion("Artemis", 120)
    assert champion.hunger == 100, "Initial hunger should be capped at 100"
    champion.reduce_hunger(20)
    assert champion.hunger == 80, "Hunger not reduced correctly"
    champion.increase_hunger(50)
    assert (
        champion.hunger == 100
    ), "Hunger not increased correctly or capped at max"

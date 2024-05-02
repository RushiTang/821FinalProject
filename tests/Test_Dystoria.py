"""Tests."""

from Dystoria import (
    Enemy,
    HealthComponent,
    Mage,
    MysticQuiver,
    NamedObject,
    Sanctuary,
    SpellcasterBow,
    StealthComponent,
    load_data_tsv,
)


def test_named_object_initialization() -> None:
    """Test the initialization of a NamedObject."""
    obj = NamedObject("Test Object")
    assert obj.get_name() == "Test Object", "NamedObject initialization failed"


def test_health_component() -> None:
    """Test the HealthComponent."""
    health = HealthComponent(100)
    assert health.health == 100, "Health not initialized correctly"
    health.reduce_health(30)
    assert health.health == 70, "Health not reduced correctly"
    health.reduce_health(90)
    assert health.health == 0, "Health should not go below zero"


def test_stealth_component() -> None:
    """Test the StealthComponent."""
    stealth = StealthComponent(50)
    assert stealth.visibility == 50, "Visibility not initialized correctly"
    stealth.modify_visibility(-20)
    assert stealth.visibility == 30, "Visibility not reduced correctly"
    stealth.modify_visibility(-50)
    assert stealth.visibility == 0, "Visibility should not go below zero"


def test_load_data_tsv() -> None:
    """Test loading data from a TSV file."""
    bows = load_data_tsv("data/spellcaster_bows.tsv")
    assert isinstance(bows, list), "Data should be a list"
    assert len(bows) > 0, "Data should not be empty"
    assert (
        "Name" in bows[0] and "MinDmg" in bows[0] and "MaxDmg" in bows[0]
    ), "Bow data should contain expected fields"

    quivers = load_data_tsv("data/mystic_quivers.tsv")
    assert isinstance(quivers, list), "Data should be a list"
    assert len(quivers) > 0, "Data should not be empty"
    assert (
        "Name" in quivers[0] and "Qty" in quivers[0]
    ), "Quiver data should contain expected fields"

    enemies = load_data_tsv("data/enemies.tsv")
    assert isinstance(enemies, list), "Data should be a list"
    assert len(enemies) > 0, "Data should not be empty"
    assert (
        "Name" in enemies[0]
        and "Health" in enemies[0]
        and "Damage" in enemies[0]
    ), "Enemy data should contain expected fields"


def test_spellcaster_bow_with_data_file() -> None:
    """Test the SpellcasterBow with data from a file."""
    bows_data = load_data_tsv("data/spellcaster_bows.tsv")
    bow = SpellcasterBow(
        bows_data[0]["Name"],
        int(bows_data[0]["MinDmg"]),
        int(bows_data[0]["MaxDmg"]),
    )
    quivers_data = load_data_tsv("data/mystic_quivers.tsv")
    quiver = MysticQuiver(quivers_data[0]["Name"], int(quivers_data[0]["Qty"]))
    bow.load(quiver)
    assert bow.shots == int(quivers_data[0]["Qty"]), "Bow not loaded correctly"
    damage = bow.damage()
    assert (
        int(bows_data[0]["MinDmg"]) <= damage <= int(bows_data[0]["MaxDmg"])
    ), "Bow damage out of range"


def test_sanctuary_with_data_file() -> None:
    """Test the Sanctuary class using data files for initialization."""
    bows_data = load_data_tsv("data/spellcaster_bows.tsv")
    quivers_data = load_data_tsv("data/mystic_quivers.tsv")
    enemies_data = load_data_tsv("data/enemies.tsv")
    sanctuary = Sanctuary(
        "Test Sanctuary",
        [
            SpellcasterBow(b["Name"], int(b["MinDmg"]), int(b["MaxDmg"]))
            for b in bows_data
        ],
        [MysticQuiver(q["Name"], int(q["Qty"])) for q in quivers_data],
        [
            Enemy(e["Name"], int(e["Health"]), int(e["Damage"]))
            for e in enemies_data
        ],
    )
    mage = Mage("Test Mage")
    sanctuary.add_mage(mage)
    assert mage in sanctuary.mages, "Mage not added to sanctuary correctly"

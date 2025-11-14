"""
COMP 163 - Project 2: Character Abilities Showcase
Name: Bryant Clarke
Date: 11/5/25

AI Usage: AI assisted with concepts of class design, inheritance structure, method overriding,
polymorphism examples, and comments. I fully wrote, reviewed, revised, and can explain all code.
"""

# ============================================================================
# PROVIDED BATTLE SYSTEM (DO NOT MODIFY)
# ============================================================================

class SimpleBattle:
    """
    Simple battle system provided for you to test your characters.
    DO NOT MODIFY THIS CLASS - just use it to test your character implementations.
    """
    
    def __init__(self, character1, character2):
        self.char1 = character1
        self.char2 = character2
    
    def fight(self):
        """Simulates a simple battle between two characters"""
        print(f"\n=== BATTLE: {self.char1.name} vs {self.char2.name} ===")
        
        # Show starting stats
        print("\nStarting Stats:")
        self.char1.display_stats()
        self.char2.display_stats()
        
        print(f"\n--- Round 1 ---")
        print(f"{self.char1.name} attacks:")
        self.char1.attack(self.char2)
        
        if self.char2.health > 0:
            print(f"\n{self.char2.name} attacks:")
            self.char2.attack(self.char1)
        
        print(f"\n--- Battle Results ---")
        self.char1.display_stats()
        self.char2.display_stats()
        
        if self.char1.health > self.char2.health:
            print(f"🏆 {self.char1.name} wins!")
        elif self.char2.health > self.char1.health:
            print(f"🏆 {self.char2.name} wins!")
        else:
            print("🤝 It's a tie!")

# ============================================================================
# YOUR CLASSES TO IMPLEMENT (6 CLASSES TOTAL)
# ============================================================================

from typing import Optional
import random

class Character:
    """
    Base class for all characters.
    This is the top of our inheritance hierarchy.
    """
    
    def __init__(self, name: str, health: int, strength: int, magic: int):
        """Initialize basic character attributes"""
        """Set the character's name, health, strength, and magic;
        stored as instance variables"""
        self.name = name
        self.health = int(health)
        self.strength = int(strength)
        self.magic = int(magic)
        # Composition hook: characters can HAVE a weapon
        self.weapon: Optional[Weapon] = None  # defined later

    

        
    # --- Composition helpers ---
    def equip_weapon(self, weapon: "Weapon") -> None:
        """Give this character a weapon to use for bonus damage."""
        self.weapon = weapon
    
    def _weapon_bonus(self) -> int:
        return self.weapon.damage_bonus if self.weapon else 0
        
    def attack(self, target: "Character") -> None:
        """
        Basic attack method that all characters can use.
        Damage is based on strength + any weapon bonus.
        """
        damage = max(0, self.strength + self._weapon_bonus())
        print(f"{self.name} hits {target.name} for {damage} damage.")
        target.take_damage(damage)
    def take_damage(self, damage: int) -> None:
        """
        Reduces this character's health by the damage amount.
        Health never goes below 0.
        """
        self.health = max(0, self.health - int(damage))
        print(f"{self.name} takes {int(damage)} damage (health: {self.health}).")
        
    def display_stats(self) -> None:
        """Prints the character's current stats in a nice format."""
        print(f"[{self.__class__.__name__}] {self.name} | HP: {self.health} | STR: {self.strength} | MAG: {self.magic}")

class Player(Character):
    """
    Base class for player characters.
    Inherits from Character and adds player-specific features.
    """
    
    def __init__(self, name: str, character_class: str, health: int, strength: int, magic: int):
        """
        Initialize a player character.
        Calls parent constructor and adds player-specific attributes.
        """
        super().__init__(name, health, strength, magic)
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        
    def gain_experience(self, amount: int) -> None:
        self.experience += int(amount)
        
    def display_stats(self) -> None:
        """
        Override the parent's display_stats to show additional player info.
        Shows everything the parent shows PLUS player-specific info.
        """
        super().display_stats()
        print(f"  Class: {self.character_class} | LVL: {self.level} | EXP: {self.experience}")

class Warrior(Player):
    """
    Warrior class - strong physical fighter.
    Inherits from Player.
    """
    
    def __init__(self, name: str):
        """
        Create a warrior with appropriate stats.
        Warriors: high health, high strength, low magic
        """
        super().__init__(name, "Warrior", health=120, strength=15, magic=5)
        
    def attack(self, target: Character) -> None:
        """
        Warrior-specific attack: extra physical damage.
        """
        bonus = 5
        damage = max(0, self.strength + bonus + self._weapon_bonus())
        print(f"{self.name} swings mightily for {damage} damage!")
        target.take_damage(damage)
        
    def power_strike(self, target: Character) -> None:
        """Special warrior ability - powerful attack that does extra damage."""
        damage = max(0, (self.strength * 2) + 10 + self._weapon_bonus())
        print(f"{self.name} uses Power Strike for {damage} damage!")
        target.take_damage(damage)

class Mage(Player):
    """
    Mage class - magical spellcaster.
    Inherits from Player.
    """
    
    def __init__(self, name: str):
        """
        Create a mage with appropriate stats.
        Mages: low health, low strength, high magic
        """
        super().__init__(name, "Mage", health=80, strength=8, magic=20)
        
    def attack(self, target: Character) -> None:
        """
        Mage attack: uses magic for damage instead of strength.
        """
        base = self.magic
        damage = max(0, base + 3 + self._weapon_bonus())
        print(f"{self.name} casts a magic bolt for {damage} damage!")
        target.take_damage(damage)
        
    def fireball(self, target: Character) -> None:
        """Special mage ability - powerful magical attack."""
        damage = max(0, (self.magic * 2) + 10 + self._weapon_bonus())
        print(f"{self.name} hurls a Fireball for {damage} damage!")
        target.take_damage(damage)

class Rogue(Player):
    """
    Rogue class - quick and sneaky fighter.
    Inherits from Player.
    """
    
    def __init__(self, name: str):
        """
        Create a rogue with appropriate stats.
        Rogues: medium health, medium strength, medium magic
        """
        super().__init__(name, "Rogue", health=90, strength=12, magic=10)
        
    def attack(self, target: Character) -> None:
        """
        Rogue attack: chance for a critical hit (double damage).
        30% crit chance using random.randint(1,10) <= 3.
        """
        base = self.strength + 2 + self._weapon_bonus()
        crit = random.randint(1, 10) <= 3
        damage = base * 2 if crit else base
        if crit:
            print(f"{self.name} lands a CRITICAL strike for {damage} damage!")
        else:
            print(f"{self.name} strikes for {damage} damage.")
        target.take_damage(damage)
        
    def sneak_attack(self, target: Character) -> None:
        """Special rogue ability - guaranteed critical hit."""
        base = self.strength + 2 + self._weapon_bonus()
        damage = base * 2
        print(f"{self.name} performs a Sneak Attack for {damage} damage!")
        target.take_damage(damage)

class Weapon:
    """
    Weapon class to demonstrate composition.
    Characters can HAVE weapons (composition, not inheritance).
    """
    
    def __init__(self, name: str, damage_bonus: int):
        """Create a weapon with a name and damage bonus."""
        self.name = name
        self.damage_bonus = int(damage_bonus)
        
    def display_info(self) -> None:
        """Display information about this weapon."""
        print(f"Weapon: {self.name} | Damage Bonus: +{self.damage_bonus}")

# ============================================================================
# MAIN PROGRAM FOR TESTING (YOU CAN MODIFY THIS FOR TESTING)
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER ABILITIES SHOWCASE ===")
    print("Testing inheritance, polymorphism, and method overriding")
    print("=" * 50)
    
    # Create one of each character type
    warrior = Warrior("Mike Tyson")
    mage = Mage("Muhammad Ali")
    rogue = Rogue("Floyd Mayweather")
    
    # Display their stats
    print("\n📊 Character Stats:")
    warrior.display_stats()
    mage.display_stats()
    rogue.display_stats()
    
    # Test polymorphism - same method call, different behavior
    print("\n⚔️ Testing Polymorphism (same attack method, different behavior):")
    dummy = Character("Target Dummy", 100, 0, 0)
    for c in [warrior, mage, rogue]:
        print(f"\n{c.name} attacks the dummy:")
        c.attack(dummy)
        dummy.health = 100  # reset
    
    # Test special abilities
    print("\n✨ Testing Special Abilities:")
    t1 = Character("Enemy1", 50, 0, 0)
    t2 = Character("Enemy2", 50, 0, 0)
    t3 = Character("Enemy3", 50, 0, 0)
    warrior.power_strike(t1)
    mage.fireball(t2)
    rogue.sneak_attack(t3)
    
    # Test composition with weapons
    print("\n🗡️ Testing Weapon Composition:")
    sword = Weapon("Iron Sword", 10)
    staff = Weapon("Magic Staff", 15)
    dagger = Weapon("Steel Dagger", 8)
    sword.display_info()
    staff.display_info()
    dagger.display_info()
    
    # Equip and attack with weapons
    warrior.equip_weapon(sword)
    mage.equip_weapon(staff)
    rogue.equip_weapon(dagger)
    print("\nWith weapons equipped:")
    for c in [warrior, mage, rogue]:
        print(f"\n{c.name} attacks the dummy with a weapon:")
        c.attack(dummy)
        dummy.health = 100
    
    # Test the battle system
    print("\n⚔️ Testing Battle System:")
    battle = SimpleBattle(warrior, mage)
    battle.fight()
    
    print("\n✅ Testing complete!")

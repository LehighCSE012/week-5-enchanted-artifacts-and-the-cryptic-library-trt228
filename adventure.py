# Your code goes import random

def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles discovering an enchanted artifact."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found {artifact_name.replace('_', ' ').title()}: {artifact['description']}")
        
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increases by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack increases by {artifact['power']}!")
        
        del artifacts[artifact_name]  # Remove artifact so it cannot be found again
    else:
        print("You found nothing of interest.")
    
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Handles discovering a unique clue."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)  # Using add() to store unique clues
        print(f"You discovered a new clue: {new_clue}")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Handles the player entering the dungeon rooms."""
    for room in dungeon_rooms:
        room_name, item, challenge_type, challenge_outcome = room
        print(f"\nYou enter: {room_name}")
        
        if room_name == "Cryptic Library":
            print("A vast library filled with ancient, cryptic texts.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            discovered_clues = random.sample(possible_clues, 2)
            for clue in discovered_clues:
                clues = find_clue(clues, clue)
            
            if "staff_of_wisdom" in inventory:
                print("Your staff of wisdom reveals the meaning behind the clues. You may bypass a puzzle challenge later!")
                inventory.append("bypass_puzzle")
    
    return player_stats, inventory, clues

def combat_encounter(player_stats, monster_health, has_treasure):
    """Handles combat encounter."""
    print("A monster appears!")
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health -= player_stats['attack']
        print(f"You attack! Monster's health: {monster_health}")
        
        if monster_health > 0:
            player_stats['health'] -= 10  # Monster attacks back
            print(f"Monster attacks! Your health: {player_stats['health']}")
    
    if player_stats['health'] > 0:
        print("You defeated the monster!")
        return has_treasure
    else:
        print("You have fallen in battle.")
        return None

def main():
    """Main game loop."""
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    
    artifacts = {
        "amulet_of_vitality": {"description": "Glowing amulet, life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "Powerful ring, attack boost.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "Staff of wisdom, ancient.", "power": 5, "effect": "solves puzzles"}
    }
    
    has_treasure = random.choice([True, False])
    
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            inventory.append("treasure")
        
        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
        
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
            
            print("\n--- Game End ---")
            print(f"Final Health: {player_stats['health']}, Attack: {player_stats['attack']}")
            print("Inventory:", inventory)
            print("Clues:", clues if clues else "No clues.")

if __name__ == "__main__":
    main()

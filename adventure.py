import random
import subprocess

def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles artifact discovery and applies effects."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found: {artifact['description']}")

        if artifact["effect"] == "increases health":
            player_stats["health"] += artifact["power"]
        elif artifact["effect"] == "enhances attack":
            player_stats["attack"] += artifact["power"]

        print(f"Your {artifact['effect']} increased by {artifact['power']}!")

        del artifacts[artifact_name]  # Remove the artifact after use
    else:
        print("You found nothing of interest.")

    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Handles finding clues in the cryptic library."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")

    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Handles dungeon navigation and interactions."""
    for room in dungeon_rooms:
        if len(room) != 4 or not isinstance(room[3], tuple):
            raise TypeError(f"Invalid room structure: {room}")

        room_name, item, challenge_type, challenge_outcome = room

        print(f"You have entered: {room_name}")

        if item:
            inventory.append(item)
            print(f"You found a {item} and added it to your inventory!")

        if challenge_type == "library":
            print("A vast library filled with ancient, cryptic texts.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]

            found_clues = random.sample(possible_clues, 2)
            for clue in found_clues:
                clues = find_clue(clues, clue)

            if "staff_of_wisdom" in artifacts:
                print("You understand the meaning of the clues and can bypass a puzzle challenge!")

    return player_stats, inventory, clues

def acquire_item(inventory, item):
    """Adds an item to inventory."""
    inventory.append(item)
    print(f"You acquired: {item}")
    return inventory

def display_inventory(inventory):
    """Displays the current inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Inventory:", inventory)

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
    inventory = []
    clues = set()

    artifacts = {
        "amulet_of_vitality": {"description": "Glowing amulet, life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "Powerful ring, attack boost.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "Staff of wisdom, ancient.", "power": 5, "effect": "solves puzzles"}
    }

    if random.random() < 0.3:
        artifact_keys = list(artifacts.keys())
        if artifact_keys:
            artifact_name = random.choice(artifact_keys)
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)

    if player_stats["health"] > 0:
        player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)

    print("\n--- Game End ---")
    print(f"Final Health: {player_stats['health']}, Attack: {player_stats['attack']}")
    print("Final Inventory:", inventory)
    print("Clues:", clues)

if __name__ == "__main__":
    main()

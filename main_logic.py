import enum
import math
from typing import Dict, Tuple


class Skill(enum.Enum):
    SWORD = 0
    SHIELD = 1
    SPELL = 2


# Matchup table (rock-paper-scissors style)
WIN_TABLE = {
    Skill.SWORD: Skill.SPELL,
    Skill.SPELL: Skill.SHIELD,
    Skill.SHIELD: Skill.SWORD
}


class Character:
    def __init__(self, hp, shield, skills, max_shield=None):
        self.hp = hp
        self.shield = shield
        self.max_shield = max_shield if max_shield is not None else shield
        self.skills = skills  # {Skill: {"atk":x, "def":y, "stamina":z}}


def judge(my_skill: Skill, enemy_skill: Skill) -> int:
    if my_skill == enemy_skill:
        return 0
    if WIN_TABLE[my_skill] == enemy_skill:
        return +1
    return -1


def apply_damage(target: Character, dmg: int):
    """Apply damage to shield first, then HP"""
    if dmg <= 0:
        return
    if target.shield >= dmg:
        target.shield -= dmg
    else:
        remain = dmg - target.shield
        target.shield = 0
        target.hp -= remain


def calculate_ev(my_char: Character, enemy_char: Character, my_skill: Skill) -> float:
    # Cannot select if stamina is 0
    if my_char.skills[my_skill]["stamina"] <= 0:
        return -math.inf

    enemy_available = [s for s in Skill if enemy_char.skills[s]["stamina"] > 0]
    if not enemy_available:
        return 0

    total_ev = 0

    for es in enemy_available:
        win_result = judge(my_skill, es)

        # Copy state for simulation
        me = Character(my_char.hp, my_char.shield, my_char.skills, my_char.max_shield)
        enemy = Character(enemy_char.hp, enemy_char.shield, enemy_char.skills, enemy_char.max_shield)

        my_atk = me.skills[my_skill]["atk"]
        my_def = me.skills[my_skill]["def"]
        enemy_atk = enemy.skills[es]["atk"]
        enemy_def = enemy.skills[es]["def"]

        # --- Matchup-based application rules ---
        if win_result == 1:
            # I win: Only my attack and shield apply
            apply_damage(enemy, my_atk)
            me.shield = min(me.shield + my_def, me.max_shield)
        elif win_result == -1:
            # I lose: Only enemy attack and shield apply
            apply_damage(me, enemy_atk)
            enemy.shield = min(enemy.shield + enemy_def, enemy.max_shield)
        else:
            # Draw: Both attacks and shields apply
            apply_damage(enemy, my_atk)
            apply_damage(me, enemy_atk)
            me.shield = min(me.shield + my_def, me.max_shield)
            enemy.shield = min(enemy.shield + enemy_def, enemy.max_shield)

        # Expected value = (Enemy HP + Shield lost) - (My HP + Shield lost)
        enemy_hp_lost = enemy_char.hp - enemy.hp
        enemy_shield_lost = enemy_char.shield - enemy.shield
        my_hp_lost = my_char.hp - me.hp
        my_shield_lost = my_char.shield - me.shield
        
        net_value = (enemy_hp_lost + enemy_shield_lost) - (my_hp_lost + my_shield_lost)

        total_ev += net_value / len(enemy_available)

    return total_ev


def best_action(my_char: Character, enemy_char: Character):
    results = {}
    for s in Skill:
        results[s] = calculate_ev(my_char, enemy_char, s)

    best = max(results, key=results.get)
    return best, results[best]
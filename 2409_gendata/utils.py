# utils.py

import random

def weighted_choice(choices_dict):
    total = sum(choices_dict.values())
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in choices_dict.items():
        if upto + weight >= r:
            return choice
        upto += weight
    # Should not reach here
    return None
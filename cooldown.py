
from time import time
from config import COOLDOWN

cooldowns = {}

# Cooldown check for a user
def is_on_cooldown(user_id):
    now = time()
    return user_id in cooldowns and now - cooldowns[user_id] < COOLDOWN

def set_cooldown(user_id):
    cooldowns[user_id] = time()
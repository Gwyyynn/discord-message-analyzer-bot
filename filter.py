import re
from config import MAX_MESSAGE_LENGTH

URL_RE = re.compile(r'https?://\S+|discord\.gg/\S+', re.IGNORECASE)

# Check if a message is suitable for analysis
# Filters out:
# - empty and short messages
# - links
# - overly long texts
# - messages without letters
def is_good_message(text: str) -> bool:
    if not text:
        return False

    if len(text) < 5:
        return False

    if URL_RE.search(text):
        return False
    
    if len(text) > MAX_MESSAGE_LENGTH:
        return False

    # если нет букв вообще
    if not re.search(r'[a-zA-Zа-яА-Я]', text):
        return False

    return True

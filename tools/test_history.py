
from bot.utils import file_ops

print("--- Loading History ---")
history = file_ops.load_recent_history()
print(history)
print("-----------------------")

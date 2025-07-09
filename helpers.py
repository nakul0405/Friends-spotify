import time

def time_player(initial_timestamp: int):
    minutes = abs(int(time.time()) - initial_timestamp // 1000) // 60
    if minutes > 24 * 60:
        return f"{minutes // (24 * 60)}d", False
    elif minutes > 60:
        return f"{minutes // 60}h", False
    elif minutes > 5:
        return f"{minutes}m", False
    else:
        return "now", True

# services/event_store.py

EVENTS = []

def add_event(event: dict):
    """
    Store latest security events (FIFO buffer)
    """
    EVENTS.append(event)
    if len(EVENTS) > 50:
        EVENTS.pop(0)

def get_events():
    """
    Return all stored events
    """
    return EVENTS

ALLOWED_TRANSITIONS = {
    'open': ['assigned'],
    'assigned': ['in_progress'],
    'in_progress': ['closed'],
    'closed': []
}

class TransitionError(Exception):
    pass

def validate_transition(current: str, target: str):
    allowed = get_allowed_moves(current)
    if target not in allowed:
        raise TransitionError(f"Invalid transition from {current} to {target}")

def get_allowed_moves(current: str) -> list[str]:
    return ALLOWED_TRANSITIONS.get(current, [])

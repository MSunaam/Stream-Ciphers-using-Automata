class A51Statistics:
    def __init__(self):
        self._state_transitions = {}  # Renamed from state_transitions
        self._state_frequency = {}  # Renamed from state_frequency

    def record_transition(self, from_state: str, to_state: str):
        # Convert states to strings if they aren't already
        from_state_str = str(from_state)
        to_state_str = str(to_state)

        if from_state_str not in self._state_transitions:
            self._state_transitions[from_state_str] = []
        self._state_transitions[from_state_str].append(to_state_str)

        # Update frequencies
        self._state_frequency[from_state_str] = (
            self._state_frequency.get(from_state_str, 0) + 1
        )
        self._state_frequency[to_state_str] = (
            self._state_frequency.get(to_state_str, 0) + 1
        )

    def state_transitions(self) -> dict:
        return self._state_transitions

    def get_frequency(self) -> dict:
        return self._state_frequency

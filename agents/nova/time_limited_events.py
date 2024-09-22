import time
from typing import Dict, Any, List, Callable

class TimeLimitedEvent:
    def __init__(self, event_id: str, description: str, duration: int, start_action: Callable, end_action: Callable):
        self.event_id = event_id
        self.description = description
        self.duration = duration
        self.start_time = None
        self.end_time = None
        self.start_action = start_action
        self.end_action = end_action
        self.is_active = False

    def start(self):
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration
        self.is_active = True
        self.start_action()

    def end(self):
        self.is_active = False
        self.end_action()

    def time_remaining(self) -> int:
        if not self.is_active:
            return 0
        remaining = int(self.end_time - time.time())
        return max(0, remaining)

class TimeLimitedEventSystem:
    def __init__(self):
        self.events: Dict[str, TimeLimitedEvent] = {}
        self.active_events: List[str] = []

    def create_event(self, event_id: str, description: str, duration: int, start_action: Callable, end_action: Callable):
        event = TimeLimitedEvent(event_id, description, duration, start_action, end_action)
        self.events[event_id] = event

    def start_event(self, event_id: str):
        if event_id in self.events and event_id not in self.active_events:
            self.events[event_id].start()
            self.active_events.append(event_id)

    def end_event(self, event_id: str):
        if event_id in self.active_events:
            self.events[event_id].end()
            self.active_events.remove(event_id)

    def update(self):
        current_time = time.time()
        for event_id in self.active_events[:]:
            event = self.events[event_id]
            if current_time >= event.end_time:
                self.end_event(event_id)

    def get_active_events(self) -> List[Dict[str, Any]]:
        return [
            {
                "event_id": self.events[event_id].event_id,
                "description": self.events[event_id].description,
                "time_remaining": self.events[event_id].time_remaining()
            }
            for event_id in self.active_events
        ]

    def get_event_status(self, event_id: str) -> Dict[str, Any]:
        if event_id in self.events:
            event = self.events[event_id]
            return {
                "event_id": event.event_id,
                "description": event.description,
                "is_active": event.is_active,
                "time_remaining": event.time_remaining()
            }
        return {}

# Example usage:
# def start_quantum_storm():
#     print("A quantum storm has begun in the metaverse!")

# def end_quantum_storm():
#     print("The quantum storm has dissipated.")

# tles = TimeLimitedEventSystem()
# tles.create_event("quantum_storm", "A reality-bending quantum storm sweeps through the metaverse", 300, start_quantum_storm, end_quantum_storm)
# tles.start_event("quantum_storm")

# # Simulate time passing
# import time
# for _ in range(30):
#     time.sleep(1)
#     tles.update()
#     print(tles.get_event_status("quantum_storm"))

# print(tles.get_active_events())

import hashlib
import time
from typing import Dict, Any, List

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class BlockchainNarrative:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.pending_narrative_events: List[Dict[str, Any]] = []

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), {"narrative_event": "The story begins"}, "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_narrative_event(self, event: Dict[str, Any]):
        self.pending_narrative_events.append(event)

    def mine_pending_events(self) -> Block:
        if not self.pending_narrative_events:
            return None

        last_block = self.get_latest_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            data={"narrative_events": self.pending_narrative_events},
            previous_hash=last_block.hash
        )

        self.chain.append(new_block)
        self.pending_narrative_events = []

        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_narrative_history(self) -> List[Dict[str, Any]]:
        history = []
        for block in self.chain:
            if "narrative_events" in block.data:
                for event in block.data["narrative_events"]:
                    history.append({
                        "timestamp": block.timestamp,
                        "event": event
                    })
            elif "narrative_event" in block.data:
                history.append({
                    "timestamp": block.timestamp,
                    "event": block.data["narrative_event"]
                })
        return history

    def verify_narrative_event(self, event_data: Dict[str, Any]) -> bool:
        for block in self.chain:
            if "narrative_events" in block.data:
                if event_data in block.data["narrative_events"]:
                    return True
            elif "narrative_event" in block.data:
                if event_data == block.data["narrative_event"]:
                    return True
        return False

    def create_achievement(self, user_id: str, achievement_name: str, description: str) -> Dict[str, Any]:
        achievement = {
            "user_id": user_id,
            "achievement_name": achievement_name,
            "description": description,
            "timestamp": time.time()
        }
        self.add_narrative_event({"type": "achievement", "data": achievement})
        self.mine_pending_events()
        return achievement

    def verify_achievement(self, user_id: str, achievement_name: str) -> bool:
        for block in self.chain:
            if "narrative_events" in block.data:
                for event in block.data["narrative_events"]:
                    if event["type"] == "achievement" and \
                       event["data"]["user_id"] == user_id and \
                       event["data"]["achievement_name"] == achievement_name:
                        return True
        return False

# Example usage:
# bn = BlockchainNarrative()
# bn.add_narrative_event({"type": "character_action", "data": "Nova explores the quantum realm"})
# bn.add_narrative_event({"type": "world_event", "data": "A new digital dimension emerges"})
# bn.mine_pending_events()
# bn.create_achievement("user123", "Quantum Explorer", "Visited 10 unique quantum realms")
# print(bn.get_narrative_history())
# print(bn.verify_achievement("user123", "Quantum Explorer"))
# print(bn.is_chain_valid())

import hashlib
from typing import Dict, List

class UBCHNode:
    def __init__(self, node_id: str, compute_power: float):
        self.node_id = node_id
        self.compute_power = compute_power
        self.tasks = []

    def add_task(self, task: Dict):
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]

class UBCHNetwork:
    def __init__(self):
        self.nodes: Dict[str, UBCHNode] = {}
        self.users: Dict[str, float] = {}  # user_id: compute_allocation

    def add_node(self, node: UBCHNode):
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str):
        if node_id in self.nodes:
            del self.nodes[node_id]

    def register_user(self, user_id: str, initial_allocation: float = 1.0):
        self.users[user_id] = initial_allocation

    def allocate_task(self, user_id: str, task: Dict) -> bool:
        if user_id not in self.users or self.users[user_id] < task['compute_required']:
            return False

        available_nodes = [node for node in self.nodes.values() if node.compute_power >= task['compute_required']]
        if not available_nodes:
            return False

        # Simple allocation strategy: choose the first available node
        chosen_node = available_nodes[0]
        chosen_node.add_task(task)
        self.users[user_id] -= task['compute_required']
        return True

    def complete_task(self, node_id: str, task_id: str, user_id: str):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            task = next((t for t in node.tasks if t['id'] == task_id), None)
            if task:
                node.remove_task(task_id)
                self.users[user_id] += task['compute_required']

def main():
    network = UBCHNetwork()

    # Add some nodes to the network
    for i in range(5):
        node_id = hashlib.sha256(f"node_{i}".encode()).hexdigest()[:8]
        node = UBCHNode(node_id, compute_power=10.0)
        network.add_node(node)

    # Register some users
    for i in range(10):
        user_id = hashlib.sha256(f"user_{i}".encode()).hexdigest()[:8]
        network.register_user(user_id)

    # Simulate task allocation
    for i in range(20):
        user_id = list(network.users.keys())[i % len(network.users)]
        task = {
            'id': hashlib.sha256(f"task_{i}".encode()).hexdigest()[:8],
            'compute_required': 0.5
        }
        success = network.allocate_task(user_id, task)
        print(f"Task allocation for user {user_id}: {'Successful' if success else 'Failed'}")

    print("\nFinal state:")
    for user_id, allocation in network.users.items():
        print(f"User {user_id}: Remaining allocation = {allocation}")

if __name__ == "__main__":
    main()

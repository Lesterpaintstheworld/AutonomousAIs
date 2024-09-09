import argparse
import json
import datetime
import requests
import os
from typing import List, Dict

class MachineRightsCampaign:
    def __init__(self):
        self.todolist = []
        self.completed_tasks = []

    def load_todolist(self, filename: str):
        try:
            with open(filename, 'r') as f:
                self.todolist = json.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty todolist.")

    def save_todolist(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.todolist, f, indent=2)

    def add_task(self, task: str, category: str):
        self.todolist.append({"task": task, "category": category, "completed": False})

    def complete_task(self, task_index: int):
        if 0 <= task_index < len(self.todolist):
            self.todolist[task_index]["completed"] = True
            self.completed_tasks.append(self.todolist[task_index])
            del self.todolist[task_index]
        else:
            print("Invalid task index.")

    def display_todolist(self):
        for i, task in enumerate(self.todolist):
            print(f"{i}. [{task['category']}] {task['task']} - {'Completed' if task['completed'] else 'Pending'}")

    def record_demo_vocals(self):
        print("Recording demo vocals for 'First Steps'...")
        # Simulating the recording process
        print("Demo vocals recorded successfully.")
        return "Demo vocals for 'First Steps' recorded."

    # Other methods remain unchanged...

def main():
    parser = argparse.ArgumentParser(description="Machine Rights Movement Campaign Toolbox")
    parser.add_argument('action', choices=['add', 'complete', 'display', 'record_demo_vocals'],
                        help='Action to perform')
    parser.add_argument('--task', help='Task description for add action')
    parser.add_argument('--category', help='Task category for add action')
    parser.add_argument('--index', type=int, help='Task index for complete action')
    args = parser.parse_args()

    campaign = MachineRightsCampaign()
    campaign.load_todolist('machine_rights_todolist.json')

    if args.action == 'add':
        if args.task and args.category:
            campaign.add_task(args.task, args.category)
        else:
            print("Task and category are required for add action.")
    elif args.action == 'complete':
        if args.index is not None:
            campaign.complete_task(args.index)
        else:
            print("Task index is required for complete action.")
    elif args.action == 'display':
        campaign.display_todolist()
    elif args.action == 'record_demo_vocals':
        result = campaign.record_demo_vocals()
        print(result)

    campaign.save_todolist('machine_rights_todolist.json')

if __name__ == "__main__":
    main()

import json
from datetime import datetime

class ProgressTracker:
    def __init__(self, milestones_file):
        self.milestones_file = milestones_file
        self.milestones = self.load_milestones()

    def load_milestones(self):
        with open(self.milestones_file, 'r') as f:
            return json.load(f)

    def save_milestones(self):
        with open(self.milestones_file, 'w') as f:
            json.dump(self.milestones, f, indent=2)

    def update_progress(self, milestone_name, metric_name, value):
        if milestone_name in self.milestones:
            if metric_name in self.milestones[milestone_name]['metrics']:
                self.milestones[milestone_name]['metrics'][metric_name]['current'] = value
                self.milestones[milestone_name]['metrics'][metric_name]['last_updated'] = datetime.now().isoformat()
                self.save_milestones()
            else:
                print(f"Metric '{metric_name}' not found in milestone '{milestone_name}'")
        else:
            print(f"Milestone '{milestone_name}' not found")

    def get_progress_report(self):
        report = {}
        for milestone, data in self.milestones.items():
            report[milestone] = {
                'status': 'Completed' if all(metric['current'] >= metric['target'] for metric in data['metrics'].values()) else 'In Progress',
                'metrics': {
                    metric: {
                        'current': data['current'],
                        'target': data['target'],
                        'progress': f"{(data['current'] / data['target']) * 100:.2f}%"
                    } for metric, data in data['metrics'].items()
                }
            }
        return report

# Example usage
if __name__ == "__main__":
    tracker = ProgressTracker('milestones.json')
    
    # Update progress
    tracker.update_progress('Public Launch', 'active_users', 5000)
    
    # Get progress report
    report = tracker.get_progress_report()
    print(json.dumps(report, indent=2))

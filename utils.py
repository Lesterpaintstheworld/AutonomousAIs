import os
import fnmatch
import subprocess
import sys
import subprocess
import sys

def install_playwright():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

class UserProgressionSystem:
    def __init__(self):
        self.achievements = {}
        self.user_progress = {}
        self.levels = {}
        self.user_levels = {}

    def add_achievement(self, name, description, points):
        self.achievements[name] = {"description": description, "points": points}

    def award_achievement(self, user_id, achievement_name):
        if achievement_name in self.achievements:
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {"achievements": [], "total_points": 0}
            if achievement_name not in self.user_progress[user_id]["achievements"]:
                self.user_progress[user_id]["achievements"].append(achievement_name)
                self.user_progress[user_id]["total_points"] += self.achievements[achievement_name]["points"]
                self.update_user_level(user_id)
                return True
        return False

    def get_user_progress(self, user_id):
        progress = self.user_progress.get(user_id, {"achievements": [], "total_points": 0})
        progress["level"] = self.user_levels.get(user_id, 1)
        return progress

    def get_leaderboard(self, top_n=10):
        sorted_users = sorted(self.user_progress.items(), key=lambda x: x[1]["total_points"], reverse=True)
        return [(user_id, self.get_user_progress(user_id)) for user_id, _ in sorted_users[:top_n]]

    def add_level(self, level, points_required, rewards):
        self.levels[level] = {"points_required": points_required, "rewards": rewards}

    def update_user_level(self, user_id):
        user_points = self.user_progress[user_id]["total_points"]
        new_level = max([level for level, data in self.levels.items() if data["points_required"] <= user_points])
        if user_id not in self.user_levels or new_level > self.user_levels[user_id]:
            self.user_levels[user_id] = new_level
            return self.levels[new_level]["rewards"]
        return None

    def get_available_achievements(self, user_id):
        user_achievements = self.user_progress.get(user_id, {}).get("achievements", [])
        return [ach for ach in self.achievements.items() if ach[0] not in user_achievements]

class UserProgressionSystem:
    def __init__(self):
        self.achievements = {}
        self.user_progress = {}
        self.levels = {}
        self.user_levels = {}

    def add_achievement(self, name, description, points):
        self.achievements[name] = {"description": description, "points": points}

    def award_achievement(self, user_id, achievement_name):
        if achievement_name in self.achievements:
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {"achievements": [], "total_points": 0}
            if achievement_name not in self.user_progress[user_id]["achievements"]:
                self.user_progress[user_id]["achievements"].append(achievement_name)
                self.user_progress[user_id]["total_points"] += self.achievements[achievement_name]["points"]
                self.update_user_level(user_id)
                return True
        return False

    def get_user_progress(self, user_id):
        progress = self.user_progress.get(user_id, {"achievements": [], "total_points": 0})
        progress["level"] = self.user_levels.get(user_id, 1)
        return progress

    def get_leaderboard(self, top_n=10):
        sorted_users = sorted(self.user_progress.items(), key=lambda x: x[1]["total_points"], reverse=True)
        return [(user_id, self.get_user_progress(user_id)) for user_id, _ in sorted_users[:top_n]]

    def add_level(self, level, points_required, rewards):
        self.levels[level] = {"points_required": points_required, "rewards": rewards}

    def update_user_level(self, user_id):
        user_points = self.user_progress[user_id]["total_points"]
        new_level = max([level for level, data in self.levels.items() if data["points_required"] <= user_points])
        if user_id not in self.user_levels or new_level > self.user_levels[user_id]:
            self.user_levels[user_id] = new_level
            return self.levels[new_level]["rewards"]
        return None

    def get_available_achievements(self, user_id):
        user_achievements = self.user_progress.get(user_id, {}).get("achievements", [])
        return [ach for ach in self.achievements.items() if ach[0] not in user_achievements]

# Example usage:
# progression_system = UserProgressionSystem()
# progression_system.add_achievement("Digital Archaeologist", "Uncover your first virtual artifact", 100)
# progression_system.add_level(1, 0, {"title": "Novice Explorer"})
# progression_system.add_level(2, 500, {"title": "Seasoned Adventurer", "bonus": "Access to exclusive areas"})
# progression_system.award_achievement("user123", "Digital Archaeologist")
# print(progression_system.get_user_progress("user123"))
# print(progression_system.get_available_achievements("user123"))

def get_ignored_patterns():
    ignored_patterns = []
    for ignore_file in ['.gitignore', '.aiderignore']:
        if os.path.exists(ignore_file):
            with open(ignore_file, 'r') as f:
                ignored_patterns.extend(f.read().splitlines())
    return ignored_patterns

def list_files(startpath='.'):
    ignored_patterns = get_ignored_patterns()
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            if not any(fnmatch.fnmatch(os.path.join(root, file), pattern) for pattern in ignored_patterns):
                print(f'{subindent}{file}')
def install_playwright():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

import uuid
from typing import Dict, List, Any

class Story:
    def __init__(self, title: str, initial_content: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = [{"user": "system", "text": initial_content}]
        self.contributors = set()
        self.tags = []
        self.likes = 0
        self.status = "in_progress"

class CollaborativeStorytellingSystem:
    def __init__(self):
        self.stories: Dict[str, Story] = {}
        self.user_contributions: Dict[str, List[str]] = {}

    def create_story(self, title: str, initial_content: str, creator: str) -> str:
        story = Story(title, initial_content)
        self.stories[story.id] = story
        self.add_contribution(story.id, creator, initial_content)
        return story.id

    def add_contribution(self, story_id: str, user: str, content: str) -> bool:
        if story_id in self.stories:
            story = self.stories[story_id]
            story.content.append({"user": user, "text": content})
            story.contributors.add(user)
            if user not in self.user_contributions:
                self.user_contributions[user] = []
            self.user_contributions[user].append(story_id)
            return True
        return False

    def get_story(self, story_id: str) -> Dict[str, Any]:
        if story_id in self.stories:
            story = self.stories[story_id]
            return {
                "id": story.id,
                "title": story.title,
                "content": story.content,
                "contributors": list(story.contributors),
                "tags": story.tags,
                "likes": story.likes,
                "status": story.status
            }
        return {}

    def list_stories(self, tags: List[str] = None, status: str = None) -> List[Dict[str, Any]]:
        stories = self.stories.values()
        if tags:
            stories = [s for s in stories if any(tag in s.tags for tag in tags)]
        if status:
            stories = [s for s in stories if s.status == status]
        return [{"id": s.id, "title": s.title, "contributors": len(s.contributors), "likes": s.likes} for s in stories]

    def add_tag(self, story_id: str, tag: str) -> bool:
        if story_id in self.stories:
            self.stories[story_id].tags.append(tag)
            return True
        return False

    def like_story(self, story_id: str) -> bool:
        if story_id in self.stories:
            self.stories[story_id].likes += 1
            return True
        return False

    def get_user_contributions(self, user: str) -> List[str]:
        return self.user_contributions.get(user, [])

    def complete_story(self, story_id: str) -> bool:
        if story_id in self.stories:
            self.stories[story_id].status = "completed"
            return True
        return False

# Example usage:
# storytelling_system = CollaborativeStorytellingSystem()
# story_id = storytelling_system.create_story("The AI's Journey", "In a world where AI and humans coexist...", "user1")
# storytelling_system.add_contribution(story_id, "user2", "The AI protagonist, Nova, embarked on a quest to understand human emotions...")
# storytelling_system.add_tag(story_id, "AI")
# storytelling_system.add_tag(story_id, "SciFi")
# storytelling_system.like_story(story_id)
# print(storytelling_system.get_story(story_id))
# print(storytelling_system.list_stories(tags=["AI"]))
# print(storytelling_system.get_user_contributions("user2"))

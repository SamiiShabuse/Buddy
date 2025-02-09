import uuid
import datetime
import json
from typing import Optional, Dict, Any, ClassVar

# Predefined categories
USER_CATEGORIES = [
    "Work", "School", "Personal", "Health", "Finance", "Social",
    "Errands", "Home", "Travel", "Other"
]

# Predefined task types
TASK_TYPES = [
    "basic_task",            # Static to-do
    "reminder",              # Notification-based
    "recurring_task",        # Repeats on schedule
    "deadline_based_task",   # Strict deadline
    "ai_suggested_task",     # AI-generated or adjusted
    "auto_rescheduled_task"  # Moves itself if missed
]

class Task:
    def __init__(self, 
                 name: str, 
                 description: Optional[str] = None,
                 user_category: str = "Other",
                 task_type: str = "basic_task",
                 source: Optional[str] = "Manual",
                 datetime_str: Optional[str] = None,
                 ai_generated: bool = False):
        if user_category not in USER_CATEGORIES:
            raise ValueError(f"Invalid user_category: {user_category}")
        if task_type not in TASK_TYPES:
            raise ValueError(f"Invalid task_type: {task_type}")

        self.id = str(uuid.uuid4())  # Unique task ID
        self.name = name
        self.description = description or ""
        self.user_category = user_category
        self.task_type = task_type
        self.source = source
        self.ai_generated = ai_generated
        self.trigger_time = self.parse_datetime(datetime_str)
        self.status = "Pending"  # Default status
        self.execution_details = self.get_execution_details()

    def parse_datetime(self, datetime_str: Optional[str]):
        """Parse datetime from string if provided."""
        if datetime_str:
            try:
                return datetime.datetime.fromisoformat(datetime_str)
            except ValueError:
                raise ValueError("Invalid datetime format. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)")
        return None

    def get_execution_details(self) -> Dict[str, str]:
        """Determine execution details based on task type."""
        details = {"message": f"Task: {self.name}"}

        if self.task_type == "reminder":
            details.update({"notification_type": "push", "message": f"Reminder: {self.name}"})
        elif self.task_type == "deadline_based_task":
            details.update({"notification_type": "push", "message": f"Task due soon: {self.name}"})
        elif self.task_type == "recurring_task":
            details.update({"recurrence": "weekly", "message": f"Recurring Task: {self.name}"})
        elif self.task_type == "auto_rescheduled_task":
            details.update({"reschedule_if_missed": "true", "message": f"Rescheduled: {self.name}"})
        elif self.task_type == "ai_suggested_task":
            details.update({"ai_generated": "true", "message": f"AI suggests: {self.name}"})

        return details

    def mark_completed(self):
        """Mark the task as completed."""
        self.status = "Completed"

    def reschedule(self, new_datetime_str: str):
        """Reschedule a task."""
        self.trigger_time = self.parse_datetime(new_datetime_str)
        self.status = "Pending"

    # ✅ JSON Representation Method
    def to_json(self, as_string: bool = False) -> Any:
        """Convert the Task object to a JSON-compatible dictionary or JSON string."""
        task_dict = {
            "id": self.id,
            "name": self.name,
            "user_category": self.user_category,
            "task_type": self.task_type,
            "source": self.source,
            "trigger": {
                "type": "time-based" if self.trigger_time else "none",
                "datetime": self.trigger_time.isoformat() if self.trigger_time else None
            },
            "execution_details": self.execution_details,
            "editable_fields": ["trigger", "execution_details" , "name"],
            "status": self.status
        }
        return json.dumps(task_dict, indent=2) if as_string else task_dict

    # ✅ Deserialize JSON to Task Object
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Task":
        """Create a Task object from JSON data."""
        task = cls(
            name=data["name"],
            user_category=data.get("user_category", "Other"),
            task_type=data.get("task_type", "basic_task"),
            source=data.get("source", "Manual"),
            datetime_str=data.get("trigger", {}).get("datetime"),
            ai_generated=data.get("execution_details", {}).get("ai_generated", False)
        )
        task.id = data.get("id", str(uuid.uuid4()))
        task.status = data.get("status", "Pending")
        return task

    def __repr__(self):
        return f"<Task {self.name} [{self.user_category}] - {self.status}>"

    def __str__(self):
        return (
            f"Task ID: {self.id}\n"
            f"📝 {self.name}\n"
            f"📖 {self.description if self.description else 'No description'}\n"
            f"📂 Category: {self.user_category}\n"
            f"⚡ Type: {self.task_type.replace('_', ' ').title()}\n"
            f"📅 Due: {self.trigger_time.strftime('%Y-%m-%d %H:%M') if self.trigger_time else 'No set time'}\n"
            f"📌 Source: {self.source}\n"
            f"🚀 AI-Generated: {'Yes' if self.ai_generated else 'No'}\n"
            f"✅ Status: {self.status}"
        )

# Example Usage
if __name__ == "__main__":
    # Create a task
    task = Task(
        name="Submit Homework",
        description="Complete and upload math assignment by Friday.",
        user_category="School",
        task_type="deadline_based_task",
        source="Email",
        datetime_str="2025-02-02T18:00:00",
        ai_generated=True
    )

    # Serialize to JSON
    task_json = task.to_json(as_string=True)
    print(task_json)

    # Deserialize back to a Task object
    new_task = Task.from_json(json.loads(task_json))
    print(new_task)

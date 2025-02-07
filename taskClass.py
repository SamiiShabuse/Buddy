import uuid
import datetime
from typing import Optional, Dict

# Predefined categories
USER_CATEGORIES = [
    "Work", "School", "Personal", "Health", "Finance", "Social", 
    "Errands", "Home", "Travel", "Other"
]

# Predefined task types
TASK_TYPES = [
    "basic_task",  # Static to-do
    "reminder",  # Notification-based
    "recurring_task",  # Repeats on schedule
    "deadline_based_task",  # Strict deadline
    "ai_suggested_task",  # AI-generated or adjusted
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
        """
        Initialize a task (supports both manual & AI-generated tasks).
        
        :param name: Task name (e.g., "Submit Homework").
        :param description: Additional details about the task.
        :param user_category: Task category (e.g., Work, School, etc.).
        :param task_type: How the system automates it (Reminder, Deadline, etc.).
        :param source: Where the task was created (Manual, Email, Calendar, Notes, AI).
        :param datetime_str: Scheduled time (optional, in ISO 8601 format).
        :param ai_generated: Boolean flag indicating if AI created the task.
        """
        if user_category not in USER_CATEGORIES:
            raise ValueError(f"Invalid user_category: {user_category}")
        if task_type not in TASK_TYPES:
            raise ValueError(f"Invalid task_type: {task_type}")

        self.id = str(uuid.uuid4())  # Unique task ID
        self.name = name
        self.description = description if description else ""
        self.user_category = user_category
        self.task_type = task_type
        self.source = source
        self.ai_generated = ai_generated
        self.trigger_time = self.parse_datetime(datetime_str)
        self.status = "Pending"  # Default status: Pending
        self.execution_details = self.get_execution_details()

    def parse_datetime(self, datetime_str: Optional[str]):
        """Parse datetime from string if provided."""
        if datetime_str:
            try:
                return datetime.datetime.fromisoformat(datetime_str)
            except ValueError:
                raise ValueError("Invalid datetime format. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)")
        return None  # Some tasks may not require a specific time

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

    def __repr__(self):
        return f"<Task {self.name} [{self.user_category}] - {self.status}>"
    
    def __str__(self):
        """Return a structured string representation of the task for frontend rendering."""
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


if __name__ == "__main__":
    print("hello")
    # Example Usage:

    # AI-generated task from email
    task1 = Task(
        name="Submit Homework",
        description="Complete and upload math assignment by Friday.",
        user_category="School",
        task_type="deadline_based_task",
        source="Email",
        datetime_str="2025-02-02T18:00:00",
        ai_generated=True
    )

    # Manually created task
    task2 = Task(
        name="Morning Workout",
        description="30-minute cardio session.",
        user_category="Health",
        task_type="recurring_task",
        source="Manual"
    )

    # Display tasks
    print(task1)
    print(task2)
# taskextractor.py
#Notes: Should we do a regex approach with a bunch of differnt use case cased depnding on the thing 
# or rely oin generative ai to process the different texts fed into the pipe line?



import re
import datetime
import json
from dateutil.parser import parse as dateutil_parse  # Requires: pip install python-dateutil
from taskClass import Task

def extract_datetime_from_text(text: str) -> str:
    """
    Search the text for a time pattern (e.g., "at 2 PM" or "at 14:00") and, if found,
    combine it with today's date (or tomorrow if that time has passed) to return an ISO 8601 datetime string.
    """
    # Look for a pattern like "at 2 PM" or "at 14:00"
    pattern = r"at (\d{1,2}(?::\d{2})?\s*[APMapm]{2})"
    match = re.search(pattern, text)
    if match:
        time_str = match.group(1).strip()
        now = datetime.datetime.now()
        try:
            # Parse the time string (using today's date)
            time_parsed = dateutil_parse(time_str)
            dt = now.replace(hour=time_parsed.hour,
                             minute=time_parsed.minute,
                             second=0,
                             microsecond=0)
            # If the time has already passed today, schedule for tomorrow
            if dt < now:
                dt += datetime.timedelta(days=1)
            return dt.isoformat()
        except Exception:
            return None
    return None

def determine_category_and_type(source: str, text: str) -> (str, str):
    """
    Determine the task's user_category and task_type based on the source and text.
    These heuristic rules can be enhanced or replaced with a more advanced NLP model.
    """
    text_lower = text.lower()

    if source.lower() == "calendar":
        if "prof" in text_lower or "class" in text_lower:
            return "School", "reminder"
        elif "meeting" in text_lower:
            return "Work", "reminder"
        elif "appointment" in text_lower:
            return "Health", "reminder"
    elif source.lower() == "email":
        if "assignment" in text_lower or "due" in text_lower:
            return "School", "deadline_based_task"
        elif "invoice" in text_lower or "bill" in text_lower:
            return "Finance", "reminder"
        elif "update" in text_lower:
            return "Work", "basic_task"
    elif source.lower() == "notes":
        if "buy" in text_lower or "groceries" in text_lower:
            return "Personal", "basic_task"
        elif "workout" in text_lower:
            return "Health", "recurring_task"

    # Default fallback
    return "Other", "basic_task"

def extract_task(source: str, text: str) -> Task:
    """
    Given text from a specific source, extract relevant information and
    return an auto-generated Task object.
    """
    # Use the first sentence (or the full text if no period is present) as the task name.
    name = text.split('.')[0] if '.' in text else text

    # Determine the user_category and task_type based on heuristics.
    user_category, task_type = determine_category_and_type(source, text)

    # Attempt to extract a datetime string from the text.
    datetime_str = extract_datetime_from_text(text)

    # Create and return the Task instance (marking it as AI-generated).
    task = Task(
        name=name,
        description=text,
        user_category=user_category,
        task_type=task_type,
        source=source,
        datetime_str=datetime_str,
        ai_generated=True
    )
    return task

def task_to_json(task: Task) -> dict:
    """
    Serialize the Task object into a JSON-ready dictionary.
    """
    return {
        "id": task.id,
        "name": task.name,
        "user_category": task.user_category,
        "task_type": task.task_type,
        "source": task.source,
        "trigger": {
            "type": "time-based" if task.trigger_time else "none",
            "datetime": task.trigger_time.isoformat() if task.trigger_time else None
        },
        "execution_details": task.execution_details,
        "editable_fields": ["trigger", "execution_details"],
        "status": task.status
    }

def generate_task_from_text(text: str, source: str = "Notes") -> dict:
    """
    Given a text input (and an optional source type), extract a task and return its JSON representation.
    
    :param text: The raw text from which to extract a task.
    :param source: The source of the text (e.g., "Email", "Calendar", "Notes"). Defaults to "Notes".
    :return: A dictionary representing the extracted task in JSON format.
    """
    task = extract_task(source, text)
    return task_to_json(task)

# Example usage:
if __name__ == "__main__":
    # You can simply input any text here:
    sample_text = "Your assignment is due Friday. Please ensure it is submitted on time."
    task_json = generate_task_from_text(sample_text, source="Email")
    print("Extracted Task (JSON):")
    print(json.dumps(task_json, indent=4))

import re
import datetime
import json
from dateutil.parser import parse as dateutil_parse  # pip install python-dateutil
from taskClass import Task

def preprocess_text(text: str) -> str:
    """
    Clean up and normalize the input text.
    """
    # Remove extra spaces and newlines
    return " ".join(text.strip().split())

def classify_domain(text: str) -> str:
    """
    Classify the input text into one of several domains:
    - "syllabus": Academic texts (e.g., assignments, course modules).
    - "meeting_minutes": Corporate or meeting texts (e.g., action items, agenda).
    - "notes": General unstructured notes.
    
    This simple heuristic checks for key phrases.
    """
    lower_text = text.lower()
    # Check for academic-related keywords
    if any(keyword in lower_text for keyword in ["assignment", "due", "course", "module", "syllabus", "lecture"]):
        return "syllabus"
    # Check for meeting-related keywords
    elif any(keyword in lower_text for keyword in ["action item", "agenda", "meeting", "minutes", "assigned", "discussion"]):
        return "meeting_minutes"
    # Default to general notes
    else:
        return "notes"

def extract_datetime_from_text(text: str) -> str:
    """
    Look for a time pattern in the text (e.g., "at 2 PM") and, if found, 
    create an ISO 8601 datetime string for today (or tomorrow if the time has passed).
    """
    pattern = r"at (\d{1,2}(?::\d{2})?\s*[APMapm]{2})"
    match = re.search(pattern, text)
    if match:
        time_str = match.group(1).strip()
        now = datetime.datetime.now()
        try:
            time_parsed = dateutil_parse(time_str)
            dt = now.replace(hour=time_parsed.hour,
                             minute=time_parsed.minute,
                             second=0,
                             microsecond=0)
            # If the time has already passed, schedule for tomorrow.
            if dt < now:
                dt += datetime.timedelta(days=1)
            return dt.isoformat()
        except Exception:
            return None
    return None

def determine_category_and_type(domain: str, text: str) -> (str, str):
    """
    Based on the document domain and the text content, determine the 
    user_category and task_type for the Task.
    """
    text_lower = text.lower()
    
    if domain == "syllabus":
        # In academic texts, assignments or due items become deadline tasks.
        if "assignment" in text_lower or "due" in text_lower:
            return "School", "deadline_based_task"
        else:
            return "School", "reminder"
    
    elif domain == "meeting_minutes":
        # In meeting minutes, action items and assigned tasks might be flagged.
        if "action item" in text_lower or "assigned" in text_lower:
            return "Work", "ai_suggested_task"
        else:
            return "Work", "reminder"
    
    elif domain == "notes":
        # In notes, we can check for keywords that indicate a to-do.
        if any(word in text_lower for word in ["buy", "call", "submit", "check"]):
            return "Personal", "basic_task"
        else:
            return "Other", "basic_task"
    
    # Fallback:
    return "Other", "basic_task"

def extract_task(domain: str, text: str) -> Task:
    """
    Extracts a Task from a given piece of text using the domain context.
    """
    # Use the first sentence (or the full text if no period) as the task name.
    name = text.split('.')[0] if '.' in text else text
    user_category, task_type = determine_category_and_type(domain, text)
    datetime_str = extract_datetime_from_text(text)
    
    task = Task(
        name=name,
        description=text,
        user_category=user_category,
        task_type=task_type,
        source=domain,  # Use the domain as the source
        datetime_str=datetime_str,
        ai_generated=True
    )
    return task

def task_to_json(task: Task) -> dict:
    """
    Convert a Task object into a JSON-ready dictionary.
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

def generate_tasks_from_text(text: str, domain: str) -> list:
    """
    Splits the text into separate task entries and extracts each task.
    Assumes that tasks are separated by newline characters.
    """
    tasks = []
    # Split on newlines (or other delimiters if needed)
    task_entries = text.strip().split("\n")
    for entry in task_entries:
        entry = entry.strip()
        if entry:  # Ignore empty lines
            task = extract_task(domain, entry)
            tasks.append(task_to_json(task))
    return tasks

def extract_tasks_from_document(text: str) -> list:
    """
    The complete pipeline:
      1. Preprocess the text.
      2. Classify the domain.
      3. Split the text into entries.
      4. Extract tasks from each entry.
    Returns a list of task JSON objects.
    """
    preprocessed_text = preprocess_text(text)
    domain = classify_domain(preprocessed_text)
    
    # If the document appears to have multiple lines, assume each is a separate task.
    if "\n" in text:
        tasks = generate_tasks_from_text(text, domain)
    else:
        # Otherwise, attempt to split the text into sentences.
        sentences = re.split(r'(?<=[.!?])\s+', text)
        tasks = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                task = extract_task(domain, sentence)
                tasks.append(task_to_json(task))
    return tasks

# -------------------------------
# Example usage of the pipeline
# -------------------------------
if __name__ == "__main__":
    # Sample text from different domains:
    
    sample_syllabus = (
        "Assignment: Read Chapter 5 and submit a summary by Tuesday.\n"
        "Lecture: Introduction to Machine Learning at 10 AM.\n"
        "Due: Homework 3 is due on Friday."
    )
    
    sample_meeting = (
        "Action item: Follow up with John regarding the budget proposal at 3 PM.\n"
        "Discussed new project ideas and assigned tasks to the team.\n"
        "Meeting scheduled: Next meeting at 11 AM on Thursday."
    )
    
    sample_notes = (
        "Buy groceries after work.\n"
        "Call the electrician for repair.\n"
        "Submit expense report."
    )
    
    # Process each sample:
    print("=== Syllabus Tasks ===")
    syllabus_tasks = extract_tasks_from_document(sample_syllabus)
    print(json.dumps(syllabus_tasks, indent=4))
    
    print("\n=== Meeting Minutes Tasks ===")
    meeting_tasks = extract_tasks_from_document(sample_meeting)
    print(json.dumps(meeting_tasks, indent=4))
    
    print("\n=== General Notes Tasks ===")
    notes_tasks = extract_tasks_from_document(sample_notes)
    print(json.dumps(notes_tasks, indent=4))

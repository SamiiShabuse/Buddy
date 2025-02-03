# task_extractor.py
import spacy
import dateparser
from typing import List
from taskClass import Task  # <-- Import your Task class here

# If you have these constants in taskClass.py, you don't necessarily
# need them repeated. You can reuse from taskClass if they are accessible.
USER_CATEGORIES = [
    "Work", "School", "Personal", "Health", "Finance", "Social", 
    "Errands", "Home", "Travel", "Other"
]

TASK_TYPES = [
    "basic_task",
    "reminder",
    "recurring_task",
    "deadline_based_task",
    "ai_suggested_task",
    "auto_rescheduled_task"
]

def guess_category(text: str) -> str:
    """
    Very naive approach: 
    Assign 'School' if words like 'homework' or 'class' are found, 
    'Work' if 'meeting' or 'project', etc.
    """
    text_lower = text.lower()
    if any(word in text_lower for word in ["homework", "assignment", "exam", "class"]):
        return "School"
    if any(word in text_lower for word in ["meeting", "project", "report", "office"]):
        return "Work"
    if any(word in text_lower for word in ["doctor", "workout", "exercise", "gym"]):
        return "Health"
    if any(word in text_lower for word in ["budget", "invoice", "bank", "tax", "finance"]):
        return "Finance"
    if any(word in text_lower for word in ["flight", "trip", "travel", "hotel"]):
        return "Travel"
    if any(word in text_lower for word in ["groceries", "errand", "errands", "shopping"]):
        return "Errands"
    return "Other"

def guess_task_type(text: str) -> str:
    """
    Another naive approach for deciding the task type.
    - If 'remind' is in text, it's a "reminder".
    - If 'due' or 'deadline' in text, it's a "deadline_based_task".
    - If 'every week' or 'recurring', it's a "recurring_task".
    - Otherwise, "basic_task".
    """
    text_lower = text.lower()
    if "remind" in text_lower:
        return "reminder"
    elif "due" in text_lower or "deadline" in text_lower:
        return "deadline_based_task"
    elif "recurring" in text_lower or "every day" in text_lower or "every week" in text_lower:
        return "recurring_task"
    else:
        return "basic_task"

def parse_tasks_spacy(text: str, source: str = "AI") -> List[Task]:
    """
    Use spaCy to:
      - Break text into sentences
      - Identify potential date/time entities
      - Create Task objects
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tasks = []

    # For each sentence, treat it as a potential "task".
    for sent in doc.sents:
        sent_text = sent.text.strip()
        if not sent_text:
            continue

        # Heuristic: if the sentence is too short (1-2 words), skip it.
        if len(sent_text.split()) < 2:
            continue

        # 1. Try to guess category
        user_category = guess_category(sent_text)

        # 2. Guess the task type
        task_type = guess_task_type(sent_text)

        # 3. Attempt to parse out a date/time (using spaCy's recognized entities + dateparser)
        date_found_iso = None
        for ent in sent.ents:
            if ent.label_ in ["DATE", "TIME"]:  # spaCy recognized it as date/time
                parsed_dt = dateparser.parse(ent.text)
                if parsed_dt:
                    # Convert to ISO8601
                    date_found_iso = parsed_dt.isoformat()
                    # (If your logic only expects one date per sentence, break here)
                    break

        # 4. Create a short "name" and use the full sentence as the "description"
        #    (If text is too long, we’ll truncate with "...")
        name = (sent_text[:50] + "...") if len(sent_text) > 50 else sent_text

        # 5. Build the Task
        new_task = Task(
            name=name,
            description=sent_text,
            user_category=user_category,
            task_type=task_type,
            source=source,
            datetime_str=date_found_iso,
            ai_generated=True  # Mark that it was AI generated or auto-suggested
        )

        tasks.append(new_task)

    return tasks

if __name__ == "__main__":
    sample_text = """
    Complete the math homework assignment. It's due by February 5th.
    Remind me to schedule a meeting with the project team on 2025-02-10.
    Grocery shopping next week Saturday morning.
    Doctor appointment at 10 am on 3/01/2025.
    """

    extracted_tasks = parse_tasks_spacy(sample_text, source="Syllabus/Email/Notes/etc.")

    for t in extracted_tasks:
        print("------------------------------------------------")
        print(t)
        print("------------------------------------------------")




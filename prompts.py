


taskExtractorPrompt = f"""
    Extract **all tasks** from the following text and return them as a JSON array.

    Input: "{input_text}"

    Each task should have the following structure:
    - id (generate a unique ID)
    - name (short description of the task)
    - user_category (Work, School, Personal, Health, etc.)
    - task_type (Reminder, Deadline-Based Task, Recurring Task, Basic Task)
    - source (Email, Calendar, Notes)
    - trigger (if time-based, include datetime in ISO 8601 format)
    - execution_details (notification_type: push, email, etc., and message)
    - editable_fields (list of fields that the user can modify)
    - status (default: Pending)

    Example output:
    [
      {{
        "id": "a1b2c3d4",
        "name": "Submit Homework",
        "user_category": "School",
        "task_type": "deadline_based_task",
        "source": "Email",
        "trigger": {{
          "type": "time-based",
          "datetime": "2025-02-02T18:00:00Z"
        }},
        "execution_details": {{
          "notification_type": "push",
          "message": "Reminder: Submit your homework!"
        }},
        "editable_fields": ["trigger", "execution_details"],
        "status": "Pending"
      }},
      {{
        "id": "e5f6g7h8",
        "name": "Doctor's Appointment",
        "user_category": "Health",
        "task_type": "Reminder",
        "source": "Calendar",
        "trigger": {{
          "type": "time-based",
          "datetime": "2025-03-05T15:00:00Z"
        }},
        "execution_details": {{
          "notification_type": "push",
          "message": "Reminder: Doctor's appointment at 3 PM"
        }},
        "editable_fields": ["trigger", "execution_details"],
        "status": "Pending"
      }}
    ]

    Provide the JSON array only.
    """
import tkinter as tk
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scopes and token file name
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.pickle'


# Authenticate and authorize the user
def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


# Create a task event on the student's calendar
def create_task_event(creds, student_name, task_details, due_date, due_time):
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'Task for {student_name}',
        'description': task_details,
        'start': {
            'dateTime': f'{due_date}T{due_time}:00',
            'timeZone': 'UTC'  # Replace with the desired time zone
        },
        'end': {
            'dateTime': f'{due_date}T{due_time}:00',
            'timeZone': 'UTC'  # Replace with the desired time zone
        },
        'reminders': {'useDefault': True}
    }

    service.events().insert(calendarId='primary', body=event).execute()


# Retrieve and display all tasks from Google Calendar
def view_tasks():
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)

    # Retrieve the list of events from the calendar
    events_result = service.events().list(calendarId='primary', timeMin='2023-01-01T00:00:00Z',
                                          maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Create a new window to display the tasks
    tasks_window = tk.Toplevel(root)
    tasks_window.title('Tasks')

    tasks_text = tk.Text(tasks_window, height=10, width=50)
    tasks_text.pack()

    # Populate the Text widget with the tasks
    if events:
        for event in events:
            summary = event['summary']
            description = event['description']
            start = event['start'].get('dateTime', 'No start time')
            end = event['end'].get('dateTime', 'No end time')
            tasks_text.insert(tk.END, f'Summary: {summary}\n')
            tasks_text.insert(tk.END, f'Description: {description}\n')
            tasks_text.insert(tk.END, f'Start: {start}\n')
            tasks_text.insert(tk.END, f'End: {end}\n')
            tasks_text.insert(tk.END, '\n')

    else:
        tasks_text.insert(tk.END, 'No tasks found.')

    tasks_text.config(state=tk.DISABLED)
    tasks_text.bind("<1>", lambda event: tasks_text.focus_set())  # Prevent clicking inside the Text widget


# Handle task assignment button click
def assign_task():
    student_name = student_entry.get()
    task_details = task_entry.get('1.0', tk.END)
    due_date = due_entry.get()
    due_time = time_entry.get()

    creds = authenticate()
    create_task_event(creds, student_name, task_details, due_date, due_time)

def logout():
    root.destroy()

# Create the Tkinter admin interface
root = tk.Tk()

# Create a label for "Admin Homepage"
label = tk.Label(root, text="Admin Homepage", font=("Helvetica", 32))
label.pack(pady=20)  # Position the label at the top with some padding

student_label = tk.Label(root, text='Student Name:')
student_entry = tk.Entry(root, width=40)

task_label = tk.Label(root, text='Task Details:')
task_entry = tk.Text(root, height=10, width=30)

due_label = tk.Label(root, text='Due Date:')
due_entry = tk.Entry(root)

time_label = tk.Label(root, text='Due Time:')
time_entry = tk.Entry(root)

assign_button = tk.Button(root, text='Assign Task', command=assign_task)
view_button = tk.Button(root, text='View Tasks', command=view_tasks)
logout_button = tk.Button(root, text='Logout', command=logout)

student_label.pack()
student_entry.pack()

task_label.pack()
task_entry.pack()

due_label.pack()
due_entry.pack()

time_label.pack()
time_entry.pack()

assign_button.pack()
view_button.pack()
logout_button.pack()

# Check if the token file exists and contains valid credentials
creds = authenticate()
if creds:
    view_button.config(state=tk.NORMAL)
    assign_button.config(state=tk.NORMAL)

root.mainloop()
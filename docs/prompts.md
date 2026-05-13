# Prompts Used

## Prompt 1: 

Objective:
Create the complete Mini Task Tracker application from scratch using Python, PySide6, SQLite, and MVC architecture. The goal was to generate the required folder structure, core files, database logic, validation logic, UI, controller flow, tests, and documentation.

Prompt:
You are an expert Python desktop application developer.

Build a complete Linux desktop application named Mini Task Tracker using:

- Python
- PySide6
- SQLite
- MVC architecture

First, understand the problem clearly:

Problem Statement:
Build a small desktop task tracker application for managing simple software development tasks locally. The user should be able to add, view, edit, delete, search, and filter tasks. All tasks must be stored locally using SQLite. The project must strictly follow MVC separation so that the UI, database logic, and validation logic are cleanly separated.

Expected Result:
The final output should be a runnable PySide6 desktop app. When the user runs `python main.py`, the application should open a window where the user can:

1. Add a task with title, description, priority, and status.
2. View all tasks in a table.
3. Edit an existing selected task.
4. Delete a selected task after confirmation.
5. Filter tasks by status.
6. Filter tasks by priority.
7. Search tasks by title.
8. Persist all task data locally in SQLite.
9. Validate input before saving:
   - Title cannot be empty.
   - Priority must be selected.
   - Status must be selected.

Each task should contain:

- id
- title
- description
- priority: Low, Medium, High
- status: Todo, In Progress, Done
- created_at: automatically generated current date/time

Architecture Requirements:
The code must be scalable, adaptable, maintainable, and easy to extend later. Follow proper MVC separation.

Use this exact folder structure:

mini_task_tracker/
│
├── main.py
├── requirements.txt
├── README.md
│
├── models/
│   └── task.py
│
├── views/
│   ├── main_window.py
│   └── task_form.py
│
├── controllers/
│   └── task_controller.py
│
├── repositories/
│   └── task_repository.py
│
├── services/
│   └── validation_service.py
│
├── tests/
│   └── test_validation_service.py
│
└── docs/
    ├── AI_USAGE_LOG.md
    ├── PROMPTS.md
    └── FINAL_REFLECTION.md

Important MVC Rules:

1. Model:
   - Only contains the task data structure.
   - Use a dataclass named Task.

2. View:
   - Contains only PySide6 UI code.
   - It can have buttons, forms, tables, dialogs, layouts, and signals.
   - It must not contain SQL queries.
   - It must not directly access SQLite.
   - It must not contain business validation logic.

3. Controller:
   - Coordinates the flow between View, Repository, and Service.
   - Handles add, edit, delete, filter, search, and refresh actions.
   - Shows validation errors received from the validation service.

4. Repository:
   - Handles only SQLite database logic.
   - Creates the database table automatically when the app starts.
   - Implements insert, update, delete, fetch, search, and filter methods.

5. Service:
   - Handles validation only.
   - Validates title, priority, and status.
   - Returns clear validation error messages.

SQLite Table:
Create the table automatically if it does not exist:

tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
)

Implementation Requirements:

- The app should run on Linux.
- Use clean, readable Python code.
- Use type hints where useful.
- Keep functions small and focused.
- Avoid duplicate logic.
- Use clear class and method names.
- Add comments only where helpful.
- Make the code easy to extend with future features such as dark mode, CSV export, task summary, or sorting.
- Do not place all logic in one file.
- Do not break MVC rules.

UI Requirements:

Main window should include:

- A task form area with:
  - Title input
  - Description input
  - Priority dropdown
  - Status dropdown
  - Add/Update button
  - Clear button

- A task table with columns:
  - ID
  - Title
  - Priority
  - Status
  - Created Date

- Action buttons:
  - Edit selected task
  - Delete selected task
  - Refresh

- Filter/search area:
  - Status filter dropdown
  - Priority filter dropdown
  - Search title input
  - Apply filter button
  - Clear filter button

Behavior Requirements:

- On app startup, initialize the SQLite database.
- Show all existing tasks in the table.
- When adding a task, validate input first.
- If validation fails, show an error dialog.
- After adding, editing, or deleting, refresh the table.
- When editing, load selected task data into the form.
- When deleting, ask for confirmation first.
- Filters and search should work together.
- The database should persist data after the app is closed and reopened.

Testing Requirements:

Create basic unit tests for the validation service.

Test at least:

- Empty title is invalid.
- Missing priority is invalid.
- Missing status is invalid.
- Valid task input passes validation.



Expected Output:

A complete initial Mini Task Tracker project with the required MVC folder structure, PySide6 UI, SQLite database setup, task model, repository, controller, validation service, tests and README.md

Actual Output:
The AI generated the initial project structure and application files. The UI opened successfully and showed the task form, filter section, task table, and action buttons. However, after entering task details and clicking Add Task, the task was not appearing in the table, so the Add Task flow needed debugging.

Review Notes:
The generated UI matched the assignment layout, but the functionality was incomplete. The main issue was that the Add Task action was not correctly saving and refreshing the table. MVC structure was present, but the controller, repository, or table refresh flow needed correction.





## Prompt 2: Fix Add Task and Table Refresh Flow

Objective:
Debug and fix the issue where the user could enter task details, but the added task was not appearing in the table. Ensure the Add Task flow works completely from UI input to SQLite persistence and table refresh.

Prompt:
The Mini Task Tracker UI is opening correctly, and I can enter Title, Description, Priority, and Status. However, after clicking Add Task, the task is not appearing in the table.

Please debug and fix the full Add Task flow.

Check and fix the following:

1. Ensure the Add Task button signal is connected to the controller's add_task method.
2. Ensure the controller reads form values correctly from the TaskForm view.
3. Ensure validation errors are shown clearly using a dialog.
4. Ensure placeholder values like "Select priority" and "Select status" are treated as invalid.
5. Ensure TaskRepository inserts the task into SQLite correctly.
6. Ensure SQLite commit() is called after insert/update/delete.
7. Ensure the database table is created automatically on app startup.
8. Ensure after adding a task, the controller refreshes the task table.
9. Ensure the MainWindow or table view has a method to populate rows with:
   ID, Title, Priority, Status, Created Date.
10. Ensure the same repository/database instance is used by the controller.
11. Ensure the app loads existing tasks from SQLite when it starts.
12. Ensure MVC separation is preserved:
    - View should not contain SQL.
    - Repository should handle SQLite only.
    - Controller should coordinate add, refresh, edit, delete, and filter.
    - Validation should stay inside validation_service.py.

After fixing, when I add a task and click Add Task, the task must immediately appear in the table and must remain visible after closing and reopening the app.

Expected Output:
The Add Task button should correctly save task data into SQLite and immediately show the new task in the table. The task should remain available after closing and reopening the application. Validation errors should appear when title, priority, or status is missing.

Actual Output:
The Add Task flow was fixed. After entering title, description, priority, and status, clicking Add Task inserted the task into SQLite and displayed it in the table. Invalid priority and status placeholder values were handled correctly. The table showed ID, Title, Priority, Status, and Created Date. Data persistence worked using SQLite.

Review Notes:
This prompt successfully fixed the most important functional issue. After the fix, add, view, validation, and table refresh behavior worked as expected. The task IDs were unique and auto-incremented correctly, which is expected behavior for SQLite AUTOINCREMENT.




## Prompt 3: Professional UI/UX Improvement

Objective:
Improve the visual design and user experience of the already working Mini Task Tracker app without breaking the existing functionality or MVC architecture.

Prompt:
You are an expert PySide6 UI/UX developer.

I already have a working Mini Task Tracker desktop application built with:

- Python
- PySide6
- SQLite
- MVC architecture

The app currently supports:

- Add task
- Validate title, priority, and status
- View tasks in table
- Edit selected task
- Delete selected task
- Refresh table
- Filter by status
- Filter by priority
- Search by title
- Clear form
- Clear filters
- SQLite 

Now I want you to improve only the UI/UX and make the app look like a polished professional desktop application.

Important:
Do not break existing functionality.
Do not change the core architecture.
Do not move database logic into the view.
Do not move validation logic into the view.
Do not remove any existing feature.
Keep MVC separation clean.

The final UI should look modern, clean, professional, and user-friendly.

UI improvement requirements:

1. Overall Layout

Improve the layout so the app looks balanced and not like a plain form.

Use this structure:

- Header section
- Summary 
- Task form 
- Search and filter 
- Task table 
- Bottom action/status area

Add proper margins, padding, spacing, and alignment.

2. Header Section

Add a modern header at the top with:

Title:
Mini Task Tracker

Subtitle:
Track, organize, and complete your development tasks efficiently.

The header should look visually separated from the rest of the content.

3. Summary

add the below ones:
- Total Tasks
- Todo
- In Progress
- Done

The summary cards should update whenever:

- A task is added
- A task is edited
- A task is deleted
- Tasks are refreshed
- Filters are cleared

Make the cards look clean and professional.

4. Task Form Section

Improve the task form design.

It should include:

- Title input
- Description input
- Priority dropdown
- Status dropdown
- Add Task / Update Task button
- Clear button

Make this section look like a card with rounded borders and good spacing.

Use clear labels and good input sizes.

5. Search and Filter Section

Improve the search and filter area.

It should include:

- Status filter dropdown
- Priority filter dropdown
- Search by title input
- Apply Filter button
- Clear Filter button


6. Task Table Section

Improve the task table design.

The table must keep these columns:

- ID
- Title
- Priority
- Status
- Created Date

Table improvements:

- Bold table headers
- Better row height
- Alternating row colors
- Full-row selection
- Stretch the Title column
- Clean grid lines
- Better spacing inside cells
- Non-editable cells
- Professional dark theme styling

7. Buttons

Improve button styling and text.

Use clear button labels like:

- + Add Task
- Update Task
- Clear
- Edit Selected
- Delete Selected
- Refresh
- Apply Filter
- Clear Filter

Button style requirements:

- Add Task should look like a primary action.
- Update Task should look like a primary action.
- Delete Selected should look like a danger action.
- Refresh, Clear, and Clear Filter should look neutral.
- Buttons should have hover effects.
- Buttons should have consistent height and padding.

8. Status Bar / User Feedback

Add a status bar or footer message area.

Show short messages like:

- Ready
- Task added successfully
- Task updated successfully
- Task deleted successfully
- Filter applied
- Showing all tasks
- Please select a task first

Avoid too many popups for success messages. Use popups only for validation errors, warnings, and delete confirmation.

9. Empty State

If there are no tasks in the table, show a friendly message somewhere near the table:

No tasks found. Add your first task to get started.

If filters return no result, show:

No matching tasks found. Try changing your filters.

10. Styling

Create a separate stylesheet file:

styles/app_style.py

Put all QSS styling inside this file.

Apply it in main.py using:

app.setStyleSheet(APP_STYLESHEET)

Use a professional dark theme.


11. Maintainability

Keep the code clean and maintainable.

Do not hardcode repeated style strings inside many widgets if they can be handled by QSS.

Use object names for special buttons where needed.

12. Functional Verification

After improving the UI, verify that all existing features still work:

- App runs using python main.py
- Add task works
- Validation works
- Clear form works
- Edit selected task works
- Delete selected task works
- Refresh works
- Filter by status works
- Filter by priority works
- Search by title works
- Clear filter works
- SQLite persistence still works
- Existing tests still pass using pytest

13. MVC Verification

Confirm that:

- views contain only UI code
- repository contains SQLite code only
- service contains validation only
- controller coordinates app actions
- model contains only the Task data structure

Final output expected:

- Updated PySide6 UI files
- New styles/app_style.py file
- Updated main.py to apply the stylesheet
- No broken existing features
- Professional-looking Mini Task Tracker UI

Expected Output:
A more professional-looking Mini Task Tracker UI with improved layout, header, styled buttons, styled table, summary cards, status feedback, and a separate stylesheet file, while keeping all existing functionality and MVC separation unchanged.

Actual Output:
The AI was expected to improve the visual design of the existing working application without changing the core app logic. The expected result was a cleaner, modern, professional dark-themed UI with better spacing, card layout, improved buttons, styled table, and user feedback.

Review Notes:
This prompt focuses on UI enhancement only. The important review point is to verify that no working feature is broken after the visual update. Add, edit, delete, filter, search, validation, refresh, and SQLite persistence must still work after the UI changes.

# Bot Architecture

## Project Structure

```
project-group-30/
├── handlers/                    # Command handlers
│   ├── command_handler.py      # Main router (orchestrates all commands)
│   ├── contact_handler.py      # Contact operations (add, find, change, delete)
│   ├── task_handler.py         # Task operations (add, find, change, delete)
│   └── decorators.py           # Error handling decorators
│
├── repositories/                # Data access layer
│   ├── contact_repository.py   # Contact data storage
│   ├── task_repository.py      # Task data storage
│   └── note_repository.py      # (legacy, to be merged with task)
│
├── models/                      # Data models
│   ├── contact.py              # Contact record model
│   ├── address.py              # Address model
│   ├── phone.py                # Phone model
│   ├── email.py                # Email model
│   ├── birthday.py             # Birthday model
│   ├── note.py                 # Note/Task model
│   └── ...
│
├── storage/                     # Persistence layer
│   ├── json_storage.py         # JSON file storage
│   ├── pickle_storage.py       # Pickle storage
│   └── ...
│
├── main.py                      # Entry point + main loop
├── constants.py                 # All messages, menus, prompts
├── utils.py                     # Helper functions (validation, UI, pagination)
└── main_Sage_arch.py           # Original draft (reference)
```

## Architecture Layers

### 1. Main Loop (`main.py`)
- Entry point for the application
- Handles user input parsing (`parse_input`)
- Routes commands to appropriate handlers
- Manages bot lifecycle (start, help, exit)
- Backward compatible with legacy commands

### 2. Command Router (`handlers/command_handler.py`)
- Orchestrates all commands
- Routes to specialized handlers (contact, task)
- Maintains legacy methods for backward compatibility
- Methods:
  - `route_add_command()` - Routes add operations
  - `route_find_command()` - Routes search operations
  - `route_change_command()` - Routes edit operations
  - `route_delete_command()` - Routes delete operations
  - `route_all_command()` - Routes list operations
  - `route_sort_command()` - Routes sort operations

### 3. Specialized Handlers

#### Contact Handler (`handlers/contact_handler.py`)
Handles all contact-related operations:
- `add_contact_interactive()` - Interactive contact creation
- `find_contact()` - Search by name/phone/email
- `find_by_address()` - Search by address
- `find_birthday()` - Find upcoming birthdays
- `show_contact_actions()` - Action menu for selected contact
- `change_contact()` - Edit contact info
- `change_address()` - Edit address
- `delete_contact()` - Remove contact
- `show_all_contacts()` - List with pagination
- `sort_contacts()` - Sort by criteria

#### Task Handler (`handlers/task_handler.py`)
Handles all task-related operations:
- `add_task_interactive()` - Interactive task creation
- `find_task()` - Search by text/tags
- `show_task_actions()` - Action menu for selected task
- `change_task()` - Edit task
- `change_task_text()` - Update text
- `change_task_tags()` - Update tags
- `link_task_to_contact()` - Link to contact
- `delete_task()` - Remove task
- `show_all_tasks()` - List with pagination
- `sort_tasks()` - Sort by criteria

### 4. Repositories
Data access layer - handles CRUD operations:
- `ContactRepository` - Contact data management
- `TaskRepository` - Task data management

### 5. Models
Data structures representing entities:
- Contact, Address, Phone, Email, Birthday
- Task/Note

### 6. Storage
Persistence layer for saving/loading data:
- JSON storage
- Pickle storage

### 7. Utilities (`utils.py`)
Helper functions:
- Validation (email, phone)
- UI helpers (menus, prompts)
- Pagination
- Phone normalization

### 8. Constants (`constants.py`)
All user-facing text in one place:
- Welcome/help messages
- Menu options
- Input prompts
- Success/error messages

## Command Flow Example

```
User Input: "add"
    ↓
main.py: parse_input() → ("add", [])
    ↓
main.py: routes to command_handler.route_add_command()
    ↓
CommandHandler: shows menu, gets user choice
    ↓
If choice = "1" (contact):
    → ContactHandler.add_contact_interactive()
        → Gets user input (name, phone, email, etc.)
        → Creates Contact model
        → Saves via ContactRepository
        → Returns success message
    ↓
main.py: prints result
```

## Development Guidelines

### Adding New Features
1. Add method skeleton in appropriate handler
2. Add constants to `constants.py` if needed
3. Implement repository methods if data access needed
4. Add routing logic in `command_handler.py`
5. Implement handler logic
6. Test

### Code Organization
- Keep handlers focused on user interaction flow
- Keep repositories focused on data operations
- Use constants for all user-facing text
- Use utils for reusable helper functions
- Add `@input_error` decorator for error handling

### Backward Compatibility
Legacy commands (show, rename, delete-phone) are maintained in `command_handler.py` for existing functionality.

## TODO
- [ ] Implement all handler methods (currently skeletons)
- [ ] Implement repository methods
- [ ] Add task-contact linking
- [ ] Add birthday notifications
- [ ] Add data persistence (save/load)
- [ ] Add search by tags
- [ ] Add sorting implementations
- [ ] Add pagination for large lists
- [ ] Merge note_repository with task_repository

"""Centralized command routing system"""
from typing import Callable, Dict, Any, Tuple, Optional
from cli.input_parser import InputParser
from cli.command_suggester import CommandSuggester
from cli.presenter import Presenter


class CommandRouter:
    """Route commands to appropriate handler functions"""
    
    def __init__(self, command_handler):
        """
        Initialize command router
        
        Args:
            command_handler: Instance of CommandHandler with handler methods
        """
        self.command_handler = command_handler
        self.commands: Dict[str, Callable] = {}
        self.command_aliases: Dict[str, str] = {}
        self._register_commands()
        self._register_aliases()
    
    def _register_commands(self):
        """Register all available commands"""
        self.commands = {
            "add": self._handle_add,
            "show": self._handle_show,
            "all": self._handle_all,
            "search-contacts": self._handle_search_contacts,
            "change": self._handle_change,
            "rename": self._handle_rename,
            "delete": self._handle_delete,
            "delete-phone": self._handle_delete_phone,
            "help": self._handle_help,
            "exit": self._handle_exit,
            "quit": self._handle_exit,
            "close": self._handle_exit,
        }
    
    def _register_aliases(self):
        """Register command aliases"""
        self.command_aliases = {
            "create": "add",
            "new": "add",
            "list": "all",
            "list-contacts": "all",
            "search": "search-contacts",
            "find": "search-contacts",
            "edit": "change",
            "remove": "delete",
            "del": "delete",
        }
    
    def route(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """
        Route user input to appropriate handler
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (should_continue, result_message)
            should_continue: False if should exit, True otherwise
            result_message: Message to display (None if no message)
        """
        command, args = InputParser.parse_command(user_input)
        
        if not command:
            return True, None
        
        # Check aliases
        if command in self.command_aliases:
            command = self.command_aliases[command]
        
        # Route to handler
        if command in self.commands:
            try:
                return self.commands[command](args)
            except Exception as e:
                return True, Presenter.error(f"Error executing command: {str(e)}")
        else:
            # Unknown command - suggest alternatives
            suggestion = CommandSuggester.get_suggestion_message(command)
            return True, Presenter.warning(suggestion)
    
    def _handle_add(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle add command"""
        if not InputParser.validate_args_count(args, 1, command="add"):
            return True, Presenter.error("Error: Please provide at least a name.")
        
        name = args[0]
        phone = args[1] if len(args) > 1 else None
        email = args[2] if len(args) > 2 else None
        address = args[3] if len(args) > 3 else None
        birthday = args[4] if len(args) > 4 else None
        
        result = self.command_handler.add_contact(name, phone, email, address, birthday)
        return True, Presenter.success(result)
    
    def _handle_show(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle show command"""
        if not InputParser.validate_args_count(args, 1, command="show"):
            return True, Presenter.error("Error: Please provide a contact name.")
        
        result = self.command_handler.show_contact(args[0])
        return True, Presenter.format_contact(result)
    
    def _handle_all(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle all command"""
        result = self.command_handler.show_all_contacts()
        # Return as-is, main.py will handle formatting
        return True, result
    
    def _handle_search_contacts(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle search-contacts command"""
        if not InputParser.validate_args_count(args, 1, command="search-contacts"):
            return True, Presenter.error("Error: Please provide a search query.")
        
        result = self.command_handler.search_contacts(args[0])
        # Return as-is, main.py will handle formatting
        return True, result
    
    def _handle_change(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle change command"""
        if not InputParser.validate_args_count(args, 3, command="change"):
            return True, Presenter.error(
                "Error: Please provide contact name, old phone, and new phone."
            )
        
        result = self.command_handler.change(args[0], args[1], args[2])
        return True, Presenter.success(result)
    
    def _handle_rename(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle rename command"""
        if not InputParser.validate_args_count(args, 2, command="rename"):
            return True, Presenter.error("Error: Please provide old name and new name.")
        
        result = self.command_handler.edit_name(args[0], args[1])
        return True, Presenter.success(result)
    
    def _handle_delete(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle delete command"""
        if not InputParser.validate_args_count(args, 1, command="delete"):
            return True, Presenter.error("Error: Please provide a contact name.")
        
        result = self.command_handler.delete_contact(args[0])
        return True, Presenter.success(result)
    
    def _handle_delete_phone(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle delete-phone command"""
        if not InputParser.validate_args_count(args, 2, command="delete-phone"):
            return True, Presenter.error(
                "Error: Please provide contact name and phone number."
            )
        
        result = self.command_handler.delete_phone(args[0], args[1])
        return True, Presenter.success(result)
    
    def _handle_help(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle help command"""
        help_text = f"""
{Presenter.header("Available Commands:")}

{Presenter.highlight("Contact Management:")}
  {Presenter.info("add <name> [phone] [email] [address] [birthday]")}
    Add or update a contact
    
  {Presenter.info("show <name>")}
    Show a specific contact
    
  {Presenter.info("all")}
    Show all contacts
    
  {Presenter.info("search-contacts <query>")}
    Search contacts by name, phone, or email
    
  {Presenter.info("change <name> <old-phone> <new-phone>")}
    Change a phone number
    
  {Presenter.info("rename <old-name> <new-name>")}
    Rename a contact
    
  {Presenter.info("delete <name>")}
    Delete a contact
    
  {Presenter.info("delete-phone <name> <phone>")}
    Delete a phone number from a contact

{Presenter.highlight("System:")}
  {Presenter.info("help [command]")}
    Show this help message
    
  {Presenter.info("exit / quit / close")}
    Exit the application

{Presenter.warning("Example:")} add John 1234567890 john@example.com '123 Main St' 01.01.1990
"""
        return True, help_text
    
    def _handle_exit(self, args: list) -> Tuple[bool, Optional[str]]:
        """Handle exit command"""
        return False, Presenter.info("Goodbye!")


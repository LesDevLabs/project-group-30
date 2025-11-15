"""Presenter for handling all user-facing output with colorama and Rich"""

from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel

from .table_renderer import TableRenderer

# Initialize colorama
init(autoreset=True)


class Presenter:
    """Handles all user-facing output with colorama colors"""

    @staticmethod
    def success(message: str) -> str:
        """Format success message in green"""
        return f"{Fore.GREEN}{message}{Style.RESET_ALL}"

    @staticmethod
    def error(message: str) -> str:
        """Format error message in red"""
        return f"{Fore.RED}{message}{Style.RESET_ALL}"

    @staticmethod
    def info(message: str) -> str:
        """Format info message in cyan"""
        return f"{Fore.CYAN}{message}{Style.RESET_ALL}"

    @staticmethod
    def warning(message: str) -> str:
        """Format warning message in yellow"""
        return f"{Fore.YELLOW}{message}{Style.RESET_ALL}"

    @staticmethod
    def header(message: str) -> str:
        """Format header message in blue/magenta"""
        return f"{Fore.BLUE}{Style.BRIGHT}{message}{Style.RESET_ALL}"

    @staticmethod
    def highlight(message: str) -> str:
        """Format highlighted text in magenta"""
        return f"{Fore.MAGENTA}{message}{Style.RESET_ALL}"

    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(Presenter.success(message))

    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(Presenter.error(message))

    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(Presenter.info(message))

    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        print(Presenter.warning(message))

    @staticmethod
    def print_header(message: str):
        """Print header message"""
        print(Presenter.header(message))

    @staticmethod
    def format_contact(contact_str: str) -> str:
        """Format contact display with colors"""
        lines = contact_str.split('\n')
        formatted_lines = []
        for line in lines:
            if 'Contact name:' in line:
                # Highlight contact name
                parts = line.split('Contact name:')
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}Contact name:{Style.RESET_ALL} "
                        f"{Fore.MAGENTA}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif 'phones:' in line:
                parts = line.split('phones:')
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}phones:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif 'emails:' in line:
                parts = line.split('emails:')
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}emails:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif 'address:' in line:
                parts = line.split('address:')
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}address:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif 'birthday:' in line:
                parts = line.split('birthday:')
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}birthday:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def print_contact(contact_str: str):
        """Print formatted contact"""
        print(Presenter.format_contact(contact_str))
    
    @staticmethod
    def print_contacts_list(contacts_list: str):
        """Print formatted list of contacts"""
        if not contacts_list or contacts_list == "No contacts stored.":
            print(Presenter.info(contacts_list))
            return
        
        contacts = contacts_list.split('\n')
        for i, contact in enumerate(contacts, 1):
            print(f"{Fore.YELLOW}[{i}]{Style.RESET_ALL} {Presenter.format_contact(contact)}")
    
    @staticmethod
    def print_prompt():
        """Print colored prompt"""
        return f"{Fore.CYAN}Enter a command:{Style.RESET_ALL} "

    @staticmethod
    def print_welcome():
        """Print welcome message"""
        welcome = f"""
{Fore.BLUE}{Style.BRIGHT}{'='*50}
  Welcome to the Personal Assistant!
{'='*50}{Style.RESET_ALL}
{Fore.CYAN}Commands:{Style.RESET_ALL}
  {Fore.GREEN}add{Style.RESET_ALL}          - Add or update a contact
  {Fore.GREEN}show{Style.RESET_ALL}         - Show a specific contact
  {Fore.GREEN}all{Style.RESET_ALL}          - Show all contacts
  {Fore.GREEN}search-contacts{Style.RESET_ALL} - Search contacts
  {Fore.GREEN}change{Style.RESET_ALL}       - Change phone number
  {Fore.GREEN}rename{Style.RESET_ALL}       - Rename a contact
  {Fore.GREEN}delete{Style.RESET_ALL}       - Delete a contact
  {Fore.GREEN}delete-phone{Style.RESET_ALL} - Delete a phone number
  {Fore.GREEN}help{Style.RESET_ALL}         - Show help
  {Fore.GREEN}exit{Style.RESET_ALL}         - Exit application

{Fore.YELLOW}Example:{Style.RESET_ALL} add John 1234567890 john@example.com '123 Main St' 01.01.1990
"""
        print(welcome)


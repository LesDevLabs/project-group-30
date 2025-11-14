"""Presenter for handling all user-facing output with colorama and Rich"""
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

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
        console = Console()
    
        title = Text("Personal Assistant", style="bold cyan", justify="center")

        table = Table(show_header=True, header_style="bold cyan", border_style="blue")
        table.add_column("Command", style="green", width=20)
        table.add_column("Description", style="white", width=30)
        
        table.add_row("add", "Add or update a contact")
        table.add_row("show", "Show a specific contact")
        table.add_row("all", "Show all contacts")
        table.add_row("search-contacts", "Search contacts")
        table.add_row("change", "Change phone number")
        table.add_row("rename", "Rename a contact")
        table.add_row("delete", "Delete a contact")
        table.add_row("delete-phone", "Delete a phone number")
        
        table.add_row("note-add, n-add", "Add note", style="magenta")
        table.add_row("note-del, n-del", "Delete note", style="magenta")
        table.add_row("note-list, n-list", "List note(s)", style="magenta")
        table.add_row("note-edit, n-edit", "Edit note", style="magenta")
        
        table.add_row("help", "Show help")
        table.add_row("exit", "Exit application")
        
        example = Text("\nExample: ", style="bold yellow")
        example.append("add John 1234567890 john@example.com '123 Main St' 01.01.1990", style="white")
        
        panel = Panel(
            table,
            title="[bold cyan]Welcome to Personal Assistant![/bold cyan]",
            subtitle="[yellow]Type 'help' for more information[/yellow]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(panel)
        console.print(example)


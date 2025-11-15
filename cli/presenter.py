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
        lines = contact_str.split("\n")
        formatted_lines = []
        for line in lines:
            if "Contact name:" in line:
                # Highlight contact name
                parts = line.split("Contact name:")
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}Contact name:{Style.RESET_ALL} "
                        f"{Fore.MAGENTA}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif "phones:" in line:
                parts = line.split("phones:")
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}phones:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif "emails:" in line:
                parts = line.split("emails:")
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}emails:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif "address:" in line:
                parts = line.split("address:")
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}address:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            elif "birthday:" in line:
                parts = line.split("birthday:")
                if len(parts) == 2:
                    formatted_lines.append(
                        f"{Fore.CYAN}birthday:{Style.RESET_ALL} "
                        f"{Fore.GREEN}{parts[1].strip()}{Style.RESET_ALL}"
                    )
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        return "\n".join(formatted_lines)

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

        contacts = contacts_list.split("\n")
        for i, contact in enumerate(contacts, 1):
            print(
                f"{Fore.YELLOW}[{i}]{Style.RESET_ALL} {Presenter.format_contact(contact)}"
            )

    @staticmethod
    def print_prompt():
        """Print colored prompt"""
        return f"{Fore.CYAN}Enter a command:{Style.RESET_ALL} "

    @staticmethod
    def print_welcome():
        """Print welcome message using TableRenderer"""
        console = Console()
        renderer = TableRenderer()

        commands_data = [
            ["add", "Add or update a contact"],
            ["show", "Show a specific contact"],
            ["all", "Show all contacts"],
            ["search-contacts", "Search contacts"],
            ["change", "Change contact information"],
            ["rename", "Rename a contact"],
            ["delete", "Delete a contact"],
            ["delete-phone", "Delete a phone number"],
            ["note-add, na", "Add note"],
            ["note-del, nd", "Delete note"],
            ["note-list, nl", "List note(s)"],
            ["note-edit, ne", "Edit note"],
            ["tag", "Show notes sorted by tags"],
            ["help", "Show help"],
            ["exit", "Exit application"],
        ]

        columns = [
            {"name": "Command", "style": "green", "width": 24},
            {"name": "Description", "style": "white", "width": 30},
        ]
        
        console.print()
        console.print(
            Panel(
                "",
                title="[bold cyan]Welcome to Personal Assistant![/bold cyan]",
                subtitle="[yellow]Type 'help' for more information[/yellow]",
                border_style="cyan",
            )
        )
        console.print()
        renderer.render(title="Available Commands", columns=columns, rows=commands_data)
        console.print()

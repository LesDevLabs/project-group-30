"""Presenter for handling all user-facing output with colorama"""
from colorama import Fore, Style, init

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
    def print_contacts_table(contacts):
        """Print contacts in a formatted table with colors"""
        if not contacts:
            print(Presenter.info("No contacts stored."))
            return
        
        # Header
        print(f"\n{Fore.BLUE}{Style.BRIGHT}{'='*120}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'#':<4} {'Name':<20} {'Contact Information':<90}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{Style.BRIGHT}{'='*120}{Style.RESET_ALL}")
        
        # Print each contact
        for idx, contact in enumerate(contacts, 1):
            # Get all phones in one line
            phones = '; '.join(p.value for p in contact.phones) if contact.phones else '-'
            
            # Get all emails in one line
            emails = '; '.join(e.value for e in contact.emails) if contact.emails else '-'
            
            # Get address
            address = contact.address.value if contact.address else '-'
            
            # Get birthday
            birthday = str(contact.birthday) if contact.birthday else '-'
            
            # Print contact info
            print(f"{Fore.YELLOW}{idx:<4}{Style.RESET_ALL} {Fore.MAGENTA}{contact.name.value:<20}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Phones:{Style.RESET_ALL}   {Fore.GREEN}{phones}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Emails:{Style.RESET_ALL}   {Fore.GREEN}{emails}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Address:{Style.RESET_ALL}  {Fore.GREEN}{address}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Birthday:{Style.RESET_ALL} {Fore.GREEN}{birthday}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-'*120}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Total contacts: {len(contacts)}{Style.RESET_ALL}\n")
    
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
    
    @staticmethod
    def print_birthdays_table(results: list[dict], days: int):
        """Print birthdays in a formatted table with colors"""
        if not results:
            print(Presenter.warning(f"No contacts have birthdays in the next {days} days."))
            return
        
        # Header
        print(f"\n{Fore.BLUE}{Style.BRIGHT}{'='*120}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'#':<4} {'Name':<20} {'Birthday Information':<90}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{Style.BRIGHT}{'='*120}{Style.RESET_ALL}")
        
        # Print each birthday
        for idx, result in enumerate(results, 1):
            # Prepare data
            jubilee = " (BIG JUBILEE)" if result['jubilee_type'] == "большой юбилей" else " (Jubilee)" if result['is_jubilee'] else ""
            age_display = f"{result['age']} years{jubilee}"
            phone = result['phone'] if result['phone'] else '-'
            email = result['email'] if result['email'] else '-'
            birthday_display = f"{result['actual_birthday_weekday']} {result['actual_birthday_date']}" if result['is_shifted'] else f"{result['weekday']} {result['date']}"
            
            # Print birthday info
            print(f"{Fore.YELLOW}{idx:<4}{Style.RESET_ALL} {Fore.MAGENTA}{result['name']:<20}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Age:{Style.RESET_ALL}        {Fore.GREEN}{age_display}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Birthday:{Style.RESET_ALL}   {Fore.GREEN}{birthday_display}{Style.RESET_ALL}")
            if result['is_shifted']:
                print(f"{'':26}{Fore.CYAN}Congratulate:{Style.RESET_ALL} {Fore.GREEN}{result['weekday']} {result['date']} (shifted from {result['shift_reason']}){Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Phone:{Style.RESET_ALL}      {Fore.GREEN}{phone}{Style.RESET_ALL}")
            print(f"{'':26}{Fore.CYAN}Email:{Style.RESET_ALL}      {Fore.GREEN}{email}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-'*120}{Style.RESET_ALL}")
        
        # Statistics
        jubilees = sum(1 for r in results if r['is_jubilee'])
        big_jubilees = sum(1 for r in results if r['jubilee_type'] == 'большой юбилей')
        shifted = sum(1 for r in results if r['is_shifted'])
        
        stats = f"Total: {len(results)} birthdays"
        if jubilees:
            stats += f" | Jubilees: {jubilees} ({big_jubilees} big, {jubilees - big_jubilees} regular)"
        if shifted:
            stats += f" | Weekend shifts: {shifted}"
        
        print(f"{Fore.CYAN}{stats}{Style.RESET_ALL}\n")


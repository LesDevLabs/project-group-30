"""Enhanced command parsing with better error handling"""
import shlex
from typing import Tuple, List


class InputParser:
    """Parse user input into command and arguments"""
    
    @staticmethod
    def parse_command(user_input: str) -> Tuple[str, List[str]]:
        """
        Parse user input into command and arguments, handling quoted strings
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (command, args) where command is lowercase and args is list
        """
        if not user_input or not user_input.strip():
            return "", []
        
        try:
            # Use shlex to handle quoted strings properly
            parts = shlex.split(user_input.strip())
        except ValueError:
            # Fallback to simple split if shlex fails (e.g., unmatched quotes)
            parts = user_input.strip().split()
        
        if not parts:
            return "", []
        
        command = parts[0].lower()
        args = parts[1:]
        
        return command, args
    
    @staticmethod
    def parse_with_flags(user_input: str) -> Tuple[str, List[str], dict]:
        """
        Parse user input with support for flags and options
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (command, args, flags) where flags is a dict
        """
        command, args = InputParser.parse_command(user_input)
        
        flags = {}
        remaining_args = []
        
        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith('--'):
                # Long flag: --flag or --flag=value
                if '=' in arg:
                    flag_name, flag_value = arg[2:].split('=', 1)
                    flags[flag_name] = flag_value
                else:
                    flag_name = arg[2:]
                    # Check if next arg is a value (not a flag)
                    if i + 1 < len(args) and not args[i + 1].startswith('-'):
                        flags[flag_name] = args[i + 1]
                        i += 1
                    else:
                        flags[flag_name] = True
            elif arg.startswith('-') and len(arg) > 1:
                # Short flag: -f or -f value
                flag_name = arg[1:]
                if i + 1 < len(args) and not args[i + 1].startswith('-'):
                    flags[flag_name] = args[i + 1]
                    i += 1
                else:
                    flags[flag_name] = True
            else:
                remaining_args.append(arg)
            i += 1
        
        return command, remaining_args, flags
    
    @staticmethod
    def validate_args_count(args: List[str], min_count: int, 
                           max_count: int = None, command: str = "") -> bool:
        """
        Validate argument count
        
        Args:
            args: List of arguments
            min_count: Minimum required arguments
            max_count: Maximum allowed arguments (None for unlimited)
            command: Command name for error messages
            
        Returns:
            True if valid, False otherwise
        """
        count = len(args)
        if count < min_count:
            return False
        if max_count is not None and count > max_count:
            return False
        return True


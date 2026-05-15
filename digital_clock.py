#!/usr/bin/env python3
"""Digital Clock displaying current time in different time zones."""

import time
from datetime import datetime
import pytz
import os
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Define time zones to display
TIME_ZONES = {
    'UTC': 'UTC',
    'EST': 'America/New_York',
    'CST': 'America/Chicago',
    'MST': 'America/Denver',
    'PST': 'America/Los_Angeles',
    'IST': 'Asia/Kolkata',
    'JST': 'Asia/Tokyo',
    'AEST': 'Australia/Sydney',
    'GMT': 'Europe/London',
    'CET': 'Europe/Paris',
    'GST': 'Asia/Dubai',
    'SGT': 'Asia/Singapore',
}


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_time_in_zone(timezone_name):
    """Get current time in a specific timezone."""
    tz = pytz.timezone(timezone_name)
    return datetime.now(tz)


def format_time(dt):
    """Format datetime object to readable time string."""
    return dt.strftime('%H:%M:%S')


def format_date(dt):
    """Format datetime object to readable date string."""
    return dt.strftime('%A, %B %d, %Y')


def display_clock(use_24_hour=True):
    """Display digital clock with multiple time zones."""
    try:
        while True:
            clear_screen()
            
            # Header
            print(f"{Back.CYAN}{Fore.BLACK}{'╔' + '═'*78 + '╗'}{Style.RESET_ALL}")
            print(f"{Back.CYAN}{Fore.BLACK}{'║' + ' '*78 + '║'}{Style.RESET_ALL}")
            print(f"{Back.CYAN}{Fore.BLACK}{'║' + 'WORLD TIME ZONE CLOCK'.center(78) + '║'}{Style.RESET_ALL}")
            print(f"{Back.CYAN}{Fore.BLACK}{'║' + ' '*78 + '║'}{Style.RESET_ALL}")
            print(f"{Back.CYAN}{Fore.BLACK}{'╚' + '═'*78 + '╝'}{Style.RESET_ALL}")
            print()
            
            # Get current time in local timezone
            local_time = datetime.now()
            print(f"{Fore.YELLOW}Local Time: {format_date(local_time)}")
            print()
            
            # Display clocks for each timezone
            print(f"{Fore.GREEN}{'Timezone':<15} {'Time':<20} {'Date':<35}")
            print(f"{Fore.GREEN}{'-'*70}")
            
            for abbr, timezone_name in TIME_ZONES.items():
                try:
                    dt = get_time_in_zone(timezone_name)
                    time_str = format_time(dt)
                    date_str = format_date(dt)
                    
                    # Color code based on timezone region
                    if 'America' in timezone_name:
                        color = Fore.BLUE
                    elif 'Europe' in timezone_name:
                        color = Fore.MAGENTA
                    elif 'Asia' in timezone_name or 'Australia' in timezone_name:
                        color = Fore.CYAN
                    else:
                        color = Fore.WHITE
                    
                    print(f"{color}{abbr:<15} {time_str:<20} {date_str:<35}")
                
                except Exception as e:
                    print(f"{Fore.RED}{abbr:<15} Error: {str(e)}")
            
            print()
            print(f"{Fore.YELLOW}{'═'*70}")
            print(f"{Fore.CYAN}Press Ctrl+C to exit | Refreshing every second...")
            print(f"{Fore.YELLOW}{'═'*70}")
            
            # Refresh every second
            time.sleep(1)
    
    except KeyboardInterrupt:
        clear_screen()
        print(f"{Fore.GREEN}Thank you for using World Time Zone Clock!")
        print(f"{Fore.GREEN}Goodbye!\n")


def display_static_clock():
    """Display static clock (no refresh) showing all timezones."""
    clear_screen()
    
    # Header
    print(f"{Back.CYAN}{Fore.BLACK}{'╔' + '═'*78 + '╗'}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'║' + ' '*78 + '║'}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'║' + 'WORLD TIME ZONE SNAPSHOT'.center(78) + '║'}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'║' + ' '*78 + '║'}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'╚' + '═'*78 + '╝'}{Style.RESET_ALL}")
    print()
    
    # Get current time in local timezone
    local_time = datetime.now()
    print(f"{Fore.YELLOW}Generated at: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Display clocks for each timezone
    print(f"{Fore.GREEN}{'Timezone':<15} {'Time':<20} {'Date':<35} {'UTC Offset':<10}")
    print(f"{Fore.GREEN}{'-'*80}")
    
    for abbr, timezone_name in TIME_ZONES.items():
        try:
            dt = get_time_in_zone(timezone_name)
            time_str = format_time(dt)
            date_str = format_date(dt)
            offset = dt.strftime('%z')
            offset_formatted = f"{offset[:3]}:{offset[3:]}"
            
            # Color code based on timezone region
            if 'America' in timezone_name:
                color = Fore.BLUE
            elif 'Europe' in timezone_name:
                color = Fore.MAGENTA
            elif 'Asia' in timezone_name or 'Australia' in timezone_name:
                color = Fore.CYAN
            else:
                color = Fore.WHITE
            
            print(f"{color}{abbr:<15} {time_str:<20} {date_str:<35} {offset_formatted:<10}")
        
        except Exception as e:
            print(f"{Fore.RED}{abbr:<15} Error: {str(e)}")
    
    print()
    print(f"{Fore.YELLOW}{'═'*80}")


def get_time_difference(tz1, tz2):
    """Calculate time difference between two timezones."""
    dt1 = get_time_in_zone(tz1)
    dt2 = get_time_in_zone(tz2)
    
    offset1 = dt1.utcoffset().total_seconds() / 3600
    offset2 = dt2.utcoffset().total_seconds() / 3600
    
    difference = offset2 - offset1
    return difference


def display_timezone_info():
    """Display detailed timezone information."""
    clear_screen()
    
    print(f"{Back.GREEN}{Fore.BLACK}{'TIMEZONE INFORMATION'.center(80)}{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.GREEN}{'Timezone':<15} {'Full Name':<30} {'Current Time':<20}")
    print(f"{Fore.GREEN}{'-'*65}")
    
    for abbr, timezone_name in TIME_ZONES.items():
        try:
            dt = get_time_in_zone(timezone_name)
            time_str = format_time(dt)
            print(f"{Fore.CYAN}{abbr:<15} {timezone_name:<30} {time_str:<20}")
        except Exception as e:
            print(f"{Fore.RED}{abbr:<15} Error: {str(e)}")
    
    print()
    print(f"{Fore.YELLOW}{'═'*65}")
    print(f"{Fore.MAGENTA}Time differences from UTC:")
    print(f"{Fore.YELLOW}{'═'*65}")
    
    for abbr, timezone_name in TIME_ZONES.items():
        try:
            dt = get_time_in_zone(timezone_name)
            offset = dt.utcoffset()
            hours, remainder = divmod(int(offset.total_seconds()), 3600)
            minutes = remainder // 60
            offset_str = f"UTC{'+' if hours >= 0 else ''}{hours:02d}:{minutes:02d}"
            print(f"{Fore.CYAN}{abbr:<15} {offset_str}")
        except Exception as e:
            print(f"{Fore.RED}{abbr:<15} Error: {str(e)}")
    
    print()


def main():
    """Main menu and program entry point."""
    while True:
        clear_screen()
        print(f"{Back.BLUE}{Fore.WHITE}{'WORLD TIME ZONE CLOCK - MAIN MENU'.center(80)}{Style.RESET_ALL}")
        print()
        print(f"{Fore.GREEN}1. {Fore.WHITE}Live Clock (Updates every second)")
        print(f"{Fore.GREEN}2. {Fore.WHITE}Static Snapshot (Single view of all timezones)")
        print(f"{Fore.GREEN}3. {Fore.WHITE}Timezone Information")
        print(f"{Fore.GREEN}4. {Fore.WHITE}Exit")
        print()
        print(f"{Fore.YELLOW}{'═'*80}")
        
        choice = input(f"{Fore.CYAN}Select an option (1-4): {Fore.WHITE}")
        
        if choice == '1':
            display_clock()
        elif choice == '2':
            display_static_clock()
            input(f"\n{Fore.CYAN}Press Enter to return to menu...")
        elif choice == '3':
            display_timezone_info()
            input(f"\n{Fore.CYAN}Press Enter to return to menu...")
        elif choice == '4':
            clear_screen()
            print(f"{Fore.GREEN}Thank you for using World Time Zone Clock!")
            print(f"{Fore.GREEN}Goodbye!\n")
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.")
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")

import os
import sys
import socket
import colorama
import time
import requests
import subprocess
from colorama import Fore, Style

colorama.init(autoreset=True)

def create_user(username, password):
    users_path = "users"
    os.makedirs(users_path, exist_ok=True)
    user_file_path = os.path.join(users_path, f"{username}.txt")
    with open(user_file_path, "w") as user_file:
        user_file.write(password)

def authenticate(username, password):
    users_path = "users"
    user_file_path = os.path.join(users_path, f"{username}.txt")
    if os.path.exists(user_file_path):
        with open(user_file_path, "r") as user_file:
            stored_password = user_file.read().strip()
            return stored_password == password
    return False

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def get_public_ip():
    try:
        public_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except Exception:
        public_ip = "N/A"
    return public_ip

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        country = data.get("country", "Unknown")
        city = data.get("city", "Unknown")
        postal = data.get("postal", "Unknown")
        return f"{country}, {city}, ZIP: {postal}"
    except Exception as e:
        print(f"Error fetching location for {ip}: {e}")
        return "Unknown"

def host_game_server(port):
    local_ip = get_local_ip()
    public_ip = get_public_ip()

    print(f"{Fore.RED}Local IP Address: {local_ip}")
    print(f"{Fore.RED}Public IP Address: {public_ip}")
    print(f"{Fore.YELLOW}Hosting game server on port {port}")

    print(f"{Fore.BLUE}\nLocal IP: {local_ip} | Public IP: {public_ip} | Port: {port}\n")

    current_location = get_location(public_ip)
    print(f"Your Location: {Fore.GREEN}{current_location}")

def update_progress_bar(duration):
    for percent in range(1, 101):
        sys.stdout.write("\r")
        sys.stdout.write(f"Updating: [{'=' * (percent // 10)}{' ' * ((100 - percent) // 10)}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / 100)
    sys.stdout.write("\n")
    print("Update completed!")

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main():
    global admin_logged_in
    admin_logged_in = False
    banner = f"""
{Fore.YELLOW}
███████╗██╗░██████╗░███╗░░░███╗░█████╗░██╗░░██╗░█████╗░░██████╗████████╗
██╔════╝██║██╔════╝░████╗░████║██╔══██╗██║░░██║██╔══██╗██╔════╝╚══██╔══╝
█████╗░░██║██║░░██╗░██╔████╔██║███████║███████║██║░░██║╚█████╗░░░░██║░░░
██╔══╝░░██║██║░░╚██╗██║╚██╔╝██║██╔══██║██╔══██║██║░░██║░╚═══██╗░░░██║░░░
██║░░░░░██║╚██████╔╝██║░╚═╝░██║██║░░██║██║░░██║╚█████╔╝██████╔╝░░░██║░░░
╚═╝░░░░░╚═╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░
{Style.RESET_ALL}
"""
    print(banner)
    
    while True:
        if admin_logged_in:
            choice = input("Say command: ")
        else:
            print("Enter 'Admin' to access the admin panel.")
            choice = input("Enter your choice: ")
        
        if choice.lower() == "admin":
            admin_logged_in = True
            port = input("Enter the port to host the game server: ")
            host_game_server(port)
            
        elif choice == "1":
            username = input("Login: ")
            password = input("Password: ")
            if authenticate(username, password):
                print("Login successful!")
                port = input("Enter the port to host the game server: ")
                host_game_server(port)
            else:
                print("Login failed.")
        elif choice == "2":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            create_user(username, password)
            print("User registered successfully!")
        elif choice == "3":
            break
        elif choice == "reload":
            print("Reloading...")
            subprocess.run(["python", os.path.basename(__file__)])
        elif choice == "update":
            print("Updating...")
            update_progress_bar(3)
            print("Successful update!")
        elif choice == "stop":
            sys.exit()
        elif choice == "help":
            print("Available commands:")
            print("reload - Restart the program")
            print("update - Update the program")
            print("stop - Stop the program")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

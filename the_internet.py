"""
File:    the_internet.py
Author:  Bliss Phinehas
Date:    11/29/2024
Description:
  This program simulates an internet with servers, allowing you to ping,
  traceroute, and connect servers while handling basic IPv4 validation.
"""

import re

# Dictionary to store server data and connections
servers = {}
connections = {}
current_server = None  # Tracks the currently selected server


def is_valid_ip(ip):
    """
    Validates if the given IP address is a valid IPv4 address.
    """
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True


def create_server(server_name, ip):
    """
    Creates a server with the given name and IP address.

    Arguments:
        server_name (str): The name of the server.
        ip (str): The IP address of the server.
    """
    if not is_valid_ip(ip):
        return f"Error: {ip} is not a valid IPv4 address."

    if server_name in servers:
        old_ip = servers[server_name]
        servers[server_name] = ip
        return (f"Success: A server with name {server_name} was created at IP {ip}, "
                f"overwriting the previous IP {old_ip}.")

    if ip in servers.values():
        return f"Error: The IP {ip} is already taken."

    servers[server_name] = ip
    return f"Success: A server with name {server_name} was created at IP {ip}."


def create_connection(server_1, server_2, connect_time):
    """
    Connects two servers with the given connection time in ms.
    """
    if server_1 not in servers or server_2 not in servers:
        return "Error: One or both servers do not exist."

    if server_1 == server_2:
        return "Error: Cannot connect a server to itself."

    if server_1 not in connections:
        connections[server_1] = {}
    if server_2 not in connections:
        connections[server_2] = {}

    if server_2 in connections[server_1]:
        return f"Error: {server_1} and {server_2} are already connected."

    connections[server_1][server_2] = connect_time
    connections[server_2][server_1] = connect_time
    return f"Success: {server_1} is now connected to {server_2}."


def set_server(server_name_or_ip):
    """
    Sets the current server by its name or IP address.
    """
    global current_server
    if server_name_or_ip in servers:
        current_server = server_name_or_ip
        return f"Server {server_name_or_ip} selected."
    elif server_name_or_ip in servers.values():
        current_server = server_name_or_ip
        return f"Server {server_name_or_ip} selected."
    else:
        return f"Error: The server {server_name_or_ip} does not exist."


def ping(target_server, visited=None):
    """
    Simulates a ping to the target server from the current server.
    """
    if visited is None:
        visited = set()
    if target_server == current_server:
        return "Error: Cannot ping the current server."

    if target_server not in servers:
        return f"Error: Server {target_server} does not exist."

    def ping_recursive(current, target, visited):
        if current == target:
            return 0
        visited.add(current)
        if current not in connections:
            return float('inf')

        min_time = float('inf')
        for neighbor, time in connections[current].items():
            if neighbor not in visited:
                time_to_target = ping_recursive(neighbor, target, visited)
                if time_to_target != float('inf'):
                    min_time = min(min_time, time + time_to_target)
        return min_time

    min_ping_time = ping_recursive(current_server, target_server, visited)
    if min_ping_time == float('inf'):
        return f"Error: No path to {target_server} found."

    return f"Ping successful to {target_server} with {min_ping_time}ms."


def traceroute(target_server, visited=None):
    """
    Simulates a traceroute to the target server from the current server.
    """
    if visited is None:
        visited = set()

    if target_server == current_server:
        return "Error: Cannot traceroute the current server."

    if target_server not in servers:
        return f"Error: Server {target_server} does not exist."

    def traceroute_recursive(current, target, visited, path, times):
        if current == target:
            return path, times
        visited.add(current)
        if current not in connections:
            return None, None

        for neighbor, time in connections[current].items():
            if neighbor not in visited:
                new_path, new_times = traceroute_recursive(
                    neighbor, target, visited, path + [neighbor], times + [time]
                )
                if new_path:
                    return new_path, new_times
        return None, None

    path, times = traceroute_recursive(current_server, target_server, visited, [current_server], [])
    if path is None:
        return f"Error: No path to {target_server} found."

    output = []
    for i, server in enumerate(path):
        time = times[i] if i < len(times) else 0
        output.append(f"{i}   {time}ms   [{servers[server]}]   {server}")

    return "\n".join(output)


def ip_config():
    """
    Displays the IP configuration of the current server.
    """
    if current_server is None:
        return "Error: No server selected."
    return f"Current server: {current_server} ({servers[current_server]})"


def display_servers():
    """
    Displays all available servers with their IP addresses.
    """
    output = []
    for server_name, ip in servers.items():
        output.append(f"{server_name} ({ip})")
    return "\n".join(output)


def run():
    """
    Main interaction loop for handling user commands.
    """
    while True:
        command = input(">>> ").strip().split()

        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "create-server":
            print(create_server(command[1], command[2]))
        elif cmd == "create-connection":
            print(create_connection(command[1], command[2], int(command[3])))
        elif cmd == "set-server":
            print(set_server(command[1]))
        elif cmd == "ping":
            print(ping(command[1]))
        elif cmd == "traceroute":
            print(traceroute(command[1]))
        elif cmd == "ip-config":
            print(ip_config())
        elif cmd == "display-servers":
            print(display_servers())
        elif cmd == "exit":
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    run()

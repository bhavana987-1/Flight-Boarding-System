import socket
import threading

def issue_boarding_pass(name, pnr_number, destination, seat_preference, special_meal, luggage_info, desired_time):
    boarding_pass = f"Boarding Pass for {name} (PNR: {pnr_number}):\n"
    boarding_pass += f"Destination: {destination}\n"
    boarding_pass += f"Seat Preference: {seat_preference}\n"
    boarding_pass += f"Special Meal: {special_meal}\n"
    boarding_pass += f"Luggage Information: {luggage_info}\n"
    boarding_pass += f"Desired Time: {desired_time}\n"
    return boarding_pass.strip()  # Remove trailing newline character

def ask_question(conn, question):
    conn.send(question.encode())
    return conn.recv(1024).decode()

def show_available_flights(conn, destination):
    # Define available flights based on destination and time
    # For demonstration, let's assume we have some flights available
    available_flights = {
        "Morning": 100.00,
        "Afternoon": 150.00,
        "Evening": 200.00,
        "Night": 180.00
    }

    # Send available flights information to the client
    conn.send(f"Available Flights for {destination}:\n".encode())
    for time, fare in available_flights.items():
        conn.send(f"{time}: ${fare}\n".encode())

def handle_client(conn, address):
    print(f"Connection from: {address}")

    conn.send("Welcome to the flight check-in process!\n".encode())

    conn.send("Have you already booked the flight? (yes/no): ".encode())
    try:
        booked_response = conn.recv(1024).decode().lower()
    except ConnectionResetError:
        print("Connection reset by the client.")
        conn.close()
        return

    if booked_response == "yes":
        try:
            name = ask_question(conn, "Please provide your full name as it appears on your ID: ")
            pnr_number = ask_question(conn, "Please provide your PNR number: ")

            # Assume verification is successful for demonstration purposes
            conn.send("Verification successful!\n".encode())

            conn.send("Thank you! Enjoy your flight.\n".encode())

        except ConnectionResetError:
            print("Connection reset by the client.")
            conn.close()
            return

    elif booked_response == "no":
        try:
            conn.send("Let's start the booking process!\n".encode())

            # Ask for user details
            name = ask_question(conn, "Please provide your full name as it appears on your ID: ")
            source = ask_question(conn, "Where are you flying from? ")
            destination = ask_question(conn, "Where are you flying to? ")

            # Show available flights
            show_available_flights(conn, destination)

            # Ask for desired time
            desired_time = ask_question(conn, "What time would you like to depart? ")

            # Ask for number of tickets
            num_tickets = ask_question(conn, "How many tickets would you like to book? ")

            # Send fixed fare and total cost
            fixed_fare = 180.00  # Fixed fare for demonstration purposes
            total_cost = float(num_tickets) * fixed_fare
            conn.send(f"Fixed fare for your selected flight: ${fixed_fare}\n".encode())
            conn.send(f"Total cost for {num_tickets} tickets: ${total_cost}\n".encode())

            # Confirm payment
            confirmation = ask_question(conn, "Would you like to confirm payment? (yes/no): ")
            if confirmation.lower() == "yes":
                conn.send("Payment successful!\n".encode())
                conn.send(issue_boarding_pass(name, "PNR123", destination, "Aisle", "No", "No", desired_time).encode())
            else:
                conn.send("Payment canceled.\n".encode())

        except ConnectionResetError:
            print("Connection reset by the client.")
            conn.close()
            return

    conn.close()

def server_program():
    host = '192.168.0.251'  # Change to '0.0.0.0' for connections from other devices
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    
    print(f"Server is listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept()
        
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()

if __name__ == '__main__':
    server_program()

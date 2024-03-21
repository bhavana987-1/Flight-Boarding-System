import socket
import tkinter as tk
from tkinter import messagebox


def book_flight():
    try:
        host = '10.30.202.92' '''change it the ip address of the system'''
        port = 5001

        client_socket = socket.socket()
        client_socket.connect((host, port))

        # Ask if the flight is already booked
        if messagebox.askyesno("Flight Booking", "Have you already booked the flight?"):
            messagebox.showinfo("Flight Booking", "You have already booked the flight. Thank you!")
            client_socket.close()
            return

        # Get user inputs from the GUI
        full_name = full_name_entry.get()
        flying_from = flying_from_entry.get()
        flying_to = flying_to_entry.get()
        departure_time = departure_time_var.get()
        num_tickets = int(num_tickets_entry.get())

        # Send the booking details to the server
        client_socket.send(f"{full_name},{flying_from},{flying_to}".encode())

        # Receive available flights and fares from the server
        available_flights_data = client_socket.recv(1024).decode()

        # Check if there are enough available seats
        if num_tickets <= 10:  # Assume 10 seats are available for each flight
            # Calculate total cost based on selected flight and number of tickets
            fare = {"Morning": 200, "Afternoon": 150, "Evening": 200, "Night": 180}[departure_time]
            total_cost = fare * num_tickets

            # Show payment confirmation dialog
            confirmation = messagebox.askyesno("Confirmation", f"Total cost: ${total_cost:.2f}\n\nConfirm payment?")
            if confirmation:
                client_socket.send(str(num_tickets).encode())
                messagebox.showinfo("Payment Successful", "Payment successful!")
            else:
                messagebox.showinfo("Payment Canceled", "Payment canceled.")
        else:
            messagebox.showinfo("No Availability", "No availability of seats. Please choose a lower number of tickets.")

        client_socket.close()

    except ConnectionAbortedError:
        messagebox.showerror("Connection Error", "Connection aborted. Please check your network settings.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
window = tk.Tk()
window.title("Flight Booking")

# Create and place widgets
tk.Label(window, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
full_name_entry = tk.Entry(window)
full_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Flying From:").grid(row=1, column=0, padx=5, pady=5)
flying_from_entry = tk.Entry(window)
flying_from_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(window, text="Flying To:").grid(row=2, column=0, padx=5, pady=5)
flying_to_entry = tk.Entry(window)
flying_to_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(window, text="Departure Time:").grid(row=3, column=0, padx=5, pady=5)
departure_time_var = tk.StringVar(window)
departure_time_var.set("Morning")  # Default value
departure_time_dropdown = tk.OptionMenu(window, departure_time_var, "Morning", "Afternoon", "Evening", "Night")
departure_time_dropdown.grid(row=3, column=1, padx=5, pady=5)

tk.Label(window, text="Number of Tickets:").grid(row=4, column=0, padx=5, pady=5)
num_tickets_entry = tk.Entry(window)
num_tickets_entry.grid(row=4, column=1, padx=5, pady=5)

book_button = tk.Button(window, text="Book Flight", command=book_flight)
book_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Run the application
window.mainloop()

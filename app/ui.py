import tkinter as tk
from tkinter import ttk
from app.queue_logic import PriorityQueue
from app.utils import validate_age  # Add utility to validate age

def draw_door(canvas):
    # Draw the door
    door_width = 100
    door_height = 200
    
    # Draw the door rectangle (x1, y1, x2, y2)
    canvas.create_rectangle(150, 50, 150 + door_width, 50 + door_height, fill="brown", outline="black")

    # Draw the door handle (small circle)
    handle_radius = 10
    canvas.create_oval(150 + door_width - 30, 50 + door_height // 2 - handle_radius, 
                       150 + door_width - 30 + handle_radius * 2, 50 + door_height // 2 + handle_radius, 
                       fill="gold", outline="black")

    # Draw a simple doorframe (optional)
    canvas.create_rectangle(140, 40, 150 + door_width, 50 + door_height, outline="black", width=3)

# Initialize the queue
queue = PriorityQueue()

# Create a global message label for displaying messages
message_label = None

def update_queue_display(queue_frame):
    # Clear the frame
    for widget in queue_frame.winfo_children():
        widget.destroy()

    # Display the current queue
    patients = queue.get_queue()
    if not patients:
        ttk.Label(queue_frame, text="Queue is empty.", font=("Arial", 14)).pack()
    else:
        for age, name in patients:
            ttk.Label(queue_frame, text=f"{age} ({name} years old)", font=("Arial", 14)).pack()

def update_message(message):
    # Update the message label with a new message
    if message_label:
        message_label.config(text=message)

def view_queue():
    queue_list = queue.get_queue()  # Get the current queue
    if queue_list:
        # Format the queue into a string for display
        formatted_queue = "\n".join([f"{name} (Age: {age})" for name, age in queue_list])
        update_message(f"Current Queue:\n{formatted_queue}")
    else:
        update_message("The queue is empty.")


def add_patient(name_entry, age_entry, queue_frame):
    name = name_entry.get()
    age = validate_age(age_entry.get())
    if name and age:
        queue.add_patient(name, age)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        update_queue_display(queue_frame)
        update_message(f"Patient {name} ({age} years old) added to the queue.")
    else:
        update_message("Invalid input! Please provide a valid name and age.")
def call_patient(queue_frame):
    patient = queue.call_patient()
    if patient:
        update_message(f"Called patient: {patient}")
    else:
        update_message("No patients in the queue.")

    # Refresh the queue display without reordering
    update_queue_display(queue_frame)


def remove_patient(name_entry, queue_frame):
    name = name_entry.get()
    if name:
        queue.remove_patient(name)
        name_entry.delete(0, tk.END)
        update_queue_display(queue_frame)
        update_message(f"Patient {name} removed from the queue.")
    else:
        update_message("Please provide a valid name.")

def clear_queue(queue_frame):
    queue.queue = []
    update_queue_display(queue_frame)
    update_message("All patients removed from the queue.")

def display_queue_length(queue_frame):
    length = len(queue.queue)
    update_message(f"Queue length: {length} patients.")
    update_queue_display(queue_frame)

def check_next_patient(queue_frame):
    patient = queue.get_queue()[0] if queue.queue else None
    if patient:
        update_message(f"Next patient: {patient[0]} ({patient[1]} years old)")
    else:
        update_message("No patients in the queue.")

def update_patient_ui(name_entry, age_entry, queue_frame):
    # Create a new window for updating a patient
    update_window = tk.Toplevel()
    update_window.title("Update Patient Details")
    update_window.geometry("400x300")

    # Get the list of patients for the dropdown (combo box)
    patients = queue.get_queue()
    # Format each patient as "Name (Age years old)" for the combobox
    patient_details = [f"{name} ({age} years old)" for name, age in patients]

    # Dropdown (Combobox) for selecting the patient to update
    ttk.Label(update_window, text="Select Patient:").pack(pady=5)
    selected_patient = ttk.Combobox(update_window, values=patient_details)
    selected_patient.pack(pady=5)

    # Entry fields for updating patient details
    ttk.Label(update_window, text="Name:").pack(pady=5)
    name_entry = ttk.Entry(update_window)
    name_entry.pack(pady=5)

    ttk.Label(update_window, text="Age:").pack(pady=5)
    age_entry = ttk.Entry(update_window)
    age_entry.pack(pady=5)

    def load_patient_details():
        patient_detail = selected_patient.get()
        # Extract the name and age from the selected patient detail string
        if patient_detail:
            # Split the formatted string into name and age
            selected_name, selected_age = patient_detail.split(" (")
            selected_age = selected_age.replace(" years old)", "")  # Clean the age part

            # Populate the entry fields
            name_entry.delete(0, tk.END)
            name_entry.insert(0, selected_name)
            age_entry.delete(0, tk.END)
            age_entry.insert(0, selected_age)

    # Button to load the selected patient's details into the fields
    load_button = ttk.Button(update_window, text="Load Details", command=load_patient_details)
    load_button.pack(pady=5)

    # Save button to save updated details
    def save_updates():
        new_name = name_entry.get()
        new_age = validate_age(age_entry.get())  # Validate new age input
        if new_name and new_age:
            old_name = selected_patient.get().split(" (")[0]  # Extract the old name from the combo box text
            # Remove the old patient and add the updated one
            queue.remove_patient(old_name)
            queue.add_patient(new_name, new_age)
            update_message(f"Patient {old_name} updated to {new_name} ({new_age} years old).")
            update_queue_display(queue_frame)  # Refresh the queue display
            update_window.destroy()  # Close the update window
        else:
            update_message("Invalid input! Please provide a valid name and age.")

    save_button = ttk.Button(update_window, text="Save", command=save_updates)
    save_button.pack(pady=20)

    # Start the update window's event loop
    update_window.mainloop()


def launch_app():
    global message_label
    # Create the main window
    root = tk.Tk()
    root.title("CareFirst Hospital - Priority Queue")
    root.geometry("1000x800")
    root.resizable(False, False)

    # Add title label
    ttk.Label(root, text="Welcome to CareFirst Hospital", font=("Arial", 20)).pack(pady=20)
    
    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack()
    draw_door(canvas)

    # Queue visualization area
    queue_frame = ttk.Frame(root, padding=10)
    queue_frame.pack(fill="both", expand=True)
    update_queue_display(queue_frame)  # Initialize the queue display

    # Entry fields for adding patients
    entry_frame = ttk.Frame(root, padding=10)
    entry_frame.pack(fill="x", padx=20)

    ttk.Label(entry_frame, text="Name:").pack(side="left", padx=5)
    name_entry = ttk.Entry(entry_frame)
    name_entry.pack(side="left", padx=5)

    ttk.Label(entry_frame, text="Age:").pack(side="left", padx=5)
    age_entry = ttk.Entry(entry_frame)
    age_entry.pack(side="left", padx=5)

    # Buttons for actions
    button_frame = ttk.Frame(root, padding=10)
    button_frame.pack(side="bottom", fill="x")

    # Define button commands in a list
    button_commands = [
        lambda: add_patient(name_entry, age_entry, queue_frame),
        lambda: call_patient(queue_frame),
        view_queue,
        lambda: remove_patient(name_entry, queue_frame),
        lambda: clear_queue(queue_frame),
        lambda: display_queue_length(queue_frame),
        lambda: check_next_patient(queue_frame),
        lambda: update_patient_ui(name_entry, age_entry, queue_frame)  # Update button command
    ]
    
    # Create a grid of buttons with equal width
    button_texts = [
        "Add Patient", "Call Patient", "View Queue", "Remove Patient", 
        "Clear Queue", "Queue Length", "Check Next Patient", "Update Patient"  # New Update button
    ]
    for i, text in enumerate(button_texts):
        button = ttk.Button(button_frame, text=text, command=button_commands[i])
        button.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

    # Make the columns expand equally
    for i in range(len(button_texts)):
        button_frame.grid_columnconfigure(i, weight=1)

    # Message display area at the bottom
    message_label = ttk.Label(root, text="Welcome to CareFirst Hospital", font=("Arial", 14), foreground="green")
    message_label.pack(side="bottom", pady=15)

    # Start the Tkinter main loop
    root.mainloop()

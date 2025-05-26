import tkinter as tk
# GUI Framework
import json
# JavaScript Object Notation are plain text files
import fnmatch
# Import the fnmatch module for matching

# Creates class Partner with parameters
class Partner:
    def __init__(self, name, org_type, resources, contact_person, contact_email, contact_phone):
        self.name = name
        self.org_type = org_type
        self.resources = resources
        self.contact_person = contact_person
        self.contact_email = contact_email
        self.contact_phone = contact_phone

# Creates class PartnerDatabase for storing partners
class PartnerDatabase:
    def __init__(self):
        self.partners = []

    # Adds partner
    def add_partner(self, partner):
        self.partners.append(partner)

    # Converts the list of partner objects into a dictionary format for JSON
    def to_dict(self):
        return {"partners": [
            {"name": partner.name,
             "org_type": partner.org_type,
             "resources": partner.resources,
             "contact_person": partner.contact_person,
             "contact_email": partner.contact_email,
             "contact_phone": partner.contact_phone}
            for partner in self.partners
        ]}

    # Deserializes JSON objects
    def from_dict(self, data):
        self.partners = [Partner(**partner) for partner in data["partners"]]

    # Saves partner to database
    def save_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file)

    # Pulls partner from database
    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.from_dict(data)
        except FileNotFoundError:
            pass    # Ignore if the file is not found

    # Use fnmatch to perform matching
    def search_partners(self, keyword):
        return [partner for partner in self.partners if fnmatch.fnmatch(partner.name.lower(), keyword.lower())
                or fnmatch.fnmatch(partner.org_type.lower(), keyword.lower())]

    # Use fnmatch to perform matching for organization type
    def filter_partners(self, org_type):
        return [partner for partner in self.partners if fnmatch.fnmatch(partner.org_type.lower(), org_type.lower())]


# Declare global variables
name_entry, org_type_entry, resources_entry, contact_person_entry, contact_email_entry, contact_phone_entry = None, None, None, None, None, None
search_entry, filter_entry, results, status_label = None, None, None, None
display_all_button, clear_output_button = None, None


# Function to add partners and check errors
def add_partner():
    name = name_entry.get()
    org_type = org_type_entry.get()
    resources = resources_entry.get()
    contact_person = contact_person_entry.get()
    contact_email = contact_email_entry.get()
    contact_phone = contact_phone_entry.get()

    if name and org_type and resources and contact_person and contact_email and contact_phone:
        partner = Partner(name, org_type, resources, contact_person, contact_email, contact_phone)
        partner_db.add_partner(partner)
        partner_db.save_to_file("partners.json")  # Save the database to partners.json
        status_label.config(text="Partner added successfully.", fg="green")
    else:
        status_label.config(text="Please fill in all fields.", fg="red")


# Function to searching partners
def search_partner():
    keyword = search_entry.get().lower()
    if keyword:
        search_results = [partner for partner in partner_db.partners if
                          any(word.startswith(keyword) for word in partner.name.lower().split())]
        display_results(search_results)
    else:
        status_label.config(text="Please enter a keyword to search.", fg="red")


# Function to filtering partners
def filter_partner():
    org_type = filter_entry.get().lower()
    if org_type:
        filter_results = [partner for partner in partner_db.partners if
                          any(word.startswith(org_type) for word in partner.org_type.lower().split())]
        display_results(filter_results)
    else:
        status_label.config(text="Please enter an organization type to filter.", fg="red")


# Function to display all stored data
def display_all():
    display_results(partner_db.partners)


# Function to display search, filter, or all results alphabetically
def display_results(display_results):
    results.config(state=tk.NORMAL)  # Enable editing
    results.delete(1.0, tk.END)  # Clear previous results

    if display_results:
        # Sort partners alphabetically
        sorted_results = sorted(display_results, key=lambda partner: partner.name.lower())
        for partner in sorted_results:
            results.insert(tk.END, f"Name: {partner.name}\n")
            results.insert(tk.END, f"Organization Type: {partner.org_type}\n")
            results.insert(tk.END, f"Resources: {partner.resources}\n")
            results.insert(tk.END, f"Contact Person: {partner.contact_person}\n")
            results.insert(tk.END, f"Contact Email: {partner.contact_email}\n")
            results.insert(tk.END, f"Contact Phone: {partner.contact_phone}\n\n")
    else:
        results.insert(tk.END, "No matching partners found.\n")

    results.config(state=tk.DISABLED)  # Disable editing


# Function to clear results
def clear_output():
    results.config(state=tk.NORMAL)  # Enable editing
    results.delete(1.0, tk.END)  # Clear all text
    results.config(state=tk.DISABLED)  # Disable editing


# Create main application window
root = tk.Tk()
root.title("Partner Management System")

# Create PartnerDatabase
partner_db = PartnerDatabase()
partner_db.load_from_file("partners.json")  # Load the database from a file

# Background color
root.configure(bg="lightblue")

# Load the background image
background_image = tk.PhotoImage(file="wildcat.png")  # Replace "wildcat.png" with the actual image file path
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=0.5, relheight=1)

# Create a frame for the input and output
input_output_frame = tk.Frame(root, bg="lightblue")
input_output_frame.place(relx=0.5, relwidth=0.5, relheight=1)

# GUI
tk.Label(input_output_frame, text="Partner Name:", bg="lightblue").grid(row=0, column=0, pady=5, padx=20, sticky="w")
name_entry = tk.Entry(input_output_frame)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(input_output_frame, text="Organization Type:", bg="lightblue").grid(row=1, column=0, pady=5, padx=20,
                                                                             sticky="w")
org_type_entry = tk.Entry(input_output_frame)
org_type_entry.grid(row=1, column=1, pady=5)

tk.Label(input_output_frame, text="Resources:", bg="lightblue").grid(row=2, column=0, pady=5, padx=20, sticky="w")
resources_entry = tk.Entry(input_output_frame)
resources_entry.grid(row=2, column=1, pady=5)

tk.Label(input_output_frame, text="Contact Person:", bg="lightblue").grid(row=3, column=0, pady=5, padx=20, sticky="w")
contact_person_entry = tk.Entry(input_output_frame)
contact_person_entry.grid(row=3, column=1, pady=5)

tk.Label(input_output_frame, text="Contact Email:", bg="lightblue").grid(row=4, column=0, pady=5, padx=20, sticky="w")
contact_email_entry = tk.Entry(input_output_frame)
contact_email_entry.grid(row=4, column=1, pady=5)

tk.Label(input_output_frame, text="Contact Phone:", bg="lightblue").grid(row=5, column=0, pady=5, padx=20, sticky="w")
contact_phone_entry = tk.Entry(input_output_frame)
contact_phone_entry.grid(row=5, column=1, pady=5)

add_button = tk.Button(input_output_frame, text="Add Partner", command=add_partner, bg="green", fg="white")
add_button.grid(row=6, column=0, columnspan=2, pady=10)

# Search functionality
tk.Label(input_output_frame, text="Search by Partner:", bg="lightblue").grid(row=7, column=0, pady=5, padx=20,
                                                                             sticky="w")
search_entry = tk.Entry(input_output_frame)
search_entry.grid(row=7, column=1, pady=5)
search_button = tk.Button(input_output_frame, text="Search", command=search_partner, bg="blue", fg="white")
search_button.grid(row=8, column=0, columnspan=2, pady=5)

# Filter functionality
tk.Label(input_output_frame, text="Filter by Organization Type:", bg="lightblue").grid(row=9, column=0, pady=5, padx=20,
                                                                                       sticky="w")
filter_entry = tk.Entry(input_output_frame)
filter_entry.grid(row=9, column=1, pady=5)
filter_button = tk.Button(input_output_frame, text="Filter", command=filter_partner, bg="blue", fg="white")
filter_button.grid(row=10, column=0, columnspan=2, pady=5)

results = tk.Text(input_output_frame, height=10, width=60, bg="lightgray")
results.grid(row=11, column=0, columnspan=2, pady=10)

status_label = tk.Label(input_output_frame, text="", bg="lightblue", fg="green")
status_label.grid(row=12, column=0, columnspan=2, pady=10)

# Set the size of the window
initial_width = background_image.width() * 2
initial_height = background_image.height()
root.geometry(f"{initial_width}x{initial_height}")

# Create buttons
display_all_button = tk.Button(input_output_frame, text="Display All", command=display_all)
display_all_button.grid(row=13, column=0, pady=5, padx=20, sticky="w")

clear_output_button = tk.Button(input_output_frame, text="Clear Output", command=clear_output)
clear_output_button.grid(row=13, column=1, pady=5, sticky="e")

root.mainloop()

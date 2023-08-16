import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Complaint:
    def __init__(self, complaint_id, customer_name, complaint_text):
        self.complaint_id = complaint_id
        self.customer_name = customer_name
        self.complaint_text = complaint_text
        self.resolved = False


class ComplaintDatabase:
    def __init__(self):
        self.complaints = []

    def add_complaint(self, complaint):
        self.complaints.append(complaint)

    def resolve_complaint(self, complaint_id):
        for complaint in self.complaints:
            if complaint.complaint_id == complaint_id:
                complaint.resolved = True
                return True
        return False

    def get_unresolved_complaints(self):
        return [complaint for complaint in self.complaints if not complaint.resolved]


class ComplaintManagementSystem:
    def __init__(self):
        self.complaint_db = ComplaintDatabase()
        self.logged_in_user = None

    def encourage_complaints(self, customer_name, complaint_text):
        complaint_id = len(self.complaint_db.complaints) + 1
        complaint = Complaint(complaint_id, customer_name, complaint_text)
        self.complaint_db.add_complaint(complaint)
        return complaint_id

    def resolve_complaint(self, complaint_id):
        return self.complaint_db.resolve_complaint(complaint_id)

    def get_unresolved_complaints(self):
        return self.complaint_db.get_unresolved_complaints()

    def login(self, username, password):
        # For simplicity, using hardcoded credentials
        if username == "admin" and password == "adminpass":
            self.logged_in_user = username
            return True
        return False

    def send_email_notification(self, customer_name, complaint_text):
        sender_email = "your_email@example.com"
        sender_password = "your_email_password"
        recipient_email = "recipient@example.com"

        subject = "New Complaint Submission"
        message = f"Customer: {customer_name}\nComplaint: {complaint_text}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            print("Email notification sent successfully")
        except Exception as e:
            print("Failed to send email notification:", e)


class GUI:
    def __init__(self, cms):
        self.cms = cms
        self.root = tk.Tk()
        self.root.title("Complaint Management System")

        self.label_username = tk.Label(self.root, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        self.label_password = tk.Label(self.root, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

        self.root.mainloop()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.cms.login(username, password):
            self.root.destroy()
            self.show_main_window()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_main_window(self):
        main_window = tk.Tk()
        main_window.title("Complaint Management System - Main Menu")

        unresolved_complaints = self.cms.get_unresolved_complaints()
        unresolved_text = "\n".join(
            [f"ID: {c.complaint_id}, Customer: {c.customer_name}, Complaint: {c.complaint_text}" for c in
             unresolved_complaints])

        self.unresolved_label = tk.Label(main_window, text="Unresolved Complaints:")
        self.unresolved_label.pack()

        self.unresolved_text = tk.Text(main_window, height=10, width=50)
        self.unresolved_text.insert(tk.END, unresolved_text)
        self.unresolved_text.pack()

        self.resolve_button = tk.Button(main_window, text="Resolve Complaint", command=self.resolve_complaint)
        self.resolve_button.pack()

        self.new_complaint_label = tk.Label(main_window, text="New Complaint:")
        self.new_complaint_label.pack()

        self.label_name = tk.Label(main_window, text="Customer Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(main_window)
        self.entry_name.pack()

        self.label_complaint = tk.Label(main_window, text="Complaint Text:")
        self.label_complaint.pack()
        self.entry_complaint = tk.Entry(main_window)
        self.entry_complaint.pack()

        self.submit_button = tk.Button(main_window, text="Submit Complaint", command=self.submit_complaint)
        self.submit_button.pack()

        main_window.mainloop()

    def resolve_complaint(self):
        complaint_id = simpledialog.askinteger("Resolve Complaint", "Enter Complaint ID:")
        if complaint_id is not None:
            if self.cms.resolve_complaint(complaint_id):
                messagebox.showinfo("Success", "Complaint resolved")
            else:
                messagebox.showerror("Error", "Invalid Complaint ID")

    def submit_complaint(self):
        customer_name = self.entry_name.get()
        complaint_text = self.entry_complaint.get()
        complaint_id = self.cms.encourage_complaints(customer_name, complaint_text)

        self.cms.send_email_notification(customer_name, complaint_text)

        messagebox.showinfo("Success", f"Complaint submitted. Your complaint ID: {complaint_id}")
        self.entry_name.delete(0, tk.END)
        self.entry_complaint.delete(0, tk.END)


if __name__ == "__main__":
    cms = ComplaintManagementSystem()

    # Encourage complaints
    complaint_id_1 = cms.encourage_complaints("jaswanth mathan", "Poor customer service")
    complaint_id_2 = cms.encourage_complaints("mathan", "Incorrect billing")

    gui = GUI(cms)

import tkinter as tk
from tkinter import messagebox
import requests
import uuid

mac = hex(uuid.getnode()).replace('0x', '').upper()

# Format the MAC address
mac = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))
templates = [
    "PayPal", "Venmo", "CashApp", "Western_Union", "Citi_Bank", "Wells_Fargo", 
    "Capital_One", "US_Bank", "Bank_of_America", "Coinbase", "Blockchain", 
    "Binance", "Metamask", "Norton360", "McAfee", "Webroot", "Trendmicro", 
    "Geek_Squad", "Bestbuy", "Home_Depot", "Target", "Walmart", "Amazon", "Netflix"
] 
 
class LoginDialog:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Dialog")

        # Username Label and Entry
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(master,width=30)
        self.username_entry.pack(pady=5,padx=20)

        # Password Label and Entry
        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(master,width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def save_token(self,token):
        with open('token.txt', 'w') as file:
            file.write(token)

    def load_token(self):
        try:
            with open('token.txt', 'r') as file:
                token=file.read()
                print(token)
                return token
        except FileNotFoundError:
            return None
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(mac)
        response = requests.post('http://3.26.202.39/api/auth/login', json={
            'username': username,
            'password': password,
            'mac':mac,
        })
        print(response)
        if response.status_code != 200:
            messagebox.showwarning("info","Login failed.")
            return

        token = response.json().get('token')
        if not token:
            messagebox.showerror("Login Failed", "There are 4 PCs")
            return 
        self.save_token(token)
        print(token)
        messagebox.showinfo("info","Login successful!")
        self.master.quit()
        self.open_success_dialog(self.master)  # Open the new dialog
            
    def open_success_dialog(self,root):
        root.withdraw()
        self.success_window = tk.Toplevel(root) 
        self.success_window.title("Email Template Selector")
        self.success_window.geometry("800x600")  # Increased width and height for more space
        self.success_window.configure(bg="#FFA500")  # Shiny orange background

        # Display the 24 templates as buttons
        label = tk.Label(self.success_window, text="Select an Email Template", font=("Arial", 14), bg="#FFA500")
        label.pack(pady=10)

        frame = tk.Frame(self.success_window, bg="#FFA500")
        frame.pack(pady=10)

        # Create a button for each template with adjusted width
        buttons_per_row = 4  # Reduced number of buttons per row
        for i, template in enumerate(templates):
            rb = tk.Button(frame, text=template, font=("Arial", 12, "bold"), bg="black", fg="yellow",
                        relief="raised", width=15, height=2,  # Adjusted width
                        command=lambda t=template: self.submit_template(t))  # Pass the template name
            rb.grid(row=i // buttons_per_row, column=i % buttons_per_row, padx=5, pady=5)  # Adjusted padding

        # Submit button to run the selected template
        submit_button = tk.Button(self.success_window, text="Submit", command=lambda: self.submit_template(template_var.get()), 
                                bg="black", fg="#FFA500", font=("Arial", 12, "bold"), width=15)  # Adjusted width
        submit_button.pack(pady=10)

        # Quit button to exit the application
        quit_button = tk.Button(self.success_window, text="Quit", command=self.quit_app, 
                                bg="black", fg="#FFA500", font=("Arial", 12, "bold"), width=15)  # Adjusted width
        quit_button.pack(pady=10)

        # Footer label
        footer_label = tk.Label(self.success_window, text="IA Mailer V2.1🤖", font=("Arial", 16, "bold"), bg="#FFA500", fg="black")
        footer_label.pack(side="bottom", pady=10)
        self.success_window.mainloop()
        
    def execute_template(self,template_name):
        token = self.load_token()
        print(token)
        
        response = requests.post('http://3.26.202.39/api/auth/Mac/check', json={
            'token': token, 
        })
        print(response)
        if response.status_code != 200:
            messagebox.showerror("Login Failed", "Your session destroyed")
             
            self.success_window.quit() 
            return
        
        available = response.json().get('available')
        if not available:
            return  
        
        root = tk.Toplevel(self.master) 
        match template_name:
            case "Amazon":
                from Amazon import EmailApp
                app = EmailApp(root)
                return
            case "Bestbuy":
                from Bestbuy import EmailApp
                app = EmailApp(root)
                return
            case "PayPal":
                from PayPal import EmailApp
                app = EmailApp(root)
                return
            case "Venmo":
                from Venmo import EmailApp
                app = EmailApp(root)
                return
            case "CashApp":
                from Cashapp import EmailApp
                app = EmailApp(root)
                return
            case "Western_Union":
                from Western_Union import EmailApp
                app = EmailApp(root)
                return
            case "Citi_Bank":
                from Citi_Bank import EmailApp
                app = EmailApp(root)
                return
            case "Wells_Fargo":
                from Wells_Fargo import EmailApp
                app = EmailApp(root)
                return
            case "Capital_One":
                from Capital_One import EmailApp
                app = EmailApp(root)
                return
            case "US_Bank":
                from US_Bank import EmailApp
                app = EmailApp(root)
                return
            case "Bank_of_America":
                from Bank_of_America import EmailApp
                app = EmailApp(root)
                return
            case "Coinbase":
                from Coinbase import EmailApp
                app = EmailApp(root)
                return
            case "Blockchain":
                from Blockchain import EmailApp
                app = EmailApp(root)
                return
            case "Binance":
                from Binance import EmailApp
                app = EmailApp(root)
                return
            case "Metamask":
                from Metamask import EmailApp
                app = EmailApp(root)
                return
            case "Norton360":
                from Norton360 import EmailApp
                app = EmailApp(root)
                return
            case "McAfee":
                from McAfee import EmailApp
                app = EmailApp(root)
                return
            case "Webroot":
                from Webroot import EmailApp
                app = EmailApp(root)
                return
            case "Trendmicro":
                from Trendmicro import EmailApp
                app = EmailApp(root)
                return
            case "Geek_Squad":
                from Geek_Squad import EmailApp
                app = EmailApp(root)
                return
            case "Home_Depot":
                from Home_Depot import EmailApp
                app = EmailApp(root)
                return
            case "Target":
                from Target import EmailApp
                app = EmailApp(root)
                return
            case "Walmart":
                from Walmart import EmailApp
                app = EmailApp(root)
                return
            case "Netflix":
                from Netflix import EmailApp
                app = EmailApp(root)
                return
            
        root.mainloop()
    def logout(self):
        token = self.load_token()
        print(token)
        
        response = requests.post('http://3.26.202.39/api/auth/user/logout', json={
            'token': token, 
        })
        print(response)
        if response.status_code != 200:
            messagebox.showerror("Logout Failed", "Logout Failed")
            self.success_window.quit() 
            return
        messagebox.showinfo("info","logout successful!")
        

    def submit_template(self,template_name):
        if template_name:
            self.execute_template(template_name)
        else:
            messagebox.showwarning("No Selection", "Please select a template to continue.")
        # Function to quit the application
    def quit_app(self): 
        self.logout()
        self.success_window.withdraw()
        self.success_window.quit()    

     

if __name__ == "__main__":
    root = tk.Tk()
    login_dialog = LoginDialog(root)
    root.mainloop()

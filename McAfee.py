import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import threading
from datetime import datetime
import logging
import sys
import ssl
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
from threading import Thread, Event

# Setup logging
log_file_path = "mailer.log"
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EmailSender:
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.is_running = False
        self.is_paused = False

    def send_email(self, smtp_details, receiver_email, server):
        from_address = smtp_details['sender_email']
        firm_name = random.choice(self.get_firm_names())
        intro_phrase = get_random_intro_phrase()
        amount = f"${random.uniform(280.50, 1600.50):.2f}"
        payment_method = f"MCFE ****{random.randint(10000, 99999)}"

        # Generate a random name
        full_name = get_random_name()

        # Create email
        msg = MIMEMultipart()
        msg['From'] = f"{smtp_details['sender_name']} <{from_address}>"
        msg['To'] = receiver_email
        msg['Subject'] = f"Your {random.choice(['Summary', 'Record', 'Breakdown', 'Overview', 'Account', 'Details', 'Report', 'Notice', 'Documentation', 'Recordkeeping', 'Ledger', 'Dossier', 'eTransact File', ' Transfer Sheet', 'Memorandum of paymanet', 'Update', 'Log', 'Description', 'Snapshot', 'Summary Sheet', 'payment Sheet', 'Brief', 'Record Sheet', 'Payment Overview ', 'Summary Report', 'In Transit Case', 'Logbook of transfer', 'transaction Summary', 'Briefing of payment', 'Information Sheet', 'Payment Profile', 'eTransact Log', 'eTransact Overview', 'Recap of details', 'Payment Register'])} from {firm_name}"

        # Email body with HTML content
        body = self.create_email_body(receiver_email, intro_phrase, firm_name, amount, payment_method, smtp_details, full_name)
        msg.attach(MIMEText(body, 'html'))

        # Send email
        try:
            self.log_callback(f"Preparing to send email to {receiver_email}...")
            server.sendmail(from_address, receiver_email, msg.as_string())
            self.log_callback(f"Email sent to {receiver_email}")
        except Exception as e:
            error_message = f"Failed to send email to {receiver_email}: {e}"
            logging.error(error_message)
            self.log_callback(error_message)

    def create_email_body(self, receiver_email, intro_phrase, firm_name, amount, payment_method, smtp_details, full_name):
        return f"""
        <html>
        <head>
            <style>
                .header, .footer {{
                    font-size: 12px;
                    color: #999;
                    margin-bottom: 20px;
                    text-align: center;
                }}
                .unsubscribe {{
                    font-size: 12px;
                    color: #999;
                    text-align: center;
                }}
            /* Watermark Style */
            .watermark {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                width: 100%;
                height: 100%;
                color: rgba(128, 0, 0, 0.3); /* Adjust transparency here */
                font-size: 50px; /* Adjust font size as needed */
                font-weight: bold;
                text-align: center;
                transform: rotate(-45deg); /* Rotate the text */
                transform-origin: center;
                pointer-events: none; /* Prevent the watermark from interfering with other content */
                z-index: 0; /* Send the watermark behind other content */
            }}
            .content {{
                position: relative; /* Ensure the content appears above the watermark */
                z-index: 1; /* Ensure content is above the watermark */
                padding: 20px; /* Add some padding for aesthetics */
            }}
        </style>
    </head>
    <body>
        <div class="watermark">【﻿ＭｃＡｆｅｅ】</div> <!-- Watermark element -->
        
        <div class="content"> <!-- Content wrapper to ensure content is above the watermark -->
            <div class="header">
                 
            </div>
            <p class="header" style="text-align: left;"><strong><em>Invoice for {receiver_email}</em></strong></p>

            <p><span style="color: #2a75ee; font-weight: bold;">{intro_phrase} {firm_name}</span></p>

            <p>{firm_name}: A payment of <b>{amount}</b> has been processed via {payment_method}.</p>

            <p>This is the <b>{random.choice(['receipt', 'invoice', 'order'])}</b> description. For more deails, please get in touch with us.</p>
	    <p>Customer Service USA & Canada <strong>{smtp_details['tfn']}</strong></p>

            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; max-width: 600px;">
                <tr>
                    <th style="text-align: left; padding: 8px;">Order Value</th>
                    <td style="text-align: left; padding: 8px;">{amount}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px;">Order Date</th>
                    <td style="text-align: left; padding: 8px;">{datetime.now().strftime("%A, %B %d, %Y")}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px;">Reference Number</th>
                    <td style="text-align: left; padding: 8px;">MCFE{random.randint(100000, 999999)}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px;">Description</th>
                    <td style="text-align: left; padding: 8px;">iSEC36O MCFE – {random.randint(2, 6)} Years</td>
                </tr>
            </table>

            <p>Get in touch if you need to modify or cancel your order.</p>
            <p><span class="tfn" style="color: #6495ED; font-weight: bold; font-size: 1.2em;">Customer Service USA & Canada {smtp_details['tfn']}</span></p>
            <p><strong>{full_name}</strong></p>
            <p>{get_random_address()}</p>
	    <p style="text-align: left;"><strong><span style='font-size:29px;font-family:"Segoe UI Symbol",sans-serif;color:#C00000;'>⛊</span><span style='font-size:37px;font-family:"Segoe UI Symbol",sans-serif;color:black;'>&nbsp;</span><span style='font-size:35px;font-family:"Segoe UI Semibold",sans-serif;color:#C00000;'>M</span><span style='font-size:7px;font-family:"Segoe UI Semibold",sans-serif;color:white;'>.</span><span style='font-size:35px;font-family:"Segoe UI Semibold",sans-serif;color:#C00000;'>c</span><span style='font-size:7px;font-family:"Segoe UI Semibold",sans-serif;color:white;'>.&nbsp;</span><span style='font-size:35px;font-family:"Segoe UI Semibold",sans-serif;color:black;'>A</span><span style='font-size:7px;font-family:"Segoe UI Semibold",sans-serif;color:white;'>.</span><span style='font-size:35px;font-family:"Segoe UI Semibold",sans-serif;color:black;'>f</span><span style='font-size:7px;font-family:"Segoe UI Semibold",sans-serif;color:white;'>.</span><span style='font-size:35px;font-family:"Segoe UI Semibold",sans-serif;color:black;'>e</span><span style='font-size:7px;font-family:"Segoe UI Semibold",sans-serif;color:white;'>.</span><span style='font-size:35px;font-family:"Segoe UI Semibold",sans-serif;color:black;'>e</span></strong><span style='font-size:35px;font-family:"Segoe UI Black",sans-serif;color:#C00000;'>&nbsp;</span><sup><span style='font-size:29px;font-family:"Calibri",sans-serif;'>&trade;</span></sup></p>

            <p class="unsubscribe">If you wish to unsubscribe, click <a href="#">here</a>.</p>

            <div class="footer">
                <p>{get_random_quote()}</p>
                <p>{get_random_address()}</p>
            </div>
        </body>
        </html>
        """

    def get_firm_names(self):
        return [

            'Info Wave LLC', 
            'Safe Protect Inc', 
            'Cyber Secure LLC', 
            'Trust Net Inc', 
            'Secure Point LLC',
	    'Guard Vault Inc',
	    'Data Secure LLC',
            'Shield Safe Inc',
            'Safe Guard LLC',
            'Cybersecure Solutions Inc', 
            'Secure Web LLC', 
            'Trust Safe Inc', 
            'Protect Wise LLC',
	    'Secure Guard Inc',
	    'Guard Logic LLC',
            'Info Armor Inc',
            'Data Safe LLC',
            'Safe Link Inc', 
            'Cyber Sphere LLC', 
            'Secure Protect Inc', 
            'Trust Tech LLC',
	    'Guard Wise Inc',
	    'Info Guard LLC',
            'Securenet Solutions Inc',
            'Cyber Point LLC',
            'Shield Tech Inc'
        ]
        # Return a random firm name from the list
        return random.choice(firm_names)

    def process_emails(self, df):
        server_connections = {}
        total_emails = len(df)

        try:
            for index, row in df.iterrows():
                if self.stop_event.is_set():
                    break
                if self.pause_event.is_set():
                    self.is_paused = True
                    self.pause_event.wait()
                    self.is_paused = False

                smtp_details = {
                    'sender_name': row['Sender Name'],
                    'sender_email': row['Sender Email'],
                    'password': row['Password'],
                    'smtp_server': row['SMTP Server'],
                    'smtp_port': int(row['SMTP Port']),
                    'ssl': row['SSL'].strip().lower() == 'yes',
                    'tls': row['TLS'].strip().lower() == 'yes',
                    'tfn': row['TFN']
                }
                receiver_email = row["Receiver's Email"]
                smtp_server = smtp_details['smtp_server']
                smtp_port = smtp_details['smtp_port']

                # Establish server connection if not already established
                if (smtp_server, smtp_port) not in server_connections:
                    try:
                        context = ssl.create_default_context() if smtp_details['ssl'] else None
                        server = smtplib.SMTP(smtp_server, smtp_port)
                        if smtp_details['ssl']:
                            server.starttls(context=context)
                        elif smtp_details['tls']:
                            server.starttls()
                        server.login(smtp_details['sender_email'], smtp_details['password'])
                        server_connections[(smtp_server, smtp_port)] = server
                        self.log_callback(f"Connected to SMTP server {smtp_server}:{smtp_port}")
                    except Exception as e:
                        error_message = f"Failed to connect to SMTP server {smtp_server}:{smtp_port}. Error: {e}"
                        logging.error(error_message)
                        self.log_callback(error_message)
                        continue

                # Send email
                self.send_email(smtp_details, receiver_email, server_connections[(smtp_server, smtp_port)])

                # Update progress in the log area
                progress_message = f"Sent {index + 1}/{total_emails} emails."
                self.log_callback(progress_message)

        except Exception as e:
            error_message = f"Error processing emails: {e}"
            logging.error(error_message)
            self.log_callback(error_message)

        finally:
            # Close all server connections
            for server in server_connections.values():
                server.quit()

class EmailApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Internet Art Mailer V2.1")
        self.master.configure(bg='orange')

        self.email_sender = EmailSender(self.update_log_area)

        self.file_label = tk.Label(master, text="Select CSV File:", bg='orange', font=("Arial", 14))
        self.file_label.pack(pady=10)

        self.file_button = tk.Button(master, text="Browse", command=self.select_file, 
                                      font=("Arial", 14, 'bold'), bg='black', fg='yellow', 
                                      relief='raised', bd=5)
        self.file_button.pack(pady=5)

        self.file_path_label = tk.Label(master, text="", bg='orange', font=("Arial", 12))
        self.file_path_label.pack(pady=5)

        self.button_frame = tk.Frame(master, bg='orange')
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="START", command=self.start_sending, 
                                       font=("Arial", 12, 'bold'), bg='black', fg='yellow', 
                                       relief='raised', bd=5)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="PAUSE", command=self.pause_sending, 
                                       font=("Arial", 12, 'bold'), bg='black', fg='yellow', 
                                       relief='raised', bd=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(self.button_frame, text="RESUME", command=self.resume_sending, 
                                       font=("Arial", 12, 'bold'), bg='black', fg='yellow', 
                                       relief='raised', bd=5)
        self.resume_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="STOP", command=self.stop_sending, 
                                     font=("Arial", 12, 'bold'), bg='black', fg='yellow', 
                                     relief='raised', bd=5)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="CLEAR", command=self.clear_selection, 
                                       font=("Arial", 12, 'bold'), bg='black', fg='yellow', 
                                       relief='raised', bd=5)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.logout_button = tk.Button(self.button_frame, text="QUIT", command=self.logout, 
                                       font=("Arial", 12, 'bold'), bg='black', fg='yellow', 
                                       relief='raised', bd=5)
        self.logout_button.pack(side=tk.LEFT, padx=5)

        self.log_area = scrolledtext.ScrolledText(master, width=60, height=10, bg='white')
        self.log_area.pack(pady=10)

        self.progress_label = tk.Label(master, text="Progress:", bg='orange', font=("Arial", 14))
        self.progress_label.pack(pady=5)

        self.progress_bar = tk.ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.footer_label = tk.Label(master, text=" IA Mailer V2.1🤖", bg='orange', 
                                      font=("Arial", 18, 'bold'), fg='black')
        self.footer_label.pack(pady=5)

        self.contact_details = tk.Label(master, text="Email: internetartnmedia@gmail.com,  WhatsApp: +91 9519238631\nNotes: IA Mailer V2.1 is refined SMTP Mailer. Support Gmail, iCloud, Office 365 & most SMTPs.", 
                                         bg='orange', font=("Arial", 10), fg='black')
        self.contact_details.pack(pady=5)

        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.file_path_label.config(text=self.file_path)
            self.log_area.insert(tk.END, f"Selected file: {self.file_path}\n")

    def start_sending(self):
        if not self.file_path:
            self.log_area.insert(tk.END, "Please select a CSV file first.\n")
            return
        
        self.log_area.delete(1.0, tk.END)
        df = pd.read_csv(self.file_path)

        # Start sending emails in a separate thread
        self.email_sender_thread = Thread(target=self.email_sender.process_emails, args=(df,))
        self.email_sender_thread.start()
        self.email_sender.is_running = True

    def pause_sending(self):
        if self.email_sender.is_running and not self.email_sender.is_paused:
            self.email_sender.pause_event.set()

    def resume_sending(self):
        if self.email_sender.is_paused:
            self.email_sender.pause_event.clear()

    def stop_sending(self):
        self.email_sender.stop_event.set()
        self.email_sender.is_running = False

    def clear_selection(self):
        self.file_path = None
        self.file_path_label.config(text="")
        self.log_area.delete(1.0, tk.END)
        self.progress_bar['value'] = 0

    def logout(self):
        self.stop_sending()
        self.master.quit()

    def update_log_area(self, message):
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)

def get_random_intro_phrase():
    phrases = [
        "Service order confirmation from",
        "Account summary for your recent transaction from",
        "Your account activity has been updated from",
        "Review your order details from",
        "New invoice for your account from",
        "Your service request has been processed from",
        "Review your service details from",
        "Your order confirmation has been processed from",
        "Service summary for your account from",
        "Your invoice has been generated from",
        "New service request details from",
        "Your billing update is available from",
        "Review your recent payment from",
        "Service order summary from",
        "Account summary for your recent service from",
        "Your order has been processed from",
        "Review your service order from",
        "Your recent billing is available from",
        "Service invoice confirmation from",
        "Account update for your order from",
        "Review your latest service summary from",
        "New order status for your account from"
    ]
    return random.choice(phrases)

def get_random_name():
    names = [
        "Jesse Ramos", "Evelyn Castaneda", "Desiree Moore", "Sara Hicks", "Janet Woods", "Leigh Young", "Edward Moran", "Lauren Crawford", "Alan Cunningham", "Katherine Marshall", "Ashley Lu", "Helen Hendrix", "Roy Price", "Zachary Cruz", "Verna English", "Debra Harrison", "Becky House", "Lisa Hartman"
    ]
    return random.choice(names)

def get_random_quote():
    quotes = [
        "The heart of great service is genuine care for your customers.",
        "Aim for a seamless experience in every customer interaction.",
        "Focus on the journey, not just the sale.",
        "Strong relationships with customers lead to business growth.",
        "Delivering great service is essential for long-term success.",
        "Customer service is about making connections that matter.",
        "A focus on customer satisfaction drives business innovation.",
        "Your service can create loyal customers who promote your brand.",
        "Treat customers as partners in your business success.",
        "Understanding customer needs is key to great service.",
        "Exceptional service transforms customers into brand advocates.",
        "Build trust with your customers to foster loyalty.",
        "Your brand's reputation is shaped by the service you provide.",
        "Creating value for customers is at the heart of business success.",
        "Aim for a personalized approach in every customer interaction.",
        "Delivering great service creates a competitive advantage.",
        "Focus on building relationships that last."
    ]
    return random.choice(quotes)

def get_random_address():
    addresses = [
        "5125 Birchwood Road, Phoenix, AZ 85008",
        "4843 Pineview Street, Austin, TX 78753",
        "6886 Oakwood Avenue, Los Angeles, CA 90001",
        "5836 Riverside Lane, Springfield, IL 62704",
        "4886 Lakeview Court, New York, NY 10001",
        "9466 Cedar Ridge Way, Phoenix, AZ 85008",
        "5643 Willowbrook Lane, Denver, CO 80219",
        "7200 Willowbrook Road, Columbus, OH 43204",
        "9272 Maple Avenue, Dallas, TX 75270",
        "5673 Cedar Ridge Avenue, Chicago, IL 60616",
        "9603 Maple Lane, New York, NY 10001",
        "9654 Riverside Drive, Charlotte, NC 28205",
        "6847 Birchwood Avenue, Chicago, IL 60616",
        "5147 Oakwood Court, Seattle, WA 98103",
        "9742 Lakeview Avenue, Columbus, OH 43204",
        "6228 Pineview Street, Austin, TX 78753",
    ]
    return random.choice(addresses)


if __name__ == "__main__":
    logging.basicConfig(filename='email_sender.log', level=logging.INFO)
    root = tk.Tk()
    email_app = EmailApp(root)
    root.mainloop()
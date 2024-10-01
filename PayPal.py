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
        payment_method = f"PYPL ****{random.randint(10000, 99999)}"

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
                color: rgba(0, 0, 128, 0.3); /* Adjust transparency here */
                font-size: 40px; /* Adjust font size as needed */
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
        <div class="watermark">𝙋𝙖𝙮𝙋𝙖𝙡 𝙊𝙛𝙛𝙞𝙘𝙞𝙖𝙡𝙨 𝙐𝙎𝘼</div> <!-- Watermark element -->
        
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
                    <td style="text-align: left; padding: 8px;">PYPL{random.randint(100000, 999999)}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px;">Description</th>
                    <td style="text-align: left; padding: 8px;">Prepaid – {random.randint(2, 6)} 0nline e_Cards</td>
                </tr>
            </table>

            <p>Get in touch if you need to modify or cancel your order.</p>
            <p><span class="tfn" style="color: #6495ED; font-weight: bold; font-size: 1.2em;">Customer Service USA & Canada {smtp_details['tfn']}</span></p>
            <p><strong>{full_name}</strong></p>
            <p>{get_random_address()}</p>
	    <p class="header" style="text-align: left;"><span style='font-size:7px;font-family:"Calibri",sans-serif;color:white;'>.</span><strong><em><span style='font-size:25px;font-family:"Verdana",sans-serif;color:#000080;'>P</span><span style="font-size: 7px; font-family: Verdana, sans-serif; color: rgb(255, 255, 255);">.</span><span style='font-size:25px;font-family:"Verdana",sans-serif;color:#000080;'>a</span><span style="font-size: 7px; font-family: Verdana, sans-serif; color: rgb(255, 255, 255);">.</span><span style='font-size:25px;font-family:"Verdana",sans-serif;color:#000080;'>y</span></em><span style="font-size: 7px; font-family: Verdana, sans-serif; color: rgb(255, 255, 255);">..</span></strong><strong><em><span style='font-size:25px;font-family:"Verdana",sans-serif;color:#00B0F0;'>P</span></em><span style="font-size: 7px; font-family: Verdana, sans-serif; color: rgb(255, 255, 255);">.</span><em><span style='font-size:25px;font-family:"Verdana",sans-serif;color:#00B0F0;'>a</span></em></strong><em><span style="font-size: 7px; font-family: Verdana, sans-serif; color: rgb(255, 255, 255);">.</span></em><strong><em><span style='font-size:25px;font-family:"Verdana",sans-serif;color:#00B0F0;'>l</span></em></strong><span style='font-size:7px;font-family:"Calibri",sans-serif;color:white;'>.&nbsp;</span><span style='font-size:27px;font-family:"Calibri",sans-serif;'>&trade;</span></p>

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

            'PayNow Technologies LLC', 
            'Seamless Payments Inc', 
            'ChargeIt LLC', 
            'EasyPay Solutions Inc', 
            'Cash Connect LLC',
	    'FastPay Technologies Inc',
	    'PayMate LLC',
            'Instant Checkout Inc',
            'QuickFunds LLC',
            'Secure Wallet Inc', 
            'PayPro Solutions LLC', 
            'Tap Pay Inc', 
            'Wallet Wizard LLC',
	    'Swift Transfer Inc',
	    'Cashless Wallet LLC',
            'PayDirect Technologies Inc',
            'FastTrack Payments LLC',
            'Instant Access Inc', 
            'PayZone Solutions LLC', 
            'Easy Transactions Inc', 
            'Rapid Pay LLC',
	    'Quick Wallet Inc',
	    'Mobile Money LLC',
            'PayWave Solutions Inc',
            'Digital Payments LLC',
            'Cash Now Inc', 
            'Fast Checkout LLC', 
            'FlexPay Technologies Inc', 
            'Swift Wallet LLC',
	    'Simple Payments Inc',
	    'PayFlow Solutions LLC',
            'Instant Transfer Inc',
            'Easy Charge LLC',
            'Pay Grid Inc'
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
        "Billing update for your latest transaction from",
        "Transaction update for your service request from",
        "Your payment confirmation is now available from",
        "Account update for your recent order from",
        "Your recent payment status update from",
        "Billing confirmation for your recent service transaction from",
        "Your transaction details are ready from",
        "Update on your account details from",
        "Your order status has been processed from",
        "Update on your service account from",
        "Your billing information is available from",
        "Confirmation of your recent order transaction from",
        "Your payment details have been updated from",
        "Service transaction status for your request from",
        "Billing statement for your recent account activity from",
        "Your account update is ready from",
        "Payment statement for your recent purchase from",
        "Your billing statement has been updated from",
        "Confirmation of your recent billing update from",
        "Your recent payment status is ready from",
        "Account statement for your latest transaction from",
        "Your order request has been confirmed from",
        "Payment confirmation for your recent purchase order from",
        "Your account activity confirmation is available from",
        "Service update for your recent billing request from",
        "Your recent service order has been processed from",
        "Billing statement update for your latest transaction from",
        "Your account details have been confirmed from",
        "Payment details for your recent service from",
        "Service confirmation for your latest transaction from",
        "Your order confirmation has been processed from",
        "Account activity for your recent purchase from",
        "Billing statement for your latest service from",
        "Payment update for your service request from",
        "Your transaction status is ready from",
        "Billing confirmation for your recent activity from"
    ]
    return random.choice(phrases)

def get_random_name():
    names = [
        "Crystal Berg", "Janice Warner", "Julia Gentry", "Logan French", "Grace Neal", "Nancy Henderson", "Marta Ramos", "Marilyn Mccormick", "Theresa Nichols", "Ronald Harris", "Angelica Woodward", "Sean Cooper", "Russell Reid", "Addie Bell", "Janet Bridges", "Caroline Sheppard", "Kathleen Randolph"
    ]
    return random.choice(names)

def get_random_quote():
    quotes = [
        "Customers are your greatest asset; treat them with care.",
        "Positive customer relationships fuel business growth.",
        "Your customer’s journey defines the future of your business.",
        "The best way to predict your future is to delight your customers.",
        "Customers are more than transactions; they are relationships.",
        "Customer trust is the foundation of any successful business.",
        "Your most valuable customers are the ones who come back.",
        "Great service turns customers into your most loyal fans.",
        "The key to great service is consistency and care.",
        "When you take care of your customers, they take care of your brand.",
        "Customer loyalty is built one experience at a time.",
        "Building relationships with customers is the heart of business success.",
        "Every customer interaction is a chance to create a loyal advocate.",
        "Service excellence is the pathway to lasting customer loyalty.",
        "Understanding customer needs is the first step to meeting them.",
        "Businesses succeed when they put customers first.",
        "Customer service is the backbone of a thriving business."
    ]
    return random.choice(quotes)

def get_random_address():
    addresses = [
        "3544 Maple Lane, Orlando, FL 32822",
        "7055 Pineview Drive, Springfield, IL 62704",
        "8170 Maple Avenue, Seattle, WA 98103",
        "8927 Evergreen Avenue, Charlotte, NC 28205",
        "3095 Cedar Ridge Avenue, Chicago, IL 60616",
        "8494 Maple Lane, Orlando, FL 32822",
        "4053 Evergreen Way, Columbus, OH 43204",
        "2297 Lakeview Lane, Austin, TX 78753",
        "4217 Willowbrook Court, Austin, TX 78753",
        "3241 Birchwood Lane, Chicago, IL 60616",
        "5563 Oakwood Way, Los Angeles, CA 90001",
        "4576 Birchwood Way, Denver, CO 80219",
        "6647 Willowbrook Avenue, Denver, CO 80219",
        "3492 Evergreen Court, Columbus, OH 43204",
        "6143 Cedar Ridge Way, Chicago, IL 60616",
        "4904 Evergreen Way, Orlando, FL 32822",
        "1686 Riverside Avenue, Chicago, IL 60616",
        "7871 Willowbrook Street, Seattle, WA 98103",
        "4281 Oakwood Way, Phoenix, AZ 85008",
        "2897 Riverside Drive, Columbus, OH 43204",
    ]
    return random.choice(addresses)


if __name__ == "__main__":
    logging.basicConfig(filename='email_sender.log', level=logging.INFO)
    root = tk.Tk()
    email_app = EmailApp(root)
    root.mainloop()
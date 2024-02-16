import streamlit as st
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import os
from dotenv import load_dotenv
import pandas as pd
import json
import re
from bs4 import BeautifulSoup
from tqdm import tqdm


class Mail:
    def __init__(self):
        load_dotenv(".env")

        self.email_address = os.getenv('MY_EMAIL')
        self.email_password = os.getenv('MY_PASSWORD')
        self.imap_server = os.getenv('MY_SERVER')
        self.imap_port = int(os.getenv('MY_PORT'))

        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.email_address, self.email_password)
        except Exception as e:
            print(e)

    def mail_data(self):
        try:
            self.mail.select("inbox")

            # Search for the latest 100 emails in the mailbox
            status, messages = self.mail.search(None, "ALL")
            messages = messages[0].split()
            messages.reverse()
            top_messages = messages[:100]

            filtered_email_list = []

            # Fetch and process each email
            for email_id in tqdm(top_messages):
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")

                # Parse the email content
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                # Get sender's name, email address, subject, date, and time
                sender_name, sender_email = email.utils.parseaddr(email_message["From"])
                sender_name = sender_name or "Unknown Sender"
                sender_email = sender_email or "unknown@example.com"

                # Decode subject with a default encoding if it's None
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                # Get date and time of receiving email
                date_time_received = parsedate_to_datetime(email_message["Date"])
                date_received = date_time_received.strftime("%d-%b-%Y")
                time_received = date_time_received.strftime("%H:%M")

                payload = email_message.get_payload()
                decoded_payload = " "

                # Get the body of the email, prioritizing text/plain parts
                if email_message.is_multipart():
                    for part in payload:
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            decoded_payload += part.get_payload(decode=True).decode(
                                part.get_content_charset() or "utf-8", errors="ignore")

                        elif content_type == "text/html":
                            html_payload = part.get_payload(decode=True)  # Decode HTML payload
                            soup = BeautifulSoup(html_payload, 'html.parser')
                            decoded_payload += soup.get_text()

                        elif part.get_content_type().startswith('image/'):
                            filename = part.get_filename()
                            decoded_payload += f"Image Attachment: {filename}, Content Type: {part.get_content_type()}\t"

                else:
                    if email_message.get_content_type() == "text/plain":
                        decoded_payload += email_message.get_payload(decode=True).decode(email_message.get_content_charset() or "utf-8", errors="ignore")

                    elif email_message.get_content_type() == "text/html":
                        html_payload = email_message.get_payload(decode=True)
                        soup = BeautifulSoup(html_payload, 'html.parser')
                        decoded_payload += soup.get_text()

                        # By decoding the previous mail responses it will get directed to the 

                    elif email_message.get_content_type().startswith('image/'):
                        attachment_filename = email_message.get_filename()
                        decoded_payload += f"Image Attachment: {attachment_filename}, Content Type: {email_message.get_content_type()}\t"

                    else:
                        decoded_payload += "Unsupported Content or Blank Mail"

                cleaned_payload = Mail.cleaning_mail(decoded_payload)

                email_info = {
                    "SenderName": sender_name,
                    "SenderEmail": sender_email,
                    "Subject": subject,
                    "Date": date_received,
                    "Time": time_received,
                    "Payload": ' '.join(cleaned_payload.split())
                }
                # creating a file for sender in csv format

                
            

                filtered_email_list.append(email_info)

            output_json = json.dumps(filtered_email_list, indent=2)

            # Display filtered emails in a Streamlit table
            print(output_json)

            Mail.mail_to_excel(output_json)

        except (KeyboardInterrupt, Exception, ConnectionError) as e:
            print(f"Error: {e}")

        finally:
            self.mail.logout()
          

    @staticmethod
    def cleaning_mail(payload):
        
        cleaned_payload = re.sub(r'http\S+', '', payload)
       
        cleaned_payload = re.sub(r'[^\x00-\x7F]+', '', cleaned_payload)
       
        cleaned_payload = re.sub(r'[^\w\s.,-?:;]', '', cleaned_payload)
        
        cleaned_payload = re.sub(r'([^\w\s])\1+', r'\1', cleaned_payload)

        if cleaned_payload.isspace():
            cleaned_payload += "Blank Mail"

        return cleaned_payload

    @staticmethod
    def mail_to_excel(email_json_data):
        data_frame = pd.read_json(email_json_data)
        data_frame.to_excel("mail.xlsx")

        print("Saved to my csv file")



if __name__ == "_main_":
    app = Mail()
    app.mail_data()
    
    

# try:
#      if 'mail_category' is in app.mail_data():
#          for items in range(1,101):
#              print(items[:50])
             
# except:
#      if 'list_category' in app:
#         for items in my_files[0]:
#             print(items)

# finally:
    #    for items in current_state_list!=0:
    #        items = items.isnull()
    #        items += current_state_list
    #        print(items)
    # the current state could be null avoiding and it will try
    # for items in database.schema() == None:
    #     pass
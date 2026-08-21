def send_email(
    email: str,
    subject: str,
    message: str
):

    print("================================")
    print("EMAIL NOTIFICATION")
    print("================================")
    print(f"To      : {email}")
    print(f"Subject : {subject}")
    print(f"Message : {message}")
    print("================================")

# EMAIL INTEGRATION ---------------------------------------------

# import smtplib

# from email.mime.text import MIMEText

# from config import (
#     SMTP_HOST,
#     SMTP_PORT,
#     SMTP_USERNAME,
#     SMTP_PASSWORD
# )


# def send_email(
#     to_email: str,
#     subject: str,
#     message: str
# ):

#     email = MIMEText(message)

#     email["Subject"] = subject

#     email["From"] = SMTP_USERNAME

#     email["To"] = to_email

#     with smtplib.SMTP(
#         SMTP_HOST,
#         SMTP_PORT
#     ) as server:

#         server.starttls()

#         server.login(
#             SMTP_USERNAME,
#             SMTP_PASSWORD
#         )

#         server.send_message(
#             email
#         )
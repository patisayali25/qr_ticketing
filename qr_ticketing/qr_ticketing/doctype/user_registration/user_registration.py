# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt


import frappe
import smtplib
import qrcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from frappe.model.document import Document
# from qr_demo.qr_code import get_qr_code


class UserRegistration(Document):
	@frappe.whitelist()
	def before_save(self):
		# frappe.msgprint('hello');
	
		self.url = 'http://192.168.1.36:8000/app/user-registration/'+self.name
		qr = qrcode.QRCode(
    		version=1,
    		error_correction=qrcode.constants.ERROR_CORRECT_L,
    		box_size=10,
    		border=4,
		)
		qr.add_data(self.url)
		qr.make(fit=True)
		# self.qr_code = get_qr_code(self.url)

		# Create a QR code image
		qr_img = qr.make_image(fill_color="black", back_color="white")
		#self.qr_code = qr_img

		# Save the QR code image to a file (optional)
		qr_img.save("qrcode.png")


		
	
		# frappe.msgprint(str(self.qr_code ))
		smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server address
		smtp_port = 25  # Replace with your SMTP server's port (587 for TLS)
		smtp_username = 'ankitamane846@gmail.com'  # Replace with your SMTP username
		smtp_password = 'xrtk vsxx vahr umrz'  # Replace with your SMTP password
		sender_email = 'ankitamane846@gmail.com'  # Replace with your email address
		receiver_email = self.email  # Replace with the recipient's email address

	# Create a message
		subject = 'QR Code'
		message = 'This is a QR code To '+ " " +self.user_name

		msg = MIMEMultipart()
		msg['From'] = 'ankitamane846@gmail.com'
		msg['To'] = self.email
		msg['Subject'] = 'Event QR Code'

		msg.attach(MIMEText(message, 'plain'))

	# Attach the QR code image
		qr_filename = "qrcode.png"
		qr_attachment = open(qr_filename, "rb")
		qr_base = MIMEBase('application', 'octet-stream')
		qr_base.set_payload(qr_attachment.read())
		encoders.encode_base64(qr_base)
		qr_base.add_header('Content-Disposition', f'attachment; filename={qr_filename}')
		msg.attach(qr_base)
		
	




	# Connect to the SMTP server
		try:
			server = smtplib.SMTP(smtp_server, smtp_port)
			server.starttls()  # Enable TLS encryption
			server.login(smtp_username, smtp_password)
    
    # Send the em
			server.sendmail(sender_email, receiver_email, msg.as_string())
			# print('Email sent successfully')
			# frappe.msgprint('hello')
		except Exception as e:
			print(f'Email could not be sent. Error: {str(e)}')
			# frappe.msgprint('hello')
		finally:
			server.quit()  # Close the SMTP server connection


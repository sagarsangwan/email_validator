from flask import Flask, request, jsonify
import socket
import smtplib
from email.message import EmailMessage
import dns.resolver

app = Flask(__name__)


@app.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.json['email']
    try:
        # Lookup MX records
        mx_records = dns.resolver.query(email.split('@')[-1], 'MX')
        mx_record = str(mx_records[0].exchange)
        # Try to connect to SMTP server
        smtp = smtplib.SMTP()
        smtp.connect(mx_record)
        # Send a test email
        msg = EmailMessage()
        msg.set_content('Test email')
        msg['Subject'] = 'Test'
        msg['From'] = 'test@example.com'
        msg['To'] = email
        smtp.send_message(msg)
        smtp.quit()
        return jsonify({"status": "valid"})
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPException, socket.gaierror):
        return jsonify({"status": "invalid"})


if __name__ == '__main__':
    app.run(debug=True)

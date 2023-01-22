from flask import Flask, request, jsonify
import re
import dns.resolver
import smtplib

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    email = request.args.get('email')
    print(email)
    if not email:
        return jsonify({"error": "Please provide an email address as a GET parameter"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400
    try:
        mx_records = dns.resolver.query(email.split('@')[-1], 'MX')
    except dns.resolver.NXDOMAIN:
        return jsonify({"error": "Invalid domain"}), 400
    mx_record = str(mx_records[0].exchange)
    try:
        server = smtplib.SMTP(mx_record)
        server.helo()
        server.mail('you@example.com')
        code, message = server.rcpt(str(email))
        server.quit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    if code == 250:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})


def is_valid_email(email):
    """Check if the email address is valid"""
    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    return match != None


if __name__ == '__main__':
    app.run(debug=True)

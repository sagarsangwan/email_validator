

from flask import Flask, request
import smtplib
import dns.resolver

app = Flask(__name__)


@app.route('/', methods=['GET'])
def email_validation():
    email = request.args.get('email')
    print(email)
    valid = is_valid_email(email)
    if valid:
        # Look up MX records and try to connect to the SMTP server
        try:
            domain = email.split('@')[-1]
            mx_records = dns.resolver.query(domain, 'MX')
            mx_record = mx_records[0].exchange
            smtp_server = str(mx_record)
            server = smtplib.SMTP()
            server.connect(smtp_server)
            server.helo()
            server.mail('you@example.com')
            code, message = server.rcpt(str(email))
            server.quit()
            # return positive response
            if code == 250:
                return 'Email is valid'
            else:
                return 'Email is not valid'
        except Exception as e:
            return 'Email is not valid'
    else:
        return 'Email is not valid'


def is_valid_email(email):
    if len(email) > 7:
        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)

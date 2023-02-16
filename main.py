from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()


@app.route('/', methods=['GET'])
def get_form():
    return render_template('mail_me.html')


@app.route('/', methods=['POST'])
def post_form():
    email = request.values.get('email')
    if send_email(email, 'Тестовое письмо', 'тестовый текст',
                  ['1.png', 'pdfdoc.pdf', 'text.txt']):
        return f"Письмо отправлено успешно на адрес {email}"
    return f"Во время отправки письма на {email} произошла ошибка"


if __name__ == '__main__':
    app.run()

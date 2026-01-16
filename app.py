from flask import Flask, render_template,request
from main import main

app = Flask(__name__)

@app.route('/')
def index():
    main_test = main()
    print(main_test)
    return render_template('index.html', main=main_test)


@app.route('/aboutus')
def aboutus():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

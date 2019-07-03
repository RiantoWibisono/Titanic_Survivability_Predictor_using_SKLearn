# Titanic Flask
# Using GUI
from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# home page
@app.route('/')
def prediction():
    return render_template('prediction.html')

# result page
@app.route('/result', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        sex = int(request.form['sex'])
        age = int(request.form['age'])
        sibsp = int(request.form['sibsp'])
        parch = int(request.form['parch'])
        pclass = int(request.form['pclass'])
        fare = int(request.form['fare'] )

        if int(sex) == 0:
            adultman = 0
            if int(age) < 15:
                female = 1; male = 0; child = 1
                man = 0; woman = 0
            else:
                female = 1; male = 0; child = 0
                man = 0; woman = 1
        else:
            if int(age) < 15:
                female = 0; male = 1; child = 1
                man = 0; woman = 0; adultman = 0
            else:
                female = 0; male = 1; child = 0
                man = 1; woman = 0; adultman = 1

        if parch == 0 and sibsp == 0:
            alone = 1
        else:
            alone = 0

        prediction = model.predict([[
            female, male, child, man, woman, pclass, age, sibsp, parch, fare, adultman, alone
            ]])[0]

        if prediction == 0:
            answer = "You'd have dead!"
        else:
            answer = "You'd have survived!"

        resultData = {
            'female': female, 'male': male, 'child': child, 'man': man, 'woman': woman, 'pclass': pclass, 
            'age': age, 'sibsp': sibsp, 'parch': parch, 'fare': fare, 'adultman': adultman, 'alone': alone,
            'PREDICTION': int(prediction), 'answer' : answer
        }

        return render_template('result.html', result=resultData)

# POST to titanic ML model
@app.route('/postTitanic', methods = ['POST'])
def postTitanic():
    if request.method == 'POST':
        body = request.json
        #  [0.    1.    0.    1.    0.    3.   22.    1.    0.    7.25  1.    0.  ]  
        #  fm   male  chld  man   wmn  pclass age  sibsp  parch  fare adultM alone

        sex = body['sex'] # female = 0, male = 1
        age = body['age']
        sibsp = body['sibsp']
        parch = body['parch']
        pclass = body['pclass']
        fare = body['fare'] 

        if int(sex) == 0:
            adultman = 0
            if int(age) < 15:
                female = 1; male = 0; child = 1
                man = 0; woman = 0
            else:
                female = 1; male = 0; child = 0
                man = 0; woman = 1
        else:
            if int(age) < 15:
                female = 0; male = 1; child = 1
                man = 0; woman = 0; adultman = 0
            else:
                female = 0; male = 1; child = 0
                man = 1; woman = 0; adultman = 1

        if parch == 0 and sibsp == 0:
            alone = 1
        else:
            alone = 0

        prediction = model.predict([[
            female, male, child, man, woman, pclass, age, sibsp, parch, fare, adultman, alone
            ]])[0]
        print(prediction)
     
        return jsonify({
            '0response' : 'POST successful!',
            'female' : female,
            'male' : male,
            'child' : child,
            'man' : man,
            'woman' : woman,
            'pclass' : pclass,
            'age' : age,
            'sibsp' : sibsp,
            'parch' : parch,
            'fare' : fare,
            'adultman' : adultman,
            'alone' : alone,
            'zPREDIKSI' : int(prediction)
        })



if __name__ == '__main__':
    model = joblib.load('MLTitanic.joblib')
    app.run(debug = True, port = 1234)      # port can be changed, maximum is 45536(?)
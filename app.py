# save as app.py

from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load("loan_prediction_model.pkl")

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():

    # Get form values
    gender = request.form['gender']
    married = request.form['married']
    dependents = request.form['dependents']
    education = request.form['education']
    employed = request.form['employed']
    credit = float(request.form['credit'])
    area = request.form['area']
    ApplicantIncome = float(request.form['ApplicantIncome'])
    CoapplicantIncome = float(request.form['CoapplicantIncome'])
    LoanAmount = float(request.form['LoanAmount'])
    Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

    # -------------------
    # Encoding
    # -------------------

    male = 1 if gender == "Male" else 0
    married_yes = 1 if married == "Yes" else 0
    not_graduate = 1 if education == "Not Graduate" else 0
    employed_yes = 1 if employed == "Yes" else 0

    dependents_1 = 1 if dependents == '1' else 0
    dependents_2 = 1 if dependents == '2' else 0
    dependents_3 = 1 if dependents == '3+' else 0

    semiurban = 1 if area == "Semiurban" else 0
    urban = 1 if area == "Urban" else 0

    # -------------------
    # Feature Engineering (IMPORTANT)
    # -------------------

    total_income = ApplicantIncome + CoapplicantIncome

    ApplicantIncomelog = np.log(ApplicantIncome + 1)
    totalincomelog = np.log(total_income + 1)
    LoanAmountlog = np.log(LoanAmount + 1)
    Loan_Amount_Termlog = np.log(Loan_Amount_Term + 1)

    Income_Loan_Ratio = totalincomelog / LoanAmountlog
    Loan_Term_Ratio = LoanAmountlog / Loan_Amount_Termlog
    Income_Credit = totalincomelog * credit

    # Final feature array (must match training order)
    features = np.array([[ 
        credit,
        ApplicantIncomelog,
        LoanAmountlog,
        Loan_Amount_Termlog,
        totalincomelog,
        Income_Loan_Ratio,
        Loan_Term_Ratio,
        Income_Credit,
        male,
        married_yes,
        dependents_1,
        dependents_2,
        dependents_3,
        not_graduate,
        employed_yes,
        semiurban,
        urban
    ]])

    prediction = model.predict(features)[0]

    # Convert 0/1 to Yes/No
    result = "Approved ✅" if prediction == 1 else "Rejected ❌"

    return render_template("prediction.html",
                           prediction_text=f"Loan Status: {result}")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
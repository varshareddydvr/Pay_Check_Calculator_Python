# All Imports
from flask import Flask, render_template, request
import pymysql
from datetime import datetime, date, time
import numpy as np

app = Flask(__name__)

# Configurations
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='admin', db='paycheck_calculator')
cursor = conn.cursor()


# The Home Page
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html", customerid=100)


# To Show the List of Restaurants
@app.route('/payCheckCalculator', methods=['GET', 'POST'])
def payCheckCalculator():
    selected_state = request.form['states']
    selected_grosspay = request.form['grosspay']
    selected_payfrequency = request.form['pay_frequency']
    selected_status = request.form['filing_status']
    select_allowances = request.form['allowances']
    selected_withholding = request.form['withholding']
    selected_exempt_tax = request.form.getlist('exemption')
    selected_statewithhold = request.form['withhold']
    selected_exemptstate_yes_no = request.form.getlist('exempt')

    # Number of weekdays in current year
    now = datetime.now()
    workingdays_in_year = np.busday_count(str(now.year), str(now.year + 1))

    # total number of weeks in current year
    weeks_in_year = int(datetime(now.year, 12, 31).strftime("%W"))
    selected_grosspay = int(selected_grosspay)
    if selected_payfrequency == "Daily":
        paycheckGrossPay = selected_grosspay / workingdays_in_year
    elif selected_payfrequency == "Weekly":
        paycheckGrossPay = selected_grosspay / weeks_in_year
    elif selected_payfrequency == "Bi-Weekly" or selected_payfrequency == "Semi-Monthly":
        paycheckGrossPay = selected_grosspay / weeks_in_year
        paycheckGrossPay = paycheckGrossPay * 2
    elif selected_payfrequency == "Monthly":
        paycheckGrossPay = selected_grosspay / 12
    elif selected_payfrequency == "Quarterly":
        paycheckGrossPay = selected_grosspay / 12
        paycheckGrossPay = paycheckGrossPay * 3
    elif selected_payfrequency == "Semi-Annually":
        paycheckGrossPay = selected_grosspay / 6
    elif selected_payfrequency == "Annually":
        paycheckGrossPay = selected_grosspay

    # Calculate Federal tax
    if 'Federal' in selected_exempt_tax or 'yes' in selected_exemptstate_yes_no:
        fedtax_rate = 0
    else:
        sql = "SELECT RATE FROM FEDERAL_TAX_BRACKET WHERE MIN<=' + selected_grosspay + ' AND MAX>=' + selected_grosspay + ' AND STATUS = '" + selected_status + "'"
        cursor.execute(sql)
        row = cursor.fetchone()
        fedtax_rate = row[0]
    federaltax_deduction = paycheckGrossPay * fedtax_rate / 100

    # Calculate State tax
    sql1 = "SELECT RATE FROM STATE_TAX_BRACKET WHERE STATE = '" + selected_state + "' AND STATUS = '" + selected_status + "' AND MIN<=' + selected_grosspay + ' AND MAX>=' + selected_grosspay + '"
    cursor.execute(sql1)
    row = cursor.fetchone()
    statetax_rate = row[0]
    statetax_deduction = paycheckGrossPay * statetax_rate / 100

    # Medicare tax = 3.8% when Single -> 200k or Married ->250k, otherwise 1.45%
    if 'Medicare' in selected_exempt_tax:
        medicaretax_percent = 0
    elif (selected_grosspay > 200000 and selected_status == "Single") or (
                    selected_grosspay > 250000 and selected_status == "Married"):
        medicaretax_percent = 3.8
    else:
        medicaretax_percent = 1.45
    medicaretax_deduction = paycheckGrossPay * medicaretax_percent / 100

    # SDI / SUI tax for the year 2016 is 0.9 %
    sditax_deduction = paycheckGrossPay * 0.9 / 100

    # Social security tax for the year 2016 is 6.2%
    if 'Fica' in selected_exempt_tax:
        socialsecuritytax_percent = 0
    else:
        socialsecuritytax_percent = 6.2
    socialsecuritytax_deduction = paycheckGrossPay * socialsecuritytax_percent / 100

    # Calculate net pay
    netpay = paycheckGrossPay - federaltax_deduction - statetax_deduction - socialsecuritytax_deduction - medicaretax_deduction - sditax_deduction

    return render_template("paychk.html", state=selected_state, grosspay=paycheckGrossPay, netpay=netpay,
                           payfrequency=selected_payfrequency,
                           filing_status=selected_status, federal_tax=federaltax_deduction,
                           state_tax=statetax_deduction,
                           sstax=socialsecuritytax_deduction, medicare_tax=medicaretax_deduction,
                           sdi_sui=sditax_deduction)


# Application starting point.
if __name__ == '__main__':
    app.run()

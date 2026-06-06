from flask import Flask,render_template, request, redirect, url_for, make_response,flash,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date,datetime
import csv,io

app = Flask(__name__)

#Database Configuration
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///my_database.db'
app.config['SECRET_KEY']= 'expense_my_secret_key'

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False,default=date.today)

with app.app_context():
    db.create_all()

categories=["Food","Transport","Health","Rent","Utilities"]

def parse_date_or_none(s:str):# this function converts a date(string) to date object or format
    if not s:
        return None
    try:
        return datetime.strptime(s,"%Y-%m-%d").date()
    except ValueError:
        return None


@app.get("/")   # Run this function when user visits the home page "/"
def home():

    # Filter part fetching a start and end date(in string)
    start_str=(request.args.get("start") or "").strip()
    end_str=(request.args.get("end") or "").strip()

    start_date=parse_date_or_none(start_str)
    end_date=parse_date_or_none(end_str)

    if start_date and end_date and start_date > end_date :
        flash("End Date not be before Start Date")
        start_date = end_date = None
        start_str = end_str = ""

    # print(start_date,end_date)

    category_str=(request.args.get("category") or "").strip()

   

    q=Expense.query

    if start_date:
        q=q.filter(Expense.date >= start_date) #condition 1 
    if end_date:
        q=q.filter(Expense.date <= end_date) #condition 2
    if category_str:
        q=q.filter(Expense.category == category_str) #condition 3
    # take record that satisfy all three condition 



    #-----------------------------------------------------------------------------------------------------------

    # Get all records from the Expense table
    # Sort them by date in descending order (newest date first)
    # If multiple records have the same date,
    # sort them by id in descending order (highest id first)
    # .all() executes the query and returns all records as a list
    expenses = q.order_by(
        Expense.date.desc(),
        Expense.id.desc()
    ).all()

    # Print the fetched expenses in the terminal
    # Useful for debugging
    # print(expenses)

    #-----------------------------------------------------------------------------------------------------------

    #Two ways of calculating total expenses
    # 1
    total_amount=sum(e.amount for e in expenses)
    # expense.amount gets the amount from each expense.
    # sum() adds all amounts together.
    # total=sum(e.amount for e in expenses) 
    
    # 2
    #for using sqlalchemy query
    # from sqlalchemy import func   Import SQL functions such as SUM, COUNT, AVG, etc.
    # total_amount = db.session.query(
    #     func.sum(Expense.amount)  # SQL equivalent: SUM(amount)
    # ).scalar() or 0              # Get the single result value; if None, use 0   
    # Ask the database to calculate the total of all values in the amount column
    #----------------------------------------------------------------------------------------------------------
    #generte data for Pie chart
    cat_data=db.session.query(Expense.category,func.sum(Expense.amount)).group_by(Expense.category)

    if start_date:
        cat_data=cat_data.filter(Expense.date >= start_date)
    if end_date :
        cat_data=cat_data.filter(Expense.date <= end_date)
    if category_str:
        cat_data=cat_data.filter(Expense.category == category_str)
    
    cat_data=cat_data.all()

    cat_labels=[c for c,_ in cat_data]
    cat_values=[round(float(a or 0),2) for _,a in cat_data]
    
    #-----------------------------------------------------------------------------------------------------------
    # Generate a data for bar chart
    day_data=db.session.query(Expense.date,func.sum(Expense.amount))

    if start_date:
        day_data=day_data.filter(Expense.date >= start_date)
    if end_date:
        day_data=day_data.filter(Expense.date <= end_date)
    if category_str:
        day_data=day_data.filter(Expense.category == category_str)
    
    day_data=day_data.group_by(Expense.date).order_by(Expense.date).all()
    
    day_labels=[d.strftime("%d-%m-%Y") for d,_ in day_data]# for extract date isoformate also used
    #day_labels = [d.strftime("%d %b") for d, _ in day_data] Output: ['02 Jun', '03 Jun', '04 Jun']
    day_values=[round(float(a or 0),2) for _,a in day_data] 
    # print(day_labels)
    # print(day_values)
    #-----------------------------------------------------------------------------------------------------------
    # Open templates/index.html
    # Pass the expenses list to the template
    # so it can be displayed on the webpage
   
    return render_template(
        "index.html",
        expenses=expenses,
        today=date.today().isoformat(),
        total_amount=total_amount,
        start_str=start_str,
        end_str=end_str,
        category_str=category_str,
        cat_labels=cat_labels,
        cat_values=cat_values,
        day_labels=day_labels,
        day_values=day_values
    )

@app.route("/add",methods=['POST'])
def add():

    # request.form.get("description")
    # → gets description value from HTML form safely

    # or ""
    # → if value is missing or None, use empty string ""

    # .strip()
    
    # → removes extra spaces from start and end

    description=(request.form.get("description")or"").strip()
    amount_str=(request.form.get("amount")or"").strip()   # request.form.get() usually returns a string (str).
    date_str=(request.form.get("date")or"").strip()
    category=(request.form.get("category")or"").strip()

    if not description or not amount_str or not date_str or not category :
        flash("Please fill the information","error")

    try:
        amount=float(amount_str)
        if amount <= 0 :
            raise ValueError
        
    except ValueError:
        flash("Amount must be positive (more that 1) ",'error')
        return redirect(url_for("home"))
    
    # Try to convert the form date string into a Python date object

    try:
        # If date_str has a value:
        # Example: "2026-05-29"
        # Convert string → datetime object
        # Then .date() extracts only date part
        #
        # If date_str is empty:
        # Use today's date automatically
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()

        # If user enters invalid date format
        # Example: "abc" or "2026-99-99"
        # datetime.strptime() raises ValueError

    except ValueError:
        # Use today's date as fallback
        d = date.today()

    new_expense=Expense(description=description, amount=amount, category=category, date=d)
    db.session.add(new_expense)
    db.session.commit()

    flash("Expense add",'success')


    print("form received",dict(request.form))
    return redirect(url_for('home'))

@app.route("/delete/<int:id>", methods=['POST'])
def del_exp(id):
    #find a record that based on id and if its not there send not found using _404
    del_id=Expense.query.get_or_404(id)
    #delete a record based on id-
    db.session.delete(del_id)
    #save the changes
    db.session.commit()

    #return a user to home page
    return redirect(url_for('home'))

@app.route("/edit/<int:exp_id>", methods=['GET'])
def edit(exp_id):
    e=Expense.query.get_or_404(exp_id)

    return render_template("edit.html", expense=e,categories=categories, today=date.today().isoformat())

@app.route("/edit_record/<int:id>", methods=['POST']) #@app.route("/edit_record/<int : id>") => Flask route parameters cannot contain spaces.
def editRecord(id):
    
    #extract only record that have id is match by given id
    data =Expense.query.get_or_404(id)

    print(data)
    description=(request.form.get("description") or "").strip()
    amount_str=(request.form.get("amount") or "").strip()
    date_str=(request.form.get("date") or "").strip()
    category=(request.form.get("category") or "").strip()

    if description or not amount_str or not date_str or not category :
        flash("Fill the all filed","error")

    try :
        amount=float(amount_str)
        if amount <= 0:
            raise ValueError
        
    except ValueError:
        flash("The amount should be More than ₹ 0 ")
        redirect(url_for('edit'))
    
    try:
        date= datetime.strptime(date_str,"%Y-%m-%d").date() if date_str else date.today()
        if date > date.today():
            raise ValueError
    except ValueError :
        flash(" Select correct date")

    data.description = description
    data.amount = amount
    data.date = date
    data.category = category

    db.session.commit()

    flash("Record id update ", "success")
    
    return redirect(url_for("home"))

    

    

@app.route("/export_csv")
def exportCsv():
    start = (request.args.get("start_str") or "").strip()
    end = (request.args.get("end_str") or "").strip()
    category = (request.args.get("category") or "").strip()

    start_date=parse_date_or_none(start)
    end_date=parse_date_or_none(end)

    # print("start =", start)
    # print("end =", end)
    # print("category =", category)
    # print("start_date =", start_date)
    # print("end_date =", end_date)


    q=Expense.query

    if start:
        q=q.filter(Expense.date >= start)
    if end:
        q=q.filter(Expense.date <= end)
    if category :
        q=q.filter(Expense.category == category)

    expenses = q.order_by(Expense.date.desc() , Expense.id).all()

    # This is one of the way to create a csv file data

    # lines = ["date, descrption, category, amount"]

    # for e in expenses:
    #     lines.append(f"{e.date.isoformat()}, {e.description}, {e.category}, {e.amount: .2f}")
    
    # csv_data = "\n".join(lines)

    # This is another of the way to create a csv file data

    output = io.StringIO() #StringIO() creates a temporary text file name of output in memory (RAM).

    writer=csv.writer(output) # Whenever I use writer.writerow(), write the data into output in CSV format.

    # Write column headings
    writer.writerow(["Id", "Date" ,"Description", "Category", "Amount"]) # This creates the first line of the CSV

    # Write each expense as a new row
    for e in expenses :
        writer.writerow([
            e.id,
            e.date.strftime("%d-%m-%Y"),
            e.description,
            e.category,
            f"{e.amount :.2f}"
        ])

    # Get all CSV content from memory as a string
    csv_data = output.getvalue()

    fname_start = start or "all"
    fname_end = end or "all"
    filename = f"Expenses_{fname_start}_to_{fname_end}.csv"

    # Send CSV data to browser
    return Response(
        csv_data,
        headers={
            # Tell browser this is a CSV file
            "Content-Type" :"text/csv",
            # Tell browser to download the file
            # instead of displaying it in the page
            "Content-Disposition": f"attachment; filename={filename}"

        }
    )

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configure MySQL database connection
db = pymysql.connect(
    host='datavista.c3m826cwe288.ap-south-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='AbhiAppu',
    db='datavista',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        city = None
        
        if role == 'STM24':
            city = request.form.get('city')

        # Verify credentials against the user table in the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM UserDetails WHERE Username = %s AND Password = %s AND RoleID = %s", (username, password, role))
        user = cursor.fetchone()

        if user:
            if role == 'STM24' and city is None:
                return redirect(url_for('error'))
            else:
                return redirect(url_for(get_role_redirect(role)))
        else:
            return redirect(url_for('error'))

    return render_template('login.html')

def get_role_redirect(role):
    role_redirects = {
        'SM24': 'sales_manager',
        'PM24': 'product_manager',
        'PTM24': 'product_team_member',
        'STM24': 'sales_team_member'
    }
    return role_redirects.get(role, 'error')

@app.route('/sales_manager')
def sales_manager():
    return render_template('sales_manager.html')

@app.route('/product_manager')
def product_manager():
    return render_template('product_manager.html')

@app.route('/sales_team_member')
def sales_team_member():
    return render_template('sales_team_member.html')

@app.route('/product_team_member')
def product_team_member():
    return render_template('product_team_member.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
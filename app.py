from flask import Flask, render_template ,request ,redirect ,url_for, session, Response, send_file, flash 
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json , math
import mysql.connector
import re,os
import hashlib ,secrets ,stripe
import pandas as pd
from faker import Faker
from openpyxl.workbook import Workbook
from openpyxl import Workbook
from openpyxl.writer.excel import save_workbook
from io import BytesIO
import io
import base64
import urllib.request
from werkzeug.utils import secure_filename
from flask import jsonify




app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Raja@123'
app.config['MYSQL_DB'] = 'ecart'



mysql = MySQL(app)



@app.route('/')
def index():
        cat = "ac"


        return render_template('index.html',category = cat)

@app.route('/products')
def products():
    category = request.args.get('category')
    cat = request.form.get('cat')
    subcategory = None
    priceval = request.args.get('price')
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort')
    # offset = (page - 1) * 10
    minp =0
    maxp = 0
    cur1 = mysql.connection.cursor()
    query1 = "SELECT pprice from products Where pcategory = '{}' ".format(category)
    params = ()
    cur1.execute(query1)
    res = cur1.fetchall()
    numeric_prices = []
    for price in res:
        numeric_prices.append(updated_price(price[0]))




    minp = min(numeric_prices)
    maxp = max(numeric_prices)





    
    
    cursor = mysql.connection.cursor()



    query = "select * from products Where pcategory = '{}' ".format(category)
    if sort:
        query += " ORDER BY title %s"
        params += (sort,)
    

    if priceval:
        query += " ORDER BY starrating %s"
        params += (sort,)
        
    cursor.execute(query,params)
    results = cursor.fetchall()





    

    column_names = [desc[0] for desc in cursor.description]
    
    products = []
    for row in results:
        product_dict = {}
        for i in range(len(column_names)):
            product_dict[column_names[i]] = row[i]
        price = product_dict['pprice']
        product_dict['price'] = updated_price(price)
        products.append(product_dict)
    
        # print(products)
     

    # cursor.execute("SELECT COUNT(*) FROM products Where pcategory = '{}'".format(category))
    # total_count = cursor.fetchone()[0]
    # total_pages = math.ceil(total_count / 10)


    cursor.execute("Select distinct psubcategory from products where pcategory = '{}'".format(category))
    subcategory = cursor.fetchall()

    cursor.execute("Select distinct pbrand from products where pcategory = '{}'".format(category))
    brand = cursor.fetchall()
    
    
    return render_template('productdis.html', tdata=products, category=category,min =minp,max = maxp,subcat = subcategory,brand = brand)


def adddollaar(val):
     
    value = int(val)
    dollar_value = "{:,.2f}".format(value/83)

    return dollar_value

@app.route('/fetchrecords', methods=['POST'])
def fetchrecords():
    cur = mysql.connection.cursor()
    query = request.form['sort']
    # query1 = request.form['sortbrand']
    category = request.form['cat']
    min = request.form['minval']
    rangeval = request.form['rangeval']

    minv = adddollaar(min)
    rangevalv = adddollaar(rangeval) 
    print(minv)
    print(rangevalv)


    products = []


    if query == 'All' and rangeval:
        cur.execute("SELECT * FROM products WHERE pcategory = %s and compprice >= %s and compprice <= %s" , (category,minv,rangevalv))
        print("i am excecuted")
    
    elif query:
        cur.execute("SELECT * FROM products WHERE pcategory = %s" , (category,))

    else:
        cur.execute('SELECT * FROM products WHERE psubcategory=%s', (query,))

    productlist = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]
    
    
    for row in productlist:
        product_dict = {}
        for i in range(len(column_names)):
            product_dict[column_names[i]] = row[i]
        price = product_dict['pprice']
        product_dict['price'] = updated_price(price)
        products.append(product_dict)

    print(products)

    htmlresponse = render_template('productcard.html', productlist=products)
    return jsonify({'htmlresponse': htmlresponse})







def updated_price(price):
       
        price_without_currency = price.replace('$', '')
        pri = float(price_without_currency)
        p = int(pri)
        updated_price = p * 83   
        return updated_price




if __name__ == '__main__':
    app.run(debug=True, port=3000)
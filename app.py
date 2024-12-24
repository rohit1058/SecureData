from flask import Flask, redirect, render_template, request, session, url_for, send_file
import mysql.connector, random, string, os, smtplib
from datetime import datetime 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "Qazwsx@123"  








link = mysql.connector.connect(
    host = 'localhost', 
    user = 'root', 
    password = '', 
    database = 'securedata_2024'
)




  





@app.after_request
def add_header(response):
  
  response.cache_control.no_store = True
  return response










@app.route('/')
def index():
  
  return render_template('index.html')    











@app.route('/login', methods=['GET', 'POST'])
def login(): 
    
  if 'user' in session:
    return redirect(url_for('upload'))

  if request.method == "GET":
    return render_template('login.html') 
    
  else:
    cursor = link.cursor()
    try: 
      email = request.form["email"]
      password = request.form["password"]

      if email == 'admin@admin.com' and password == 'admin':
        session['admin'] = 'admin@admin.com'
        session['adminname'] = 'admin' 
        return redirect(url_for('manageusers'))
      
      else:
        cursor.execute("SELECT * FROM securedata_2024_user WHERE email = '"+email+"' AND password = '"+password+"' and status = 'approved'")
        user = cursor.fetchone()
        if user:
          session['user'] = user[3]
          session['username'] = user[2] 
          return redirect(url_for('upload'))
        else:
          return render_template('login.html', error='Invalid email or password') 
      
    except Exception as e:
      error = e
      return render_template('login.html', error=error)
      
    finally:
        cursor.close() 














@app.route('/manageusers', methods=['GET', 'POST'])
def manageusers(): 
    
  if 'admin' not in session:
    return redirect(url_for('login'))
  
  
  if request.method == "GET": 

    cursor = link.cursor()
    try: 
      cursor.execute("SELECT * FROM securedata_2024_user")
      data = cursor.fetchall() 
      link.commit()
      return render_template('manageusers.html',data = data) 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close() 
  
  else:  

    cursor = link.cursor()
    try: 
      if 'accept' in request.form:
        uid = request.form["accept"]
        cursor.execute("UPDATE securedata_2024_user SET status = 'approved' where uid = '"+uid+"'")
         
      if 'reject' in request.form:
        uid = request.form["accept"]
        cursor.execute("UPDATE securedata_2024_user SET status = 'rejected' where uid = '"+uid+"'")
         
      if 'delete' in request.form:
        uid = request.form["accept"]
        cursor.execute("DELETE from securedata_2024_user where uid = '"+uid+"'")
         
      cursor.execute("SELECT * FROM securedata_2024_user")
      data = cursor.fetchall() 
      link.commit()
      return render_template('manageusers.html',data = data, success = 'User updated successfully') 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close()  












@app.route('/files', methods=['GET', 'POST'])
def files(): 
    
  if 'admin' not in session:
    return redirect(url_for('login'))
  
  
  if request.method == "GET": 

    cursor = link.cursor()
    try: 
      cursor.execute("SELECT * FROM securedata_2024_file")
      data = cursor.fetchall() 
      link.commit()
      return render_template('files.html',data = data) 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close() 
  
  else:  

    cursor = link.cursor()
    try: 
      uid = request.form["delete"] 
      cursor.execute("DELETE FROM securedata_2024_file where uid = '"+uid+"'") 
      cursor.execute("SELECT * FROM securedata_2024_file")
      data = cursor.fetchall() 
      link.commit()
      return render_template('files.html',data = data, success = 'File deleted successfully') 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close() 
 











@app.route('/transactions', methods=['GET', 'POST'])
def transactions(): 
    
  if 'admin' not in session:
    return redirect(url_for('login'))
   

  cursor = link.cursor()
  try: 
    cursor.execute("select * from securedata_2024_request where status = 'approved'")
    data = cursor.fetchall() 
    link.commit()
    return render_template('transactions.html',data = data) 
    
  except Exception as e:
    error = e
    return render_template('error.html', error=error)
      
  finally:
    cursor.close() 











@app.route('/register', methods=['GET', 'POST'])
def register():
      
  if 'user' in session:
    return redirect(url_for('upload'))

  if request.method == "GET": 
    return render_template('register.html') 
  
  else: 
    cursor = link.cursor()  
    try: 
      name = request.form["name"]
      email = request.form["email"]
      password = request.form["password"] 
      phone = request.form["phone"] 
      address = request.form["address"] 
      uid = 'uid_'+''.join(random.choices(string.ascii_letters + string.digits, k=10))
      cursor.execute("SELECT * FROM securedata_2024_user WHERE email = '"+email+"'")
      user = cursor.fetchone()
 
      if user:
        return render_template('register.html', exists='Email already exists') 
      else:
        cursor.execute("INSERT INTO securedata_2024_user (uid, name, email, password, phone, address, status) VALUES  ('"+uid+"', '"+name+"', '"+email+"', '"+password+"', '"+phone+"', '"+address+"', 'pending')")
        link.commit()
        return render_template('register.html', success='Registration successful') 
       
    except Exception as e:
      error = e
      return render_template('register.html', error=error)
      
    finally:
        cursor.close() 












@app.route('/upload', methods=['GET', 'POST'])
def upload():

  if 'user' not in session:
    return redirect(url_for('login'))
  
  if request.method == "GET": 
    return render_template('upload.html', uid = f"DOC{random.randint(1234, 999999)}", date = datetime.now().strftime("%Y-%m-%d"), uploadedby = session["username"] ) 

  else:
    cursor = link.cursor()
    try:  
      uid = request.form["uid"] 
      docname = request.form["docname"]  
      uploadeddate = request.form["uploadeddate"] 
      author = request.form["author"]  
      file = request.files["file"] 
      user = session["user"] 
      username = request.form["uploadedby"] 
      filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '\\static\\docs', file.filename) 
      file.save(filepath) 
      filepath = filepath.replace('\\', '\\\\') 
      query = "insert into securedata_2024_file (uid,user,username,date,file,filename,author,publickey,document) values ( '"+uid+"', '"+user+"', '"+username+"', '"+uploadeddate+"', '"+filepath+"', '"+file.filename+"', '"+author+"', '"+str(random.randint(1234, 999999))+"', '"+docname+"')"
      cursor.execute(query)
      link.commit() 
      return render_template('upload.html', success='Upload successful') 
    
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
      
    finally:
        cursor.close() 











@app.route('/managefiles', methods=['GET', 'POST'])
def managefiles(): 
    
  if 'user' not in session:
    return redirect(url_for('login'))
  
  
  if request.method == "GET": 

    cursor = link.cursor()
    try: 
      cursor.execute("SELECT * FROM securedata_2024_file where user = '"+session['user']+"'")
      data = cursor.fetchall() 
      link.commit()
      return render_template('managefiles.html',data = data) 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close() 
  
  else:  

    cursor = link.cursor()
    try: 
      uid = request.form["delete"] 
      cursor.execute("DELETE FROM securedata_2024_file where uid = '"+uid+"'") 
      cursor.execute("SELECT * FROM securedata_2024_file where user = '"+session['user']+"'")
      data = cursor.fetchall() 
      link.commit()
      return render_template('managefiles.html',data = data, success = 'File deleted successfully') 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close()  











@app.route('/requests', methods=['GET', 'POST'])
def requests(): 
    
  if 'user' not in session:
    return redirect(url_for('login'))
  
  
  if request.method == "GET": 

    cursor = link.cursor()
    try: 
      cursor.execute("SELECT * FROM securedata_2024_file where user != '" + session["user"] + "' and uid not in (select fid from securedata_2024_request where requestedby = '"+ session["user"] + "')")
      data = cursor.fetchall() 
      link.commit()
      return render_template('requests.html',data = data) 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close() 
  
  else:  

    cursor = link.cursor()
    try: 
      uid = request.form["request"] 
      cursor.execute("SELECT * FROM securedata_2024_file where uid = '"+uid+"'")
      data = cursor.fetchall()
      nuid = 'uid_'+''.join(random.choices(string.ascii_letters + string.digits, k=10))
      query = "insert into securedata_2024_request (uid,fid,file,filename,document,requestedby,requestedbyname,uploadedby,uploadedbyname,date,status) values('"+nuid+"','"+uid+"','"+data[0][5].replace('\\', '\\\\') +"','"+data[0][6]+"','"+data[0][9]+"','"+session['user']+"','"+session['username']+"','"+data[0][2]+"','"+data[0][3]+"','"+datetime.now().strftime("%Y-%m-%d")+"','pending')" 
      cursor.execute(query) 
      cursor.execute("SELECT * FROM securedata_2024_file where user != '" + session["user"] + "' and uid not in (select fid from securedata_2024_request where requestedby = '"+ session["user"] + "')")
      data = cursor.fetchall() 
      link.commit()
      return render_template('requests.html',data = data, success = 'File requested successfully') 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close()  













@app.route('/myrequests', methods=['GET', 'POST'])
def myrequests(): 
    
  if 'user' not in session:
    return redirect(url_for('login'))
  
  
  if request.method == "GET": 

    cursor = link.cursor()
    try: 
      cursor.execute("SELECT * FROM securedata_2024_request where uploadedby = '"+session['user']+"'")
      data = cursor.fetchall() 
      link.commit()
      return render_template('myrequests.html',data = data) 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close() 
  
  else:  

    cursor = link.cursor() 
    try:  
      uid = '' 

      if 'accept' in request.form:
        uid = request.form["accept"]
        cursor.execute("UPDATE securedata_2024_request set status = 'approved' where uid = '"+uid+"'")
        cursor.execute("SELECT * FROM securedata_2024_request where uid = '"+uid+"'")
        data = cursor.fetchall()
        document = data[0][5] 
        email = data[0][6] 
        fid = data[0][2] 
        cursor.execute("SELECT * FROM securedata_2024_file where uid = '"+fid+"'")
        data = cursor.fetchall()
        publickey = data[0][8]  
        message = MIMEMultipart()
        message['From'] = "bookswisesage@gmail.com"
        message['To'] = email
        message['Subject'] = "Secret Key for Your File"
        mail = smtplib.SMTP('smtp.gmail.com', 587) 
        mail.starttls()
        mail.login("bookswisesage@gmail.com", "lzeasjmkgblwnjhd")
        body = "The secret key for the file " + data[0][7] + " is: " + publickey
        message.attach(MIMEText(body, 'plain'))
        mail.sendmail("bookswisesage@gmail.com", email, message.as_string())
        mail.quit()  

      if 'reject' in request.form:
        uid = request.form["reject"]
        cursor.execute("UPDATE securedata_2024_request set status = 'rejected' where uid = '"+uid+"'") 
         
      cursor.execute("SELECT * FROM securedata_2024_request where uploadedby = '"+session['user']+"'")
      data = cursor.fetchall() 
      link.commit()
      return render_template('myrequests.html',data = data, success = 'Request updated successfully') 
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally:
      cursor.close()












@app.route('/download', methods=['GET', 'POST'])
def download(): 
    
  if 'user' not in session:
    return redirect(url_for('login'))
  
  
  if request.method == "GET": 
    return render_template('download.html')  
  
  else:  

    cursor = link.cursor()
    try: 
      publickkey = request.form["secretkey"] 
      user = session["user"] 
      cursor.execute("SELECT uid FROM securedata_2024_file where publickey = '"+publickkey+"'")  
      fdata = cursor.fetchall() 
      if len (fdata) == 0:
        return render_template('download.html', error = 'Invalid Secret Key')
      else: 
        fid = fdata[0][0]  
        cursor.execute("SELECT file FROM securedata_2024_request where fid = '"+fid+"' and requestedby = '"+user+"' and status = 'approved'")  
        rdata = cursor.fetchall()   
        if len (rdata) == 0:
          return render_template('download.html', error = 'You don''t have permission to download this file ')
        else:
          cursor.execute("UPDATE securedata_2024_file set publickey = '"+str(random.randint(1234, 999999))+"' where uid = '"+fid+"'") 
          path = rdata[0][0]
          return send_file(path, as_attachment=True)  
          
      
    except Exception as e:
      error = e
      return render_template('error.html', error=error)
        
    finally: 
      link.commit()
      cursor.close()












@app.route('/logout')
def logout():
    
    session.pop('user', None)
    session.pop('username', None)
    return redirect(url_for('index'))









if __name__ == '__main__':
    app.run(debug=True)

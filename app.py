from flask import Flask, request, redirect, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "book_exchange_123"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        phone TEXT,
        city TEXT,
        address TEXT
    )
    """)
   
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        category TEXT,
        description TEXT,
        status TEXT,
        owner TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        book_id INTEGER,
        status TEXT
    )
    """)
    try:
        cur.execute("ALTER TABLE books ADD COLUMN description TEXT")
    except:
        pass

    try:
        cur.execute("ALTER TABLE books ADD COLUMN status TEXT DEFAULT 'Available'")
    except:
        pass
    try:
        cur.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    except:
        pass

    try:
        cur.execute("ALTER TABLE users ADD COLUMN city TEXT")
    except:
        pass

    try:
        cur.execute("ALTER TABLE users ADD COLUMN address TEXT")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

# ---------------- CSS ----------------

style = """
<style>

body{
    margin:0;
    font-family:Arial;
    background:#f2f2f2;
}

nav{
    background:#2c3e50;
    padding:15px;
}

nav a{
    color:white;
    text-decoration:none;
    margin-right:20px;
    font-weight:bold;
}

.container{
    width:80%;
    margin:auto;
    margin-top:30px;
}

.card{
    background:white;
    padding:25px;
    border-radius:10px;
    box-shadow:0px 0px 10px lightgray;
}

input{
    width:96%;
    padding:10px;
    margin:10px 0;
}
select{

width:100%;

padding:10px;

margin:10px 0;

border-radius:5px;

border:1px solid gray;

}

button{
    background:#3498db;
    color:white;
    border:none;
    padding:10px 20px;
    cursor:pointer;
}

button:hover{
    background:#2980b9;
}

table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}

table,th,td{
    border:1px solid gray;
}

th,td{
    padding:10px;
    text-align:center;
}

.card:hover{
    transform:scale(1.02);
    transition:0.3s;
}

button{
    border-radius:5px;
}

input{
    border-radius:5px;
    border:1px solid gray;
}

nav{
    box-shadow:0px 3px 8px gray;
}

table tr:nth-child(even){
    background:#f5f5f5;
}
.card:hover{
    transform:scale(1.02);
    transition:.3s;
}

button{
    border-radius:6px;
    padding:10px 20px;
}

button:hover{
    background:#2c80b4;
}

input{
    border-radius:5px;
    border:1px solid #ccc;
}

nav{
    box-shadow:0px 2px 10px gray;
}

table tr:nth-child(even){
    background:#f8f8f8;
}

h1{
    color:#2c3e50;
}

h2{
    color:#3498db;
}

a{
    text-decoration:none;
}
</style>
"""
#--------Home------
@app.route("/")
def home():

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    conn.close()

    return render_template_string(f"""

    {style}

    <nav>

    <a href="/">Home</a>

    <a href="/all_books">Browse Books</a>

    <a href="/register">Register</a>

    <a href="/login">Login</a>

    </nav>

    <div class="container">

    <div class="card">

    <center>

    <h1>📚 Book Exchange System</h1>

    <h3>Read • Share • Exchange</h3>

    <p>

    Discover books from people around you.
    Exchange your old books with others.
    Read more while spending less.

    </p>

    <br>

    <h2>Total Books : {total_books}</h2>

    <br>

    <a href="/all_books">

    <button>Browse Books</button>

    </a>

    <a href="/register">

    <button>Join Now</button>

    </a>

    </center>

    </div>

    </div>

    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>

    """)
# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        phone=request.form["phone"]
        city=request.form["city"]
        address=request.form["address"]

        try:

            conn=sqlite3.connect("books.db")
            cur=conn.cursor()

            cur.execute(
                "INSERT INTO users(name,email,password,phone,city,address) VALUES(?,?,?,?,?,?)",
                (name,email,password,phone,city,address)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except Exception as e:
            return f"<h3>{e}</h3>"

    return render_template_string(f"""

    {style}

    <div class="container">

    <div class="card">

    <h2>User Registration</h2>

    <form method="POST">

    <input type="text" name="name" placeholder="Full Name" required>

    <input type="email" name="email" placeholder="Email" required>

    <input type="password" name="password" placeholder="Password" required>
    <input type="text"
    name="phone"
    placeholder="Mobile Number"
    required>

    <input type="text"
    name="city"
    placeholder="City"
    required>

    <textarea
    name="address"
    placeholder="Full Address"
    rows="3"
    style="width:100%;padding:10px;"
    required></textarea>

    <button>Register</button>

    </form>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>
    </div>

    </div>

    """)

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=sqlite3.connect("books.db")
        cur=conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user=cur.fetchone()

        conn.close()

        if user:

            session["user"]=user[1]

            return redirect("/dashboard")

        return "<h3>Invalid Email or Password</h3>"

    return render_template_string(f"""

    {style}

    <div class="container">

    <div class="card">

    <h2>User Login</h2>

    <form method="POST">

    <input type="email" name="email" placeholder="Email" required>

    <input type="password" name="password" placeholder="Password" required>

    <button>Login</button>

    </form>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>
    </div>

    </div>

    """)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    # My Books
    cur.execute("SELECT * FROM books WHERE owner=?", (session["user"],))
    books = cur.fetchall()

    # Dashboard Statistics
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM books WHERE owner=?", (session["user"],))
    my_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM requests WHERE receiver=? AND status='Pending'",
        (session["user"],)
    )
    pending = cur.fetchone()[0]

    conn.close()

    rows = ""

    if len(books) == 0:

        rows = """
        <tr>
            <td colspan="3">No Books Added Yet</td>
        </tr>
        """

    else:

        for b in books:

            rows += f"""
            <tr>

            <td>{b[1]}</td>

            <td>{b[2]}</td>

            <td>{b[3]}</td>
            
            <td>{b[5]}</td>

            </tr>
            """

    return render_template_string(f"""

    {style}

    <nav>

    <a href="/dashboard">Dashboard</a>

    <a href="/add_book">Add Book</a>

    <a href="/all_books">Browse Books</a>

    <a href="/my_requests">My Requests</a>
    
    <a href="/sent_requests">Sent Requests</a>

    <a href="/profile">Profile</a>

    <a href="/logout">Logout</a>

    </nav>

    <div class="container">

    <div class="card">

    <h2>Welcome, {session["user"]}</h2>

    <p>Manage your books and exchange requests.</p>

    <br>

    <div style="display:flex;gap:15px;flex-wrap:wrap;">

        <div style="background:#3498db;color:white;padding:20px;border-radius:10px;width:180px;text-align:center;">
            <h3>Total Books</h3>
            <h2>{total_books}</h2>
        </div>

        <div style="background:#2ecc71;color:white;padding:20px;border-radius:10px;width:180px;text-align:center;">
            <h3>My Books</h3>
            <h2>{my_books}</h2>
        </div>

        <div style="background:#9b59b6;color:white;padding:20px;border-radius:10px;width:180px;text-align:center;">
            <h3>Total Users</h3>
            <h2>{total_users}</h2>
        </div>

        <div style="background:#e67e22;color:white;padding:20px;border-radius:10px;width:180px;text-align:center;">
            <h3>Pending Requests</h3>
            <h2>{pending}</h2>
        </div>

    </div>

    <br>

    <a href="/add_book"><button>Add New Book</button></a>

    <a href="/all_books"><button>Browse Books</button></a>

    <a href="/my_requests"><button>My Requests</button></a>

    <br><br>

    <h3>My Books</h3>

    <table>

    <tr>

    <th>Book</th>

    <th>Author</th>

    <th>Category</th>

    <th>Status</th>

    <textarea
    name="description"
    placeholder="Book Description"
    rows="4"
    style="width:100%;padding:10px;"></textarea>

    </tr>

    {rows}

    </table>

    </div>

    </div>

    """)
    # ------Add_Book---------
@app.route("/add_book",methods=["GET","POST"])
def add_book():

    if "user" not in session:
        return redirect("/login")

    if request.method=="POST":

        title=request.form["title"]
        author=request.form["author"]
        category=request.form["category"]
        description=request.form["description"]
        status="Available"
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()

        cur.execute(
            "INSERT INTO books(title,author,category,description,status,owner) VALUES(?,?,?,?,?,?)",
            (title,author,category,description,status,session["user"])
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template_string(f"""

    {style}
    <nav>

    <a href="/dashboard">Dashboard</a>

    <a href="/all_books">Browse Books</a>

    <a href="/add_book">Add Book</a>

    <a href="/my_requests">Received Requests</a>

    <a href="/sent_requests">Sent Requests</a>

    <a href="/logout">Logout</a>

    </nav>

    <div class="container">

    <div class="card">

    <h2>Add Book</h2>

    <p>

    Fill the details below to share your book with other users.

    </p>

    <form method="POST">

    <input name="title" placeholder="Book Name" required>

    <input name="author" placeholder="Author Name" required>

    <select name="category" placeholder="Category" required>
    
    <option value="">Select Category</option>

    <option>Programming</option>

    <option>Science</option>

    <option>Technology</option>

    <option>History</option>

    <option>Biography</option>

    <option>Novel</option>

    <option>Education</option>

    <option>Comics</option>

    <option>Other</option>

    </select>
    <input
    type="text"
    name="description"
    placeholder="Book Description"
    required>
    <button>Add Book</button>
    
    </form>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>
    </div>

    </div>

    """) 
    #-----All Book-------
@app.route("/all_books", methods=["GET", "POST"])
def all_books():

    
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    if request.method == "POST":

        keyword = request.form["keyword"]

        cur.execute("""
        SELECT * FROM books
        WHERE title LIKE ?
        OR author LIKE ?
        OR category LIKE ?
        """, (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        ))

    else:

        cur.execute("SELECT * FROM books")

    books = cur.fetchall()

    conn.close()

    table = ""
    if len(books)==0:

        table="""

        <tr>

            <td colspan="5">

                No Books Available

            </td>

        </tr>

        """

    for b in books:

    # Action button
        if "user" not in session:

            action = '<a href="/login">Login to Request</a>'

        elif b[6] == session["user"]:

            action = f'''
            <a href="/edit_book/{b[0]}">Edit</a> |
            <a href="/delete_book/{b[0]}">Delete</a>
            '''

        else:

            if b[5] == "Available":

                action = f'''
                <a href="/request/{b[0]}">Request Book</a>
                '''

            else:

                action = "Exchanged"

        table += f"""
        <tr>
            <td>{b[1]}</td>
            <td>{b[2]}</td>
            <td>{b[3]}</td>
            <td>{b[4]}</td>
            <td>{b[5]}</td>
            <td>{b[6]}</td>
            <td>{action}</td>
        </tr>
        """
    return render_template_string(f"""

    {style}

    <nav>

        <a href="/dashboard">Dashboard</a>
        <a href="/add_book">Add Book</a>
        <a href="/my_requests">My Requests</a>
        <a href="/sent_requests">Sent Requests</a>
        <a href="/logout">Logout</a>

    </nav>

    <div class="container">

    <div class="card">

    <h2>Available Books</h2>

    <form method="POST">

        <input
            type="text"
            name="keyword"
            placeholder="Search by Book, Author or Category">

        <button type="submit">
            Search
        </button>

    </form>

    <table>

    <tr>

        <th>Book</th>
        <th>Author</th>
        <th>Category</th>
        <th>Description</th>
        <th>Status</th>
        <th>Owner</th>
        <th>Action</th>
        

    </tr>

    {table}

    </table>

    </div>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>

    </div>

    """)
    #-----delete Book----------
@app.route("/delete_book/<int:id>")
def delete_book(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM books WHERE id=? AND owner=?",
        (id, session["user"])
    )

    conn.commit()
    conn.close()

    return redirect("/all_books")
    #------Edit Book-------
@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]

        cur.execute("""
        UPDATE books
        SET title=?, author=?, category=?
        WHERE id=? AND owner=?
        """, (title, author, category, id, session["user"]))

        conn.commit()
        conn.close()

        return redirect("/all_books")

    cur.execute(
        "SELECT * FROM books WHERE id=? AND owner=?",
        (id, session["user"])
    )

    book = cur.fetchone()

    conn.close()

    if not book:
        return "Book not found."

    return render_template_string(f"""

    {style}

    <div class="container">

    <div class="card">

    <h2>Edit Book</h2>

    <form method="POST">

    <input type="text"
           name="title"
           value="{book[1]}"
           required>

    <input type="text"
           name="author"
           value="{book[2]}"
           required>

    <input type="text"
           name="category"
           value="{book[3]}"
           required>

    <button type="submit">
        Update Book
    </button>

    </form>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>
    </div>

    </div>

    """)
    #-------Edit Book-------
@app.route("/request/<int:book_id>")
def request_book(book_id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("SELECT owner FROM books WHERE id=?", (book_id,))
    book = cur.fetchone()

    if not book:
        conn.close()
        return "Book not found"

    receiver = book[0]

    cur.execute("""
        INSERT INTO requests(sender, receiver, book_id, status)
        VALUES (?, ?, ?, ?)
    """, (session["user"], receiver, book_id, "Pending"))

    conn.commit()
    conn.close()

    return redirect("/my_requests")
#-------My Request--------
@app.route("/my_requests")
def my_requests():

    if "user" not in session:
        return redirect("/login")
    
    print("Logged in user:", session["user"])


    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT
        requests.id,
        books.title,
        requests.sender,
        requests.status,
        users.phone,
        users.city,
        users.address
    FROM requests
    JOIN books
    ON requests.book_id = books.id
    JOIN users
    ON requests.sender = users.name
    WHERE requests.receiver = ?
    """, (session["user"],))

    data = cur.fetchall()
    conn.close()

    rows = ""

    for r in data:
        rows += f"""
        <tr>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td>{r[3]}</td>
            <td>{r[4]}</td>
            <td>{r[5]}</td>
            <td>{r[6]}</td>
            <td>
                <a href="/accept/{r[0]}">Accept</a> |
                <a href="/reject/{r[0]}">Reject</a>
            </td>
        </tr>
        """

    return render_template_string(f"""

    {style}
    <nav>
        <a href="/dashboard">Dashboard</a>
        <a href="/all_books">Browse Books</a>
        <a href="/add_book">Add Book</a>
        <a href="/my_requests">Received Requests</a>
        <a href="/sent_requests">Sent Requests</a>
        <a href="/logout">Logout</a>
    </nav>

    <div class="container">

    <div class="card">

    <h2>My Requests</h2>

    <table>

    <tr>
        <th>Book</th>
        <th>Sender</th>
        <th>Status</th>
        <th>Phone</th>
        <th>City</th>
        <th>Address</th>
        <th>Action</th>
    </tr>

    {rows}

    </table>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>
    </div>

    </div>

    """)
    #------sent request-------
@app.route("/sent_requests")
def sent_requests():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT
        books.title,
        requests.receiver,
        requests.status,
        users.phone,
        users.city,
        users.address
    FROM requests
    JOIN books
        ON requests.book_id = books.id
    JOIN users
        ON requests.receiver = users.name
    WHERE requests.sender = ?
    """, (session["user"],))
    data = cur.fetchall()

    conn.close()

    rows=""

    for r in data:

        rows += f"""
        <tr>
            <td>{r[0]}</td>   <!-- Book -->
            <td>{r[1]}</td>   <!-- Owner -->
            <td>{r[2]}</td>   <!-- Status -->
            <td>{r[3]}</td>   <!-- Phone -->
            <td>{r[4]}</td>   <!-- City -->
            <td>{r[5]}</td>   <!-- Address -->
        </tr>
        """

    if rows=="":

        rows="""
        <tr>
        <td colspan="3">No Requests Sent</td>
        </tr>
        """

    return render_template_string(f"""

    {style}

    <nav>

        <a href="/dashboard">Dashboard</a>
        <a href="/all_books">Browse Books</a>
        <a href="/my_requests">Received Requests</a>
        <a href="/sent_requests">Sent Requests</a>
        <a href="/logout">Logout</a>

    </nav>

    <div class="container">

    <div class="card">

    <h2>Sent Requests</h2>

    <table>

    <tr>

        <th>Book</th>
        <th>Owner</th>
        <th>Status</th>
        <th>Phone</th>
        <th>City</th>
        <th>Address</th>

    </tr>

    {rows}

    </table>

    </div>

    </div>

    """)
    #-------Accept Request-----
@app.route("/accept/<int:id>")
def accept(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    print("Accept route called")

    # Request Accept
    cur.execute(
        "UPDATE requests SET status='Accepted' WHERE id=?",
        (id,)
    )

    # Book ID
    cur.execute(
        "SELECT book_id FROM requests WHERE id=?",
        (id,)
    )

    book_id = cur.fetchone()[0]
    print("Book ID =", book_id)

    # Book Status Update
    cur.execute(
        "UPDATE books SET status='Exchanged' WHERE id=?",
         (book_id,)
    )

    print("Rows Updated =", cur.rowcount)

    # Check Database
    cur.execute(
        "SELECT id, title, status FROM books WHERE id=?",
        (book_id,)
    )

    print("Book After Update =", cur.fetchone())

    # Reject other requests
    cur.execute("""
        UPDATE requests
        SET status='Rejected'
        WHERE book_id=?
        AND id!=?
        AND status='Pending'
    """, (book_id, id))

    conn.commit()
    conn.close()

    return redirect("/my_requests")
   
    #-----Reject Request------
@app.route("/reject/<int:id>")
def reject(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE requests SET status='Rejected' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/my_requests")
    #--------User Profile page-------
@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT name,email FROM users WHERE name=?",
        (session["user"],)
    )

    user = cur.fetchone()

    conn.close()

    return render_template_string(f"""

    {style}

    <nav>

    <a href="/dashboard">Dashboard</a>
    <a href="/all_books">All Books</a>
    <a href="/logout">Logout</a>

    </nav>

    <div class="container">

    <div class="card">

    <h2>User Profile</h2>

    <h3>Name : {user[0]}</h3>

    <h3>Email : {user[1]}</h3>
    <hr>

    <center>

    <p>

    © 2026 Book Exchange System

    Developed using Python Flask & SQLite

    </p>

    </center>
    </div>

    </div>

    """)   
# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
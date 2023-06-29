import flask

from app import create_library_app, db
from app.models import Books, Members, Transactions, TransactionTypesEnum
from flask import request, render_template, redirect
from datetime import datetime

app = create_library_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/available_books/list", methods=["GET"])
def get_books():
    books = Books.query.all()
    return render_template('book_list.html', books=books)


@app.route("/available_books/<int:isbn>", methods=['GET'])
def get_isbn_available(isbn):
    book_by_isbn = Books.query.get(isbn)
    if book_by_isbn is None:
        return "Book not in stock"
    return render_template("view_book.html", book=book_by_isbn)


@app.route("/available_books/delete/<int:isbn>", methods=["GET"])
def delete_book_isbn(isbn):
    book_entry = Books.query.get(isbn)
    if book_entry is None:
        return "No deletion book does not exist"
    db.session.delete(book_entry)
    db.session.commit()
    return redirect("/available_books/list")


@app.route("/get_update_books/<int:isbn>", methods=['GET'])
def getupdatebooksform(isbn):
    book = Books.query.get(isbn)
    return render_template("update_book_form.html", context=book)


@app.route("/available_books/<int:isbn>", methods=['POST'])
def update_book_isbn(isbn):
    if not request.form:
        return "error_message""!" "No form found"
    update_book = Books.query.get(isbn)
    if update_book is None:
        return "No book with the given ISBN found"
    update_book.isbn = request.form.get('isbn', update_book.isbn)
    print(request.form)
    update_book.author = request.form.get('author', update_book.author)
    update_book.title = request.form.get('title', update_book.title)
    update_book.book_price = request.form.get('book_price', update_book.book_price)
    update_book.quantity_available = request.form.get('quantity_available', update_book.quantity_available)
    db.session.commit()
    return redirect(f"/available_books/{update_book.isbn}")
    # return render_template("view.html", context=update_book)


@app.route("/get_add_books", methods=['GET'])
def getaddbooksform():
    return render_template("add_book_form.html")


@app.route("/add_books", methods=["POST"])
def insert_book_record():
    isbn = request.form.get('isbn')
    existing_book = Books.query.get(isbn)
    if existing_book is not None:
        return f"Book ISBN {existing_book} already exists"
    else:
        new_book = Books()
        new_book.isbn = request.form.get('isbn')
        new_book.author = request.form.get('author')
        new_book.title = request.form.get('title')
        new_book.book_price = request.form.get('book_price')
        new_book.quantity_available = request.form.get('quantity_available')

        db.session.add(new_book)
        db.session.commit()
        return redirect(f"/available_books/{new_book.isbn}")


@app.route("/members/list", methods=["GET"])
def get_members():
    present_members = Members.query.all()
    return render_template("members_list.html", members=present_members)


@app.route("/members/<int:id>", methods=["GET"])
def get_member_id(id):
    available_member = Members.query.get(id)
    if available_member is None:
        return f"Member id {available_member} does not exist"
    return render_template("view_member.html", member=available_member)


@app.route("/get_update_members/<int:id>", methods=['GET'])
def getupdatememberform(id):
    member = Members.query.get(id)
    return render_template("update_member_form.html", context=member)


@app.route("/update_member/<int:id>", methods=["POST"])
def update_member_table(id):
    if not request.form:
        return render_template({"error": "Content type is not a Form"})
    update_member = Members.query.get(id)
    if update_member is None:
        return "Member id does not exist"
    update_member.id = request.form.get("id", update_member.id)
    update_member.name = request.form.get("name", update_member.name)
    update_member.account_balance = request.form.get("account_balance", update_member.account_balance)
    db.session.commit()
    return redirect(f"/members/{update_member.id}")


@app.route("/get_add_member", methods=['GET'])
def getaddmemberform():
    return render_template("add_member_form.html")


@app.route("/add_member", methods=["POST"])
def insert_member():
    print(request.form)
    new_member = Members()
    new_member.name = request.form.get("name")
    new_member.account_balance = int(request.form.get("account_balance"))
    db.session.add(new_member)
    db.session.commit()
    return redirect(f"/members/{new_member.id}")


@app.route("/members/delete/<id>", methods=["GET"])
def delete_member_id(id):
    delete_member = Members.query.get(id)
    if delete_member is None:
        return "Member does not exist"
    db.session.delete(delete_member)
    db.session.commit()
    return redirect(f"/members/list")


@app.route("/get_issue_book", methods=["GET"])
def get_issue_book():
    all_books = Books.query.all()
    all_members = Members.query.all()
    return render_template("issue_book_form.html", books=all_books, members=all_members)


@app.route("/issue_book", methods=["POST"])
def issue_book():
    """
    To issue a book requirements:
    You need bookid(isbn), member_id, available_books_in stock
    verify if the bookid and isbn are valid
    check for quantity_available for issuing from books table and member account balance
    if quantity_available is greater or equal to one and member_account_balance is not zero, issue the book by recording a transaction type of borrowed
    reduce quantity_available from books table
    :return:
    """
    print(request.form)
    book_isbn = request.form.get("book_isbn")
    member_id = request.form.get("member_id")
    quantity_borrowed = int(request.form.get("quantity_borrowed"))

    existing_book = Books.query.get(book_isbn)
    existing_member = Members.query.get(member_id)

    if existing_member is None:
        return f"Invalid Member {existing_member}"
    if existing_book is None:
        return f"Book {existing_book} does not exist!"
    if quantity_borrowed > 1:
        return "Error!" f"Cannot issue more than 1 book of title {existing_book.title}"

    present_quantity = existing_book.quantity_available
    account_balance_available = existing_member.account_balance
    price_of_book = existing_book.book_price
    if account_balance_available < 500:
        return "Error!" f"{existing_member.name} does not have sufficient funds to perform this transaction balance should be greater or equal to 5 00. Your bank balance is {existing_member.account_balance}"
    if present_quantity < 1:
        return "Error!" f"Insufficient books in stock. Books present {present_quantity}"
    if account_balance_available < price_of_book:
        return "Error!" f"Insufficient funds in account. Balance is {account_balance_available}"
    transaction = Transactions()
    transaction.member_id = existing_member.id
    transaction.book_isbn = existing_book.isbn
    transaction.transaction_type = TransactionTypesEnum.borrowed
    transaction.date_time_of_transaction = datetime.now()
    transaction.cost = 0
    existing_book.quantity_available = present_quantity - 1
    db.session.add(transaction)
    db.session.commit()

    return render_template("view_transactions.html", transaction=transaction)


@app.route("/get_return_book", methods=["GET"])
def get_return_book():
    all_books = Books.query.all()
    all_members = Members.query.all()
    return render_template("return_book_form.html", books=all_books, members=all_members)


@app.route("/return_book_to_store", methods=["POST"])
def return_book():
    """
    get the book isbn, member_id
    compare the book isbn and member_id with that of book issued

    add the quantity_available in the books table and record transaction type in the transaction table as returned
    :return: transaction in json format
    """
    book_isbn = request.form.get("book_isbn")
    member_id = request.form.get("member_id")

    existing_member = Members.query.get(member_id)
    existing_book = Books.query.get(book_isbn)

    if existing_book is None:
        return "Error!" f"Book record {existing_book} of does not exist!"
    if existing_member is None:
        return "Error!" f"Member {existing_member} not found!"

    previous_transaction = Transactions.query.filter_by(member_id=member_id, book_isbn=book_isbn,
                                                        transaction_type="borrowed").all()

    account_balance_available = existing_member.account_balance
    update_quantity = existing_book.quantity_available
    price_of_book = existing_book.book_price

    if len(previous_transaction) == 0:
        return "Error!" "Transaction does not exist!"

    if account_balance_available < price_of_book:
        return "Error!" "Transaction failed due to insufficient funds!"

    transaction = Transactions()

    transaction.book_isbn = existing_book.isbn
    transaction.member_id = existing_member.id
    transaction.quantity_borrowed = transaction.quantity_borrowed
    transaction.cost = existing_book.book_price
    transaction.date_time_of_transaction = datetime.now()
    transaction.transaction_type = TransactionTypesEnum.returned.value

    existing_book.quantity_available = update_quantity + 1
    existing_member.account_balance = account_balance_available - transaction.cost

    db.session.add(transaction)
    db.session.commit()
    return render_template("view_transactions.html", transaction=transaction)


@app.route("/get_search_book", methods=["GET"])
def get_search_book():
    return render_template("search_book_form.html")


@app.route("/search_book", methods=["POST"])
def search_book_entry():
    title = request.form.get("title", "")
    author = request.form.get("author", "")

    from sqlalchemy import or_
    book = Books.query.filter(or_(Books.title.ilike(title), Books.author.ilike(author))).all()
    return render_template("book_list.html", books=book)

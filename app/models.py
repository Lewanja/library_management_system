import enum

from . import db


class Books(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    book_price = db.Column(db.Integer)
    quantity_available = db.Column(db.Integer, default=1)
    book_transactions = db.relationship("Transactions", back_populates="book")

    def books_to_json(self):
        return {
            "isbn": self.isbn,
            'author': self.author,
            "title": self.title,
            'book_price': self.book_price,
            'quantity_available': self.quantity_available

        }


class Members(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    account_balance = db.Column(db.Float, default=0)
    member_transactions = db.relationship("Transactions", back_populates="member")

    def members_to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "account_balance": self.account_balance
        }


class TransactionTypesEnum(enum.Enum):
    borrowed = "borrowed"
    returned = "returned"


class Transactions(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_isbn = db.Column(db.Integer, db.ForeignKey('books.isbn'))
    book = db.relationship('Books', back_populates="book_transactions")
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    member = db.relationship("Members", back_populates="member_transactions")
    quantity_borrowed = db.Column(db.Integer, default=1)
    cost = db.Column(db.Float, default=0.0)
    date_time_of_transaction = db.Column(db.DateTime)
    transaction_type = db.Column(db.Enum(TransactionTypesEnum))

    def transactions_to_json(self):
        return {
            "transaction_id": self.transaction_id,
            "book_isbn": self.book_isbn,
            "member_id": self.member_id,
            "quantity_borrowed": self.quantity_borrowed,
            "cost": self.cost,
            "date_time_of_transaction": self.date_time_of_transaction,
            "transaction_type": self.transaction_type.value
        }

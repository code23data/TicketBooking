from .database import db


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    bookings = db.relationship("Bookings", backref="user")


class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String, nullable=False)


booking_table = db.Table(
    "booking",
    db.Column("show_id", db.Integer, db.ForeignKey("shows.s_id")),
    db.Column("venue_id", db.Integer, db.ForeignKey("venues.v_id")),
)


class Shows(db.Model):
    __tablename__ = "shows"
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String, nullable=False)
    s_rating = db.Column(db.Numeric(1, 2))  # Rating is a value between 0 to 5
    s_time = db.Column(db.String, nullable=False)
    s_tags = db.Column(db.String, nullable=False)
    s_price = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer)
    venues = db.relationship(
        "Venues", secondary=booking_table, backref="available_shows"
    )
    bookings = db.relationship("Bookings", backref="shows")


class Venues(db.Model):
    __tablename__ = "venues"
    v_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    v_name = db.Column(db.String, nullable=False)
    v_place = db.Column(db.String, nullable=False)
    v_location = db.Column(db.String, nullable=False)
    v_capacity = db.Column(db.Integer, nullable=False)
    bookings = db.relationship("Bookings", backref="venues")


class Bookings(db.Model):
    __tablename__ = "bookings"
    b_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    show_id = db.Column(db.Integer, db.ForeignKey("shows.s_id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.v_id"))
    tickets = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)

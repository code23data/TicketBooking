from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import current_app as app
from application.models import *  # (table class name)


# Home Page
@app.route("/", methods=["GET", "POST"])
def loginpage():
    return render_template("login.html")


# ===================================LOGIN PAGES===================================


# Admin login page
@app.route("/login/admin", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        a = Admin.query.all()
        for a in a:
            if (
                a.password == request.form["admin_password"]
                and a.username == request.form["admin_username"]
            ):
                return redirect(f"/{a.admin_id}/dashboard/home")
    return render_template("adminlogin.html")


# User login page
@app.route("/login/user", methods=["GET", "POST"])
def userlogin():
    if request.method == "POST":
        a = User.query.all()
        for a in a:
            if (
                a.password == request.form["user_password"]
                and a.username == request.form["user_username"]
            ):
                return redirect(f"/{a.user_id}/dashboard")
    return render_template("userlogin.html")


# ===================================ADMIN DASHBOARD===================================


# Home page of admin dashboard
@app.route("/<int:admin_id>/dashboard/home", methods=["GET", "POST"])
def admin_home(admin_id):
    a = Admin.query.get(admin_id)
    usr = a.username
    venues = Venues.query.all()
    shows = Shows.query.all()
    return render_template(
        "admindashboard.html",
        admin_user=usr,
        shows=shows,
        no_of_shows=Shows.query.count(),
        venues=venues,
        no_of_venues=Venues.query.count(),
        admin_id=admin_id,
    )


# ===================================CREATE VENUE===================================


# Admin can create a venue in this page
@app.route("/<int:admin_id>/dashboard/create/venue", methods=["GET", "POST"])
def create_venue(admin_id):
    a = Admin.query.get(admin_id)
    if request.method == "POST":
        name = request.form.get("venue")
        place = request.form.get("place")
        location = request.form.get("location")
        capacity = request.form.get("capacity")
        db.session.add(
            Venues(v_name=name, v_place=place, v_location=location, v_capacity=capacity)
        )
        db.session.commit()
        return redirect(f"/{admin_id}/dashboard/home")
    return render_template(
        "venuecreate.html", admin_user=a.username, admin_id=a.admin_id
    )


# ===================================UPDATE VENUE===================================


# Admin can edit (update) a venue in this page
@app.route(
    "/<int:admin_id>/dashboard/edit/venue/<int:venue_id>", methods=["GET", "POST"]
)
def edit_venue(admin_id, venue_id):
    a = Admin.query.get(admin_id)
    v = Venues.query.get(venue_id)
    if request.method == "POST":
        v.v_name = request.form.get("venue")
        v.v_place = request.form.get("place")
        v.v_location = request.form.get("location")
        v.v_capacity = request.form.get("capacity")
        db.session.commit()
        return redirect(f"/{admin_id}/dashboard/home")
    return render_template(
        "venueupdate.html",
        admin_user=a.username,
        this_venue=v.v_name,
        admin_id=a.admin_id,
        venue_id=venue_id,
    )


# ===================================DELETE VENUE===================================


# Admin can delete a venue in this page
@app.route(
    "/<int:admin_id>/dashboard/delete/venue/<int:venue_id>", methods=["GET", "POST"]
)
def delete_venue(admin_id, venue_id):
    a = Admin.query.get(admin_id)
    v = Venues.query.get(venue_id)
    db.session.delete(v)
    db.session.commit()
    return redirect(f"/{admin_id}/dashboard/home")


# ===================================CREATE SHOW===================================


# Admin can create a show in this page
@app.route(
    "/<int:admin_id>/dashboard/create/<int:venue_id>/show", methods=["GET", "POST"]
)
def create_show(admin_id, venue_id):
    a = Admin.query.get(admin_id)
    v = Venues.query.get(venue_id)
    if request.method == "POST":
        show = request.form.get("show")
        ratings = request.form.get("rating")
        timings = request.form.get("timings")
        tags = request.form.get("tags")
        price = request.form.get("price")
        seats = (v.v_capacity) // ((v.v_capacity) // 50)
        new = Shows(
            s_name=show,
            s_rating=ratings,
            s_time=timings,
            s_tags=tags,
            s_price=price,
            available_seats=seats,
        )
        db.session.add(new)
        db.session.commit()
        new.venues.append(v)
        db.session.commit()
        return redirect(f"/{admin_id}/dashboard/home")
    return render_template(
        "showcreate.html",
        admin_user=a.username,
        admin_id=a.admin_id,
        venue_id=v.v_id,
        venue_name=v.v_name,
    )


# ===================================UPDATE SHOW===================================


# Admin can edit (update) a show in this page
@app.route("/<int:admin_id>/dashboard/edit/show/<int:show_id>", methods=["GET", "POST"])
def edit_show(admin_id, show_id):
    a = Admin.query.get(admin_id)
    s = Shows.query.get(show_id)
    if request.method == "POST":
        s.s_name = request.form.get("show")
        s.s_rating = request.form.get("rating")
        s.s_time = request.form.get("timings")
        s.s_tags = request.form.get("tags")
        s.s_price = request.form.get("price")
        db.session.commit()
        return redirect(f"/{admin_id}/dashboard/home")
    return render_template(
        "showupdate.html",
        admin_user=a.username,
        this_show=s.s_name,
        admin_id=a.admin_id,
        show_id=show_id,
    )


# ===================================DELETE SHOW===================================


# Admin can delete a show in this page
@app.route(
    "/<int:admin_id>/dashboard/delete/show/<int:show_id>", methods=["GET", "POST"]
)
def delete_show(admin_id, show_id):
    a = Admin.query.get(admin_id)
    s = Shows.query.get(show_id)
    db.session.delete(s)
    db.session.commit()
    return redirect(f"/{admin_id}/dashboard/home")


# ===================================USER DASHBOARD===================================


@app.route("/<int:user_id>/dashboard", methods=["GET", "POST"])
def user_home(user_id):
    u = User.query.get(user_id)
    usr = u.username
    venues = Venues.query.all()
    shows = Shows.query.all()
    return render_template(
        "userdashboard.html",
        user=usr,
        shows=shows,
        no_of_shows=Shows.query.count(),
        venues=venues,
        no_of_venues=Venues.query.count(),
        user_id=user_id,
    )


# =================================USER REGISTRATION===================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form.get("user_username")
        new_password = request.form.get("user_password")
        new_user = User(username=user_name, password=new_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("login/user")
    return render_template("userregister.html")


# ====================================BOOKING A SHOW ======================================


@app.route(
    "/<int:user_id>/book_a_show/<int:show_id>/<int:venue_id>", methods=["GET", "POST"]
)
def book(user_id, show_id, venue_id):
    u = User.query.get(user_id)
    s = Shows.query.get(show_id)
    v = Venues.query.get(venue_id)
    if request.method == "POST":
        seats = s.available_seats
        tickets = int(request.form.get("no_of_tickets"))
        if tickets > seats:
            return redirect(f"/{user_id}/book_a_show/{show_id}/{venue_id}")
        else:
            total = tickets * (s.s_price)
            new_booking = Bookings(
                tickets=tickets, total_cost=total, shows=s, venues=v, user=u
            )
            db.session.add(new_booking)
            db.session.commit()
            s.available_seats = seats - tickets
            db.session.commit()
            return redirect(f"/{user_id}/bookings")
    return render_template(
        "bookshow.html",
        user=u.username,
        show=s,
        user_id=user_id,
        show_id=s.s_id,
        venue=v,
    )


# ====================================Bookings Page =========================================
@app.route("/<int:user_id>/bookings")
def bookings(user_id):
    u = User.query.get(user_id)
    bookings = Bookings.query.filter_by(user_id=user_id).all()
    # for booking in bookings:
    #     if booking.show_id is None or booking.venue_id is None:
    #         bookings=[]
    #         break
    return render_template("bookings.html", bookings=bookings, user=u)

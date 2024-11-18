from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.database import db
from application.models import Venues, Shows
from application.validation import NotFoundError, BusinessValidationError

v_output_fields = {
    "venue_id": fields.Integer,
    "venue_name": fields.String,
    "venue_place": fields.String,
    "venue_location": fields.String,
    "Venue_capacity": fields.Integer,
}

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument("venue_name")
create_venue_parser.add_argument("venue_place")
create_venue_parser.add_argument("venue_location")
create_venue_parser.add_argument("Venue_capacity")

update_venue_parser = reqparse.RequestParser()
update_venue_parser.add_argument("venue_name")
update_venue_parser.add_argument("venue_place")
update_venue_parser.add_argument("venue_location")
update_venue_parser.add_argument("Venue_capacity")


class VenuesAPI(Resource):
    @marshal_with(v_output_fields)
    def get(self, venue_name):
        # Get the venue name

        # Get the venue from database based on venue name
        venue = db.session.query(Venues).filter(Venue.v_name == venue_name).first()
        if venue:
            return venue
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(v_output_fields)
    def put(self, venue_name):
        venue = db.session.query(Venues).filter(Venues.v_name == venue_name).first()
        if venue is None:
            raise NotFoundError(status_code=404)
        args = update_venue_parser.parse_args()
        venue_name = args.get("venue_name", None)
        venue_place = args.get("venue_place", None)
        venue_location = args.get("venue_location", None)
        Venue_capacity = args.get("venue_capacity", None)
        if venue_name is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if venue_place is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if venue_location is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if venue_capacity is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        venue = db.session.query(Venues).filter(Venues.v_name == venue_name).first()
        if venue:
            raise BusinessValidationError(
                status_code=400, error_message="Cannot delete as this venue has shows"
            )
        if venue is None:
            raise NotFoundError(status_code=404)
        venue = Venues(
            v_name=venue_name,
            v_place=venue_place,
            v_location=venue_location,
            v_capacity=venue_capacity,
        )
        db.session.add(venue)
        db.session.commit()
        return venue

    def delete(self, venue_name):
        venue = db.session.query(Venues).filter(Venues.v_name == venue_name).first()
        if venue is None:
            raise NotFoundError(status_code=404)
        shows = Shows.query.filter(Venues.query.any(v_name=venue_name)).first()
        if shows:
            raise BusinessValidationError(
                status_code=400, error_message="Cannot delete as this venue has shows"
            )
        db.session.delete(venue)
        db.session.commit()
        return "", 200

    def post(self):
        args = create_venue_parser.parse_args()
        venue_name = args.get("venue_name", None)
        venue_place = args.get("venue_place", None)
        venue_location = args.get("venue_location", None)
        Venue_capacity = args.get("venue_capacity", None)
        if venue_name is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if venue_place is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if venue_location is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if venue_capacity is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        venue = db.session.query(Venues).filter(
            (Venues.v_name == venue_name), (Venues.v_place == venue_place)
        )
        if venue:
            raise BusinessValidationError(
                status_code=401, error_message="This field is duplicated"
            )
        new_venue = Venues(
            v_name=venue_name,
            v_place=venue_place,
            v_location=venue_location,
            v_capacity=venue_capacity,
        )
        db.session.add(new_venue)
        db.session.commit()
        return "", 201


s_output_fields = {
    "show_id": fields.Integer,
    "show_name": fields.String,
    "show_rating": fields.String,
    "show_timing": fields.String,
    "show_tags": fields.String,
    "show_price": db.Integer,
    "available_seats": db.Integer,
}

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument("show_name")
create_show_parser.add_argument("show_rating")
create_show_parser.add_argument("show_timing")
create_show_parser.add_argument("show_tags")
create_show_parser.add_argument("show_price")
create_show_parser.add_argument("available_seats")

update_show_parser = reqparse.RequestParser()
update_show_parser.add_argument("show_name")
update_show_parser.add_argument("show_rating")
update_show_parser.add_argument("show_timing")
update_show_parser.add_argument("show_tags")
update_show_parser.add_argument("show_price")
update_show_parser.add_argument("available_seats")


class ShowsAPI(Resource):
    @marshal_with(s_output_fields)
    def get(self, show_name):
        show = db.session.query(Shows).filter(Shows.s_name == show_name).first()
        if show:
            return show
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(s_output_fields)
    def put(self, show_name):
        show = db.session.query(Shows).filter(Shows.s_name == show_name).first()
        if show is None:
            raise NotFoundError(status_code=404)
        args = update_venue_parser.parse_args()
        show_name = args.get("show_name", None)
        show_rating = args.get("show_rating", None)
        show_timing = args.get("show_timing", None)
        show_tags = args.get("show_tags", None)
        show_price = args.get("show_price", None)
        if show_name is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if show_timing is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if show_tags is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if show_price is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        show = db.session.query(Shows).filter(Shows.s_name == show_name).first()
        if show is None:
            raise NotFoundError(status_code=404)
        show = Shows(
            s_name=show_name,
            s_rating=show_rating,
            s_time=show_timing,
            s_tags=show_tags,
            s_price=show_price,
        )
        db.session.add(show)
        db.session.commit()
        return show

    def delete(self, show_name):
        show = db.session.query(Shows).filter(Shows.s_name == show_name).first()
        if show is None:
            raise NotFoundError(status_code=404)
        venues = Venues.query.filter(Shows.query.any(s_name=show_name)).first()
        if venues:
            raise BusinessValidationError(
                status_code=400, error_message="Cannot delete as this venue has shows"
            )
        db.session.delete(show)
        db.session.commit()
        return "", 200

    def post(self):
        args = create_show_parser.parse_args()
        show_name = args.get("show_name", None)
        show_rating = args.get("show_rating", None)
        show_timing = args.get("show_timing", None)
        show_tags = args.get("show_tags", None)
        show_price = args.get("show_price", None)
        if show_name is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if show_timing is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if show_tags is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        if show_price is None:
            raise BusinessValidationError(
                status_code=400, error_message="This field is required"
            )
        new_show = Shows(
            s_name=show_name,
            s_rating=show_rating,
            s_time=show_timing,
            s_tags=show_tags,
            s_price=show_price,
        )
        db.session.add(new_show)
        db.session.commit()
        return "", 201

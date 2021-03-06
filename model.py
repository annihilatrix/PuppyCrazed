"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy as sqla


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = sqla()


##############################################################################
# Model definitions

class User(db.Model):
    """User of PuppyCrazed"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_fname = db.Column(db.String(63), nullable=True)
    user_lname = db.Column(db.String(64), nullable=True)
    user_email = db.Column(db.String(64), nullable=True, unique=True)
    user_password = db.Column(db.String(64), nullable=True)
    user_gender = db.Column(db.String(64), nullable=True)
    user_preferred_gender = db.Column(db.String(64), nullable=True)
    pet_img = db.Column(db.String(255), nullable=True)
    pet_name = db.Column(db.String(64), nullable=True)
    pet_name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        """Displays useful info about the Parent object."""
        return ("<User user_id:{} user_fname:{}, user_lname:{}," +
                " pet_img:{}").format(self.user_id,
                                      self.user_fname,
                                      self.user_lname,
                                      self.pet_img)

    def matches(self):
        """given a user, returns the corresponding user objects that are matches."""
        potential_matches = db.session.query(User).join(View).filter(View.viewed_id == self.user_id).filter(View.like == True).all()
        matches = []
        for match in potential_matches:
            # determine if the liked user has also liked self.user_id
            if self.has_liked(match.user_id):
                pair = db.session.query(User).filter(User.user_id == match.user_id).first()
                matches.append(pair)
        return matches



    def has_liked(self, user_id):
        """Has the user object liked the user_id supplied in the input"""
        view = db.session.query(View).filter(View.viewer_id == self.user_id).filter(View.viewed_id == user_id).filter(View.like == True).first()
        return view is not None


class View(db.Model):
    """Table storing who has viewed whom and whether they liked them or not."""

    __tablename__ = "views"

    view_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    viewer_id = db.Column(db.Integer,
                          db.ForeignKey("users.user_id"),
                          nullable=False)
    viewed_id = db.Column(db.Integer,
                          nullable=False)
    like = db.Column(db.Boolean, nullable=False)

    viewer = db.relationship("User", foreign_keys=[viewer_id])

    def __repr__(self):
        """Displays view info"""
        return "<View view_id:{}>".format(self.view_id)




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///puppycrazed'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from PuppyCrazed import app
    connect_to_db(app)

    print "Connected to DB."

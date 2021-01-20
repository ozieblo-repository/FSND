#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (Flask,
                   render_template,
                   request,
                   Response,
                   flash,
                   redirect,
                   url_for,
                   abort)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import (Formatter,
                     FileHandler)
from flask_wtf import Form
from forms import (ShowForm,
                   VenueForm,
                   ArtistForm)
from flask_migrate import Migrate

import regex as re
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

# Initial population of the Genre table here --> No, for grading they want it to be blank
# (just the schema is defined) and we count on the web form validators to only show valid choices (forms.py)

# Association tables for Artist to Genre (many2many) and Venue to Genre (many2many)
# DEFINE the Genre table as the child since it normally doesn't matter which we pick, but in this case,
# its common to both many2many relationships and we have to constrain the parents to just one backref!
artist_genre_table = db.Table('artist_genre_table',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
)

venue_genre_table = db.Table('venue_genre_table',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # Here we link the associative table for the m2m relationship with genre
    genres = db.relationship('Genre', secondary=venue_genre_table, backref=db.backref('venues'))
    # secondary links this to the associative (m2m) table name
    # can refences like venue.genres with the above statement
    # backref creates an attribute on Venue objects so we can also reference like: genre.venues

    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    # Venue is the parent (one-to-many) of a Show (Artist is also a foreign key, in def. of Show)
    # In the parent is where we put the db.relationship in SQLAlchemy
    shows = db.relationship('Show', backref='venue', lazy=True)    # Can reference show.venue (as well as venue.shows)

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # Genre should be its own table, with a many2many relationship with Artist
    # and another many2many relationship with Venue
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # Here we link the associative table for the m2m relationship with genre
    genres = db.relationship('Genre', secondary=artist_genre_table, backref=db.backref('artists'))
    # secondary links this to the associative (m2m) table name
    # can refences like artist.genres with the above statement
    # backref creates an attribute on Artist objects so we can also reference like: genre.artists

    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    # Artist is the parent (one-to-many) of a Show (Venue is also a foreign key, in def. of Show)
    # In the parent is where we put the db.relationship in SQLAlchemy
    shows = db.relationship('Show', backref='artist', lazy=True)    # Can reference show.artist (as well as artist.shows)

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    # Start time required field

    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)   # Foreign key is the tablename.pk
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
        return f'<Show {self.id} {self.start_time} artist_id={artist_id} venue_id={venue_id}>'

#db.create_all()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')

  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

def venues():
    areas = db.session.query(Venue.city,
                             Venue.state).distinct(Venue.city,
                                                   Venue.state).order_by('state').all()
    data = []

    for area in areas:
        venues = Venue.query.filter_by(state=area.state).filter_by(city=area.city).order_by('name').all()
        venue_data = []
        data.append({'city': area.city,
                     'state': area.state,
                     'venues': venue_data})

        for venue in venues:
            shows = Show.query.filter_by(venue_id=venue.id).order_by('id').all()
            venue_data.append({'id': venue.id,
                               'name': venue.name,
                               'num_upcoming_shows': len(shows)})

    return render_template('pages/venues.html',
                           areas=data)



@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get('search_term', '')

  result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  count = len(result)
  response = {"count": count,
              "data": result}

  return render_template('pages/search_venues.html',
                         results=response,
                         search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter(Venue.id == venue_id).first()

  past = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
      Show.start_time < datetime.now()).join(Artist,
                                             Show.artist_id == Artist.id).add_columns(Artist.id,
                                                                                      Artist.name,
                                                                                      Artist.image_link,
                                                                                      Show.start_time).all()

  upcoming = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
      Show.start_time > datetime.now()).join(Artist,
                                             Show.artist_id == Artist.id).add_columns(Artist.id,
                                                                                      Artist.name,
                                                                                      Artist.image_link,
                                                                                      Show.start_time).all()

  upcoming_shows = []
  past_shows = []

  for i in upcoming:
      upcoming_shows.append({'artist_id': i[1],
                             'artist_name': i[2],
                             'image_link': i[3],
                             'start_time': str(i[4])})

  for i in past:
      past_shows.append({'artist_id': i[1],
                         'artist_name': i[2],
                         'image_link': i[3],
                         'start_time': str(i[4])})

  if venue is None:
      abort(404)

  response = {"id": venue.id,
              "name": venue.name,
              "genres": [venue.genres],
              "address": venue.address,
              "city": venue.city,
              "state": venue.state,
              "phone": venue.phone,
              "website": venue.website,
              "facebook_link": venue.facebook_link,
              "seeking_talent": venue.seeking_talent,
              "seeking_description": venue.seeking_description,
              "image_link": venue.image_link,
              "past_shows": past_shows,
              "upcoming_shows": upcoming_shows,
              "past_shows_count": len(past),
              "upcoming_shows_count": len(upcoming)}

  return render_template('pages/show_venue.html',
                         venue=response)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # TODO: on unsuccessful db insert, flash an error instead.

    try:
        venue = Venue(name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            website=request.form['website'],
            seeking_talent=json.loads(request.form['seeking_talent'].lower()),
            seeking_description=request.form['seeking_description'])
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully added!')
    except Exception as e:
        print(e)
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be added')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  try:
      Venue.query.filter(Venue.id == venue_id).delete()
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  response = Artist.query.all()

  return render_template('pages/artists.html',
                         rtists=response)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')

  result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()

  count = len(result)

  response = {"count": count,
              "data": result}

  return render_template('pages/search_artists.html',
                         results=response,
                         search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  artist = Artist.query.filter(Artist.id == artist_id).first()

  past = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
      Show.start_time < datetime.now()).join(Venue,
                                             Show.venue_id == Venue.id).add_columns(Venue.id,
                                                                                    Venue.name,
                                                                                    Venue.image_link,
                                                                                    Show.start_time).all()

  upcoming = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
      Show.start_time > datetime.now()).join(Venue,
                                             Show.venue_id == Venue.id).add_columns(Venue.id,
                                                                                    Venue.name,
                                                                                    Venue.image_link,
                                                                                    Show.start_time).all()

  upcoming_shows = []

  past_shows = []

  for i in upcoming:
      upcoming_shows.append({'venue_id': i[1],
                             'venue_name': i[2],
                             'image_link': i[3],
                             'start_time': str(i[4])})

  for i in past:
      past_shows.append({'venue_id': i[1],
                         'venue_name': i[2],
                         'image_link': i[3],
                         'start_time': str(i[4])})

  if artist is None:
      abort(404)

  response = {"id": artist.id,
              "name": artist.name,
              "genres": [artist.genres],
              "city": artist.city,
              "state": artist.state,
              "phone": artist.phone,
              "website": artist.website,
              "facebook_link": artist.facebook_link,
              "seeking_venue": artist.seeking_venue,
              "seeking_description": artist.seeking_description,
              "image_link": artist.image_link,
              "past_shows": past_shows,
              "upcoming_shows": upcoming_shows,
              "past_shows_count": len(past),
              "upcoming_shows_count": len(upcoming)}

  return render_template('pages/show_artist.html',
                         artist=response)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    # TODO: populate form with fields from artist with ID <artist_id>

    artist = Artist.query.get(artist_id)

    if not artist:
        return redirect(url_for('index'))
    else:
        form = ArtistForm(obj=artist)

    genres = [genre.name for genre in artist.genres]

    artist = {"id": artist_id,
              "name": artist.name,
              "genres": genres,
              "city": artist.city,
              "state": artist.state,
              "phone": (artist.phone[:3] + '-' + artist.phone[3:6] + '-' + artist.phone[6:]),
              "website": artist.website,
              "facebook_link": artist.facebook_link,
              "seeking_venue": artist.seeking_venue,
              "seeking_description": artist.seeking_description,
              "image_link": artist.image_link}

    return render_template('forms/edit_artist.html',
                           form=form,
                           artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing

  form = ArtistForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  phone = form.phone.data
  phone = re.sub('\D', '', phone)
  genres = form.genres.data
  seeking_venue = True if form.seeking_venue.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  website = form.website.data.strip()
  facebook_link = form.facebook_link.data.strip()

  if not form.validate():
      flash(form.errors)
      return redirect(url_for('edit_artist_submission',
                              artist_id=artist_id))
  else:
      error_in_update = False

      try:
          artist = Artist.query.get(artist_id)

          artist.name = name
          artist.city = city
          artist.state = state
          artist.phone = phone
          artist.seeking_venue = seeking_venue
          artist.seeking_description = seeking_description
          artist.image_link = image_link
          artist.website = website
          artist.facebook_link = facebook_link

          artist.genres.clear()

          for genre in genres:
              fetch_genre = Genre.query.filter_by(name=genre).one_or_none()
              if fetch_genre:
                  artist.genres.append(fetch_genre)
              else:
                  new_genre = Genre(name=genre)
                  db.session.add(new_genre)
                  artist.genres.append(new_genre)

          db.session.commit()

      except Exception as e:
          error_in_update = True
          print(f'Exception "{e}" in edit_artist_submission()')
          db.session.rollback()

      finally:
          db.session.close()

      if not error_in_update:
          flash('Artist ' + request.form['name'] + ' was successfully updated!')
          return redirect(url_for('show_artist',
                                  artist_id=artist_id))
      else:
          flash('An error occurred. Artist ' + name + ' could not be updated.')
          print("Error in edit_artist_submission()")
          abort(500)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  # TODO: populate form with values from venue with ID <venue_id>

  venue = Venue.query.get(venue_id)

  if not venue:
      return redirect(url_for('index'))
  else:
      form = VenueForm(obj=venue)

  genres = [genre.name for genre in venue.genres]

  venue = {"id": venue_id,
           "name": venue.name,
           "genres": genres,
           "address": venue.address,
           "city": venue.city,
           "state": venue.state,
           "phone": (venue.phone[:3] + '-' + venue.phone[3:6] + '-' + venue.phone[6:]),
           "website": venue.website,
           "facebook_link": venue.facebook_link,
           "seeking_talent": venue.seeking_talent,
           "seeking_description": venue.seeking_description,
           "image_link": venue.image_link}

  return render_template('forms/edit_venue.html',
                         form=form,
                         venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing

  form = VenueForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  address = form.address.data.strip()
  phone = form.phone.data
  phone = re.sub('\D', '', phone)
  genres = form.genres.data
  seeking_talent = True if form.seeking_talent.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  website = form.website.data.strip()
  facebook_link = form.facebook_link.data.strip()

  if not form.validate():
      flash(form.errors)
      return redirect(url_for('edit_venue_submission',
                              venue_id=venue_id))
  else:
      error_in_update = False

      try:
          venue = Venue.query.get(venue_id)

          venue.name = name
          venue.city = city
          venue.state = state
          venue.address = address
          venue.phone = phone
          venue.seeking_talent = seeking_talent
          venue.seeking_description = seeking_description
          venue.image_link = image_link
          venue.website = website
          venue.facebook_link = facebook_link

          venue.genres.clear()

          for genre in genres:
              fetch_genre = Genre.query.filter_by(name=genre).one_or_none()

              if fetch_genre:
                  venue.genres.append(fetch_genre)
              else:
                  new_genre = Genre(name=genre)
                  db.session.add(new_genre)
                  venue.genres.append(new_genre)

          db.session.commit()

      except Exception as e:
          error_in_update = True
          print(f'Exception "{e}" in edit_venue_submission()')
          db.session.rollback()

      finally:
          db.session.close()

      if not error_in_update:
          flash('Venue ' + request.form['name'] + ' was successfully updated!')
          return redirect(url_for('show_venue',
                                  venue_id=venue_id))
      else:
          flash('An error occurred. Venue ' + name + ' could not be updated.')
          print("Error in edit_venue_submission()")
          abort(500)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

  form = ArtistForm()

  # import pdb; pdb.set_trace()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  phone = form.phone.data
  phone = re.sub('\D', '', phone)
  genres = form.genres.data
  seeking_venue = True if form.seeking_venue.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()
  website = form.website.data.strip()
  facebook_link = form.facebook_link.data.strip()

  if not form.validate():
      flash(form.errors)
      return redirect(url_for('create_artist_submission'))

  else:
      error_in_insert = False

      try:
          new_artist = Artist(name=name,
                              city=city,
                              state=state,
                              phone=phone,
                              seeking_venue=seeking_venue,
                              seeking_description=seeking_description,
                              image_link=image_link,
                              website=website,
                              facebook_link=facebook_link)

          for genre in genres:
              fetch_genre = Genre.query.filter_by(name=genre).one_or_none()
              if fetch_genre:
                  new_artist.genres.append(fetch_genre)
              else:
                  new_genre = Genre(name=genre)
                  db.session.add(new_genre)
                  new_artist.genres.append(new_genre)

          db.session.add(new_artist)
          db.session.commit()

      except Exception as e:
          error_in_insert = True
          print(f'Exception "{e}" in create_artist_submission()')
          db.session.rollback()

      finally:
          db.session.close()

      if not error_in_insert:
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
          return redirect(url_for('index'))

      else:
          flash('An error occurred. Artist ' + name + ' could not be listed.')
          print("Error in create_artist_submission()")
          abort(500)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  shows = Show.query.all()

  for show in shows:
      data.append({"venue_id": show.venue.id,
                   "venue_name": show.venue.name,
                   "artist_id": show.artist.id,
                   "artist_name": show.artist.name,
                   "artist_image_link": show.artist.image_link,
                   "start_time": format_datetime(str(show.start_time))})

  return render_template('pages/shows.html',
                         shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead


  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  form = ShowForm()

  artist_id = form.artist_id.data.strip()
  venue_id = form.venue_id.data.strip()
  start_time = form.start_time.data

  error_in_insert = False

  try:
      new_show = Show(start_time=start_time,
                      artist_id=artist_id,
                      venue_id=venue_id)
      db.session.add(new_show)
      db.session.commit()

  except:
      error_in_insert = True
      print(f'Exception "{e}" in create_show_submission()')
      db.session.rollback()

  finally:
      db.session.close()

  if error_in_insert:
      flash(f'An error occurred.  Show could not be listed.')
      print("Error in create_show_submission()")

  else:
      flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

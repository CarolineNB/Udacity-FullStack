#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import distinct
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
  
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODONE: connect to a local postgresql database

#----------------------------------------------------------------------------#
  # Models.
#----------------------------------------------------------------------------#

# shows = db.Table('venue_listing',
#   db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
#   db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
#   db.Column('upcoming', db.Boolean),
#   db.Column('start_time', db.String())
# )


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    showings = db.relationship('Shows', backref='Venue', lazy='dynamic')

    # TODONE: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    showings = db.relationship('Shows', backref='Artist', lazy='dynamic')

    # TODONE: implement any missing fields, as a database migration using Flask-Migrate


class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    start_time = db.Column(db.DateTime, nullable=False)

# TODONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
def venues():
  # TODONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #data = db.session.query(Venue).join(Shows)
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  cur = ''
  data = []
  for venue in venues:
    if venue.city + venue.state == cur:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": venue.showings.filter(Shows.start_time > now).count()
      })
    else:
      cur = venue.city + venue.state
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": venue.showings.filter(Shows.start_time > now).count()
        }]
      })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  results = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  # print(like_venue)
  response={
    "count": results.count(),
    "data": results.all()
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODONE: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": venue.showings.filter(Shows.start_time < now).all(),
    "upcoming_shows": venue.showings.filter(Shows.start_time > now).all(),
    "past_shows_count": venue.showings.filter(Shows.start_time < now).count(),
    "upcoming_shows_count": venue.showings.filter(Shows.start_time > now).count(),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODONE: insert form data as a new Venue record in the db, instead
  # TODONE: modify data to be the data object returned from db insertion
  error = False
  try:
    name = request.form['name']
    genres = request.form['genres']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    facebook_link = request.form['facebook_link']

    ''' 
    website = request.form['website']
    seeking_venue = request.form['seeking_venue']
    seeking_description = request.form['seeking_description']
    image_link = request.form['image_link']
    '''
    
    venue = Venue(name=name, genres=genres, city=city, state=state, address=address, 
    phone=phone, facebook_link=facebook_link)

    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info()) 
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    # TODONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error has occurred. The Venue ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODONE: replace with real data returned from querying the database
  data = []
  artists = Artist.query.all()
  for i in artists:
    data.append({
      "id": i.id,
      "name": i.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  results = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
  response={
    "count": results.count(),
    "data": results.all()
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODONE: replace with real venue data from the venues table, using venue_id
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  artist = Artist.query.filter_by(id=artist_id).first()
  data ={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":artist.showings.filter(Shows.start_time < now).all(),
    "upcoming_shows": artist.showings.filter(Shows.start_time > now).all(),
    "past_shows_count": artist.showings.filter(Shows.start_time < now).count(),
    "upcoming_shows_count": artist.showings.filter(Shows.start_time > now).count(),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  this = Artist.query.filter_by(id=artist_id).first()
  artist={
    "id": artist_id,
    "name": this.name,
    "genres": this.genres,
    "address": this.address,
    "city": this.city,
    "state": this.state,
    "phone": this.phone,
    "website": this.website,
    "facebook_link": this.facebook_link,
    "seeking_venue": this.seeking_venue,
    "seeking_description": this.seeking_description,
    "image_link": this.image_link
  }
  form.name.data = artist["name"]
  form.genres.data = artist["genres"]
  form.city.data = artist["city"]
  form.state.data = artist["state"]
  form.phone.data = artist["phone"]
  form.facebook_link.data = artist["facebook_link"]
  form.image_link.data = artist["image_link"]
  
  #form.website.data = artist["website"]
  #form.seeking_venue.data = artist["seeking_venue"]
  #form.seeking_description.data = artist["seeking_description"]

  # TODONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODONE: take values from the form submitted, and update existing
  error = False
  try:
    form = ArtistForm(request.form)
    past_version = Artist.query.get(artist_id)
    db.session.delete(past_version)

    name = request.form['name']
    genres = request.form['genres']
    city = request.form['city']
    state =  request.form['state']
    phone = request.form['phone']
    facebook_link = request.form['facebook_link']
    
    #"website": request.form['website'],
    #"seeking_venue": request.form['seeking_venue'],
    #"seeking_description": request.form['seeking_description'],
    #"image_link": request.form['image_link']

    artist = Artist(id=artist_id, name=name, genres=genres, city=city, state=state, phone=phone, 
      facebook_link=facebook_link)

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info()) 
    db.session.rollback()
  finally:
    db.session.close
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  else:
    flash('An error has occurred. The Artist ' + request.form['name'] + ' could not be updated.')
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  this = Venue.query.get(venue_id)
  venue={
    "id": venue_id,
    "name": this.name,
    "genres": this.genres,
    "address": this.address,
    "city": this.city,
    "state": this.state,
    "phone": this.phone,
    "website": this.website,
    "facebook_link": this.facebook_link,
    # "seeking_talent": True,
    # "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": this.image_link
  }
  form.name.data = venue["name"]
  form.address.data = venue["address"]
  form.genres.data = venue["genres"]
  form.city.data = venue["city"]
  form.state.data = venue["state"]
  form.phone.data = venue["phone"]
  form.facebook_link.data = venue["facebook_link"]
  #form.website.data= venue["website"]
  # TODONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    form = VenueForm(request.form)
    past_version = Venue.query.get(venue_id)
    db.session.delete(past_version)

    name = request.form['name']
    city = request.form['city']
    state =  request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form['genres']
    facebook_link = request.form['facebook_link']
    
    #"website": request.form['website'],
    #"seeking_venue": request.form['seeking_venue'],
    #"seeking_description": request.form['seeking_description'],
    #"image_link": request.form['image_link']

    venue = Venue(id=venue_id, name=name, genres=genres, address=address, city=city, state=state, phone=phone, 
      facebook_link=facebook_link)

    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info()) 
    db.session.rollback()
  finally:
    db.session.close
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
    flash('An error has occurred. The Venue ' + request.form['name'] + ' could not be updated.')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODONE: insert form data as a new Venue record in the db, instead
  # TODONE: modify data to be the data object returned from db insertion
  error = False
  try:
    name = request.form['name']
    genres = request.form['genres']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    facebook_link = request.form['facebook_link']
   
    ''' 
    website = request.form['website']
    seeking_venue = request.form['seeking_venue']
    seeking_description = request.form['seeking_description']
    image_link = request.form['image_link']
    '''
    artist = Artist(name=name, genres=genres, city=city, state=state, phone=phone, 
      facebook_link=facebook_link)

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info()) 
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    # TODONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error has occurred. The Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #shows = Shows.query.all()
  shows = Shows.query.all()
  

  # for i in shows:
  #   data.append({
  #     "venue_id": i.venue_id,
  #     "venue_name": Venue.query.filter_by(id=i.venue_id).one().name,
  #     "artist_id": i.artist_id,
  #     "artist_name": Artist.query.filter_by(id=i.artist_id).one().name,
  #     "artist_image_link": i.artist_image_link,
  #     "start_time": i.start_time
  #   })
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODONE: insert form data as a new Show record in the db, instead
  error = False
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except:
    error=True
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    # TODONE: on successful db insert, flash success
    flash('Show was successfully listed!')
  else:
    # TODONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error has occurred. The show could not be listed.')
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

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

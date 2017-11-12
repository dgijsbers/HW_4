## SI 364 - Fall 2017
## HW 4 - Demery Gijsbers

## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecure'
## TODO SI364: Create a database in postgresql in the code line below, and 
#fill in your app's database URI. It should be of the format: 


## Your Postgres database should be your uniqname, plus HW4, e.g.
# "jczettaHW4" or "maupandeHW4"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/demgijsHW4"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
manager = Manager(app)
db = SQLAlchemy(app) # For database use

## Set up Shell context so it's easy to use the shell to debug
## TODO SI364: Add your models to 
    #this shell context function so you can use them in the shell
    # TODO SI364: Submit a screenshot of yourself using the shell 
    #to make a query for all the Tweets in the database.
    # Filling this in will make that easier!
def make_shell_context():
    return dict(app=app, db=db, Tweet=Tweet, User=User, Hashtag=Hashtag) 

# Add function use to manager
manager.add_command("shell", Shell(make_context=make_shell_context))


#########
######### Everything above this line is important/useful setup, not 
#problem-solving.
#########

##### Set up Models #####

## TODO SI364: Set up the following Model classes, with the respective 
#fields (data types).

## The following relationships should exist between them:
# Tweet:User - Many:One
# Tweet:Hashtag - Many:Many
Tweet_Hashtag = db.Table('Tweet_Hashtag', db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id')),db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id')))

# - Tweet
## -- id (Primary Key)
## -- text (String, up to 285 chars)
## -- user_id (Integer, ID of user posted)
class Tweet(db.Model):
    __tablename__ = "tweet"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(285))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    hashtags = db.relationship('Hashtag', secondary = Tweet_Hashtag, backref=db.backref('tweet', lazy='dynamic'), lazy='dynamic')
# - User
## -- id (Primary Key)
## -- twitter_username (String, up to 64 chars) (Unique=True)
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    twitter_username = db.Column(db.String(64), unique=True)
    tweets = db.relationship('Tweet', backref="User")

# - Hashtag
## -- id (Primary Key)
## -- text (Unique=True)
class Hashtag(db.Model):
    __tablename__ = "hashtag"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True)

# Association Table: Tweet_Hashtag
# -- tweet_id
# -- hashtag_id


## NOTE: You'll have to set up database relationship 
#code in either the Tweet table or the Hashtag table so that
# the association table for that many-many relationship will 
#work properly!


##### Set up Forms #####

# TODO SI364: Fill in the rest of this Form class so that someone 
#running this web app will be able to fill in information about tweets 
#they wish existed to save in the database:

## -- tweet text
## -- the twitter username who should post it
## -- a list of comma-separated hashtags it should have

### For database additions / get_or_create functions

## TODO SI364: Write get_or_create functions for each model -- 
#Tweets, Hashtags, and Users.
## -- Tweets should be identified by their text and user id,(e.g. if 
    #there's already a tweet with that text, by that user, then return it; 
    #otherwise, create it)
## -- Users should be identified by their username (e.g. if there's already 
    #a user with that username, return it, otherwise; create it)
## -- Hashtags should be identified by their text (e.g. if there's already 
    #a hashtag with that text, return it; otherwise, create it)

## HINT: Your get_or_create_tweet function should invoke your 
#get_or_create_user function AND your get_or_create_hashtag function. 
#You'll have seen an example similar to this in class!


## NOTE: If you choose to organize your code differently so it has the 
#same effect of not encounting duplicates / identity errors, that is OK. 
#But writing separate functions that may invoke one another is our primary
# suggestion.

class TweetForm(FlaskForm):
    username = StringField("Enter your Twitter username handle:", validators=[Required()])
    text = StringField("Enter the text of a tweet:", validators=[Required()])
    hashtag = StringField("Enter a hashtag by using '#' if you want:")
    submit = SubmitField('Submit')

def get_or_create_user(db_session, user_name, tweet_text):
    username = db.session.query(User).filter_by(twitter_username = user_name).first()
    if username:
        return username
    else:
        username = User(twitter_username = user_name, text = tweet_text)
        db_session.add(username)
        db_session.commit()
        return username

def get_or_create_tweet(db_session, tweet_text, user_id, hash_tag):
    text = db.session.query(Tweet).filter_by(user_id = user_id).first()
    if text:
        return text
    else:
        text = Tweet(text = tweet_text, twitter_username = user_name, hashtags = hash_tag)
        db_session.add(text)
        db_session.commit()
        return text

def get_or_create_hashtag(db_session, text):
    hashtags = db.session.query(Hashtag).filter_by(text = text).first()
    if hashtags:
        return hashtags 
    else:
        hashtags = Hashtag(text = text)
        db_session.add(hashtags)
        db_session.commit()
        return hashtags

##### Helper functions


##### Set up Controllers (view functions) #####

## Error handling routes - PROVIDED
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

## Main route

@app.route('/', methods=['GET', 'POST'])
def index():
    tweeter = Tweet.query.all()
    num_tweets = len(tweeter)
    form = TweetForm()
    if form.validate_on_submit():
        if db.session.query(Tweet).filter_by(text = form.text.data).first():
            flash("You've already saved a tweet like that!")
        get_or_create_tweet(db.session, form.text.data, form.username.data, form.hashtag.data)
        return redirect(url_for('see_all_tweets'))
    return render_template('index.html', form=form, num_tweets=num_tweets)
    ## TODO SI364: Fill in the index route as described.
    # A template index.html has been created and provided to render 
    #what this route needs to show -- YOU just need to fill in this 
    #view function so it will work.
    ## HINT: Check out the index.html template to make sure you're 
    #sending it the data it needs.


    # The index route should:
    # - Show the Tweet form.
    # - If you enter a tweet with identical text and username to an 
    #existing tweet, it should redirect you to the list of all the 
    #tweets and a message that you've already saved a tweet like that.

    ## ^ HINT: Invoke your get_or_create_tweet function
    ## ^ HINT: Check out the get_flashed_messages setup in the songs app 
    #you saw in class

    # This  main page should ALSO show links to pages in the app (see 
        #routes below) that:
    # -- allow you to see all of the tweets posted
    # -- see all of the twitter users you've saved tweets for, along 
    #with how many tweets they have in your database

    #Discussion section 8 practice problems will help 

@app.route('/all_tweets')
def see_all_tweets():
    all_tweets = []
    tweeter = Tweet.query.all()
    for t in tweeter:
        tweet = Tweet.query.filter_by(tweet_text = t.text).first()
        all_tweets.append((t.tweet_text, t.user_name, t.hash_tag))
    return render_template('all_tweets.html', all_tweets = all_tweets)

    # TODO SI364: Fill in this view function so that it can successfully 
    #render the template all_tweets.html, which is provided.
    ## HINT: Check out the all_songs and all_artists routes in the songs
    # app you saw in class.


@app.route('/all_users')
def see_all_users():
    all_users = []
    users = User.query.all()
    for u in users:
        all_users.append(u.tweet_text, u.user_name)
    return render_template('all_users.html')
    # TODO SI364: Fill in this view function so it can successfully 
    #render the template all_users.html, which is provided. (See 
        #instructions for more detail.)
    ## HINT: Check out the all_songs and all_artists routes in the songs 
    #app you saw in class.


if __name__ == '__main__':
    db.create_all()
    manager.run() # Run with this: python main_app.py runserver
    # Also provides more tools for debugging





# SI 364 - Fall 2017 - Homework 4

### DEADLINE: Sunday, November 12, at 11:59 PM

## To Submit

* Fork and clone this repository
* Edit files per instructions and push your changes to your GitHub fork
* Submit the link to your GitHub repository to the assignment on Canvas
* Submit a screenshot of making a query in the shell, as described below

## Instructions

In this HW, you'll be writing an application that's *kind of like* Twitter for one person: you'll be saving data about tweets, but instead of getting tweets by different users on `twitter.com`, you'll be using a form to gather data from a user about tweets they would *like to see posted*, for example -- and saving that data in a database.

We've provided templates, and instructions in the `SI364_hw4.py` file. Your task(s) are to fill in code as directed in that file. Everywhere you'll need to write code, you'll find a comment `TODO SI364`. Filling in code correctly in each of those spaces will allow you to complete this application so that it works!

Additionally, you'll need to add your models to the `make_shell_context` function in the application, and use the shell to make a query for all the tweets in your database. To show that you've practiced using the shell, and that your additions to the `make_shell_context` function work (it's just a tiny bit of code to add!), you should also **submit a screenshot of your using the Flask shell in your command prompt to query for all the Tweets in the tweets table of your database.**

You'll see examples of applications and database relationships in class (section and lecture) that will be examples similar to what you're doing here.

### Sequence of steps to complete

0. Set up your Postgres database as specified, and put the DATABASE_URI into the `app.config` dictionary
1. Define your model classes
2. Define your form class(es)
3. Check out the provided templates for an idea of what data needs to be sent from different routes
4. Make comments inside the unfinished view functions that remind you what you have to do
5. Define your `get_or_create` functions -- first `get_or_create_user`, then `get_or_create_hashtag`, then `get_or_create_tweet`, which should invoke each of the other two functions.
6. Bit by bit, running intermittently to debug, try completing the `index` view function so you can see results. e.g. displaying the form first, then managing the data from the form...
7. Complete the `all_tweets` and `all_users` view functions (as always, referencing the templates for ideas of what data you need to send)
8. Finish the `make_shell_context` function by adding your models, and test it out, and take a screenshot as specified.
9. Test out the app -- make sure it runs! You're all set!

### Important Note about your database

It's important that you make your PostgreSQL database for this HW assignment your uniqname, with HW4. For example, Jackie's would be `jczettaHW4`. Mauli's would be `maupandeHW4`. So your database URI in the `app.config` should look something like this (except replace my uniqname with yours!): `postgresql://localhost/jczettaHW4`

This will allow us to grade each of your projects without incurring conflicts between different students' databases!

## Files Included

* `templates` directory:

    * `all_tweets.html`
    * `all_users.html`
    * `index.html`

* `README.md` (this file, with instructions)
* `SI364_hw4.py` (the main Python file for the application)

You may add additional files or additional features/routes if you wish, but that is not required. It is required, in order to get full credit, that the TODOs as listed be completed and function. *We will not grade code that does not run, so make sure your application does run! Check with an instructor if you are having troubles with this.*

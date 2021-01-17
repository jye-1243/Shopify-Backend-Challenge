# Shopify-Backend-Challenge

Shopify Summer 2021 Internship Backend Challenge

This web app is for a basic image repository in which users can view and search through a gallery of photos. Additionally, users can log into or register for the web app, which allows them to add and delete their own photos.

### Demo Screenshots
The main gallery view can be seen here:
![main gallery](https://github.com/jye-1243/Shopify-Backend-Challenge/blob/master/static/screenshots/gallery.PNG)

Other screenshots viewable [here](https://github.com/jye-1243/Shopify-Backend-Challenge/tree/master/static/screenshots)

## Getting Started

### Prerequisites
This project was built using Python3, which can be installed [here](https://www.python.org/downloads/). Once Python is installed, also install the [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/) and [flask-session](https://flask-session.readthedocs.io/en/latest/) libraries for use.
This project also requires SQLite, which can be installed pursuant to these [instructions](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm)

### Installation and Deployment
1. Clone this [github repository](https://github.com/jye-1243/Shopify-Backend-Challenge)
2. Navigate to your local folder for the repository
3. Run `python main.py` in the aforementioned directory
4. The web app should open in [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage
When the user first loads the web app, they can see a gallery of the images uploaded by all users. This gallery also has a search function, which allows users to search the database for photos by filename. From there, users can use the Navbar to either log in (if they already have an account) or register as a user in the database. 

Once the user is signed in, they can navigate to various pages via the Navbar. First, they may choose to view a gallery of their photos from the "My Images" tab. They may also elect to add new photos to the repository from the Add page. This is done by clicking on the file upload area and pressing submit. Finally, users may remove photos that they had previously uploaded from the Delete page. Here, the user is presented with a gallery of their own photos from which they may choose a set to delete. However, users cannot remove the images of other users. Finally, the user may log out using the Logout button in the Navbar.

### Known Bugs
At times, users may need to refresh a page using Ctrl-Shift-R, as some files upload into the cache and the site does not update accordingly.

Also, in cases where users use particularly weak passwords (eg. '123'), browsers such as Chrome deliver a warning alert asking for passwords to be changed.

## Built With
This project was built with:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
- [Bootstrap Navbar](https://getbootstrap.com/docs/4.0/components/navbar/) - Bootstrap components
- [SQLite](https://www.sqlite.org/index.html) - Database

## Acknowledgements
Portions of the code in this challenge were inspired by or used in:
- [CS50 Coursework](https://cs50.harvard.edu/x/2020/tracks/web/finance/)
- [Osvaldas Valutis](https://tympanus.net/codrops/2015/09/15/styling-customizing-file-inputs-smart-way/) and his form input styling

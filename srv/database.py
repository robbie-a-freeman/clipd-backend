import psycopg2
import sys

# instance that contains the necessary info for a database reference
class DB:
    URL = 'error'
    SSL = 'require'
    # instantiate db with url and sslmode
    def __init__(self, db_url, ssl):
        self.URL = db_url
        self.SSL = ssl
    
    # get all videos in the db
    def getAllVideos(self):
        conn = psycopg2.connect(self.URL, sslmode=self.SSL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM videos")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    # get the user by id, used for auth
    def getUserById(self, id):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT * FROM Users WHERE Id = %s;', (id, ))
            data = cur.fetchone()
            cur.close()
            conn.close()
            if data:
                print("Successfully retrieved user")
                from models import User
                return User(data[0], data[1], data[3], self.URL, self.SSL) # user, pass
            else:
                print("Failed to retrieve user: no user")
                return None
        except:
            print("Failed to retrieve user: no connection", sys.exc_info()[1])
            return None

    # get all rating categories from the db
    def getCategories(self):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT * FROM RatingCategories')
            categories = cur.fetchall()
            cur.close()
            conn.close()
            print('Successfully retrieved rating categories')
            return categories
        except:
            print('Failed to retrieve rating categories')
            return None

    # get the code of a given video id
    def getCode(self, vid):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT Code FROM Videos WHERE Id = %s', (vid,))
            code = cur.fetchall()
            cur.close()
            conn.close()
            print('Successfully retrieved video', vid, 'code')
            return code
        except:
            print('Failed to retrieve video', vid, 'code because', sys.exc_info()[1])
            return None
    # get the given user's ratings of a given video
    def getVideoUserRatings(self, vid, uid):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT * FROM Ratings WHERE VideoId=%s AND UserId=%s;', (vid, uid))
            u = cur.fetchall()
            ur = []
            for j in u:
                # append rating categoryid and rating number
                ur.append(str(j[3])) # TODO improve with Model concept
                ur.append(str(j[4]))
            print('Fetched ratings for video', vid, 'for user', uid, 'successfully.')
            cur.close()
            conn.close()
            return ur
        except:
            print('Failed to fetch ratings for video', vid, 'for user', uid, 'because', sys.exc_info()[1])
            return []
    # get the average ratings of a given video
    def getAvgVideoRatings(self, vid):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT * FROM RatingAvgs WHERE VideoId=%s;', (vid,))
            r = cur.fetchall()
            ar = []
            for j in r:
                # append rating categoryid and rating number
                ar.append(str(j[2])) # TODO improve with Model concept
                ar.append(str(j[4]))
            print('Received average ratings for video', vid, 'successfully.')
            cur.close()
            conn.close()
            return ar
        except:
            print('Failed to receive average ratings for video', vid, 'because', sys.exc_info()[1])
            return []

    # TODO improve by minimizing time function possesses lock on the db connection
    def updateRating(self, videoId, userId, categoryId, rating):
        rating = float(rating)
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT Total, Average FROM RatingAvgs WHERE VideoId=%s AND RatingCategoryId=%s;', (videoId, categoryId))
            result = cur.fetchone()
            cur.execute('SELECT * FROM Ratings WHERE VideoId=%s AND UserId=%s AND RatingCategoryId=%s;', (videoId, userId, categoryId))
            oldRatingRow = cur.fetchone()
            print("oldRatingRow:", oldRatingRow)
            # if rating exists, remove old rating and insert new
            if oldRatingRow != None: # assumption: a rating exists, the rating average exists too
                print("result: ", result[0])
                if result[0] > 1:
                    revertedRating = (result[0] * result[1] - oldRatingRow[4]) / (result[0] - 1)
                    newRating = (revertedRating * (result[0] - 1) + rating) / result[0]
                else: # if there's only one rating to begin with
                    newRating = rating
                cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE VideoId=%s AND RatingCategoryId=%s;', (newRating, result[0], videoId, categoryId))
                cur.execute('UPDATE Ratings SET rating=%s WHERE VideoId=%s AND UserId=%s AND RatingCategoryId=%s;', (rating, videoId, userId, categoryId))
            # if rating doesn't exist, insert into db
            else:
                if result != None:
                    newTotal = result[0] + 1
                    newAvg = (newTotal * result[1] + float(rating)) / (newTotal + 1)
                    cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE VideoId=%s AND RatingCategoryId=%s;', (newAvg, newTotal, videoId, categoryId))
                else:
                    cur.execute('INSERT INTO RatingAvgs VALUES(DEFAULT, %s, %s, %s, %s);', (videoId, categoryId, 1, rating))
                cur.execute('INSERT INTO Ratings VALUES(DEFAULT, %s, %s, %s, %s, DEFAULT);', (videoId, userId, categoryId, rating))
            conn.commit()
            print('Sent rating', rating, 'for video', videoId, 'for user', userId, 'of type', categoryId, 'successfully.')
            cur.close()
            conn.close()
            return "test success"
        except:
            print('Failed to send rating', rating, 'for video', videoId, 'for user', userId, 'of type', categoryId, 'because', sys.exc_info()[0:2])
            return "test failed"
    
    # authenticates a user and starts a session
    def loginUser(self, username, password, remember):
        from flask import flash
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT password FROM Users WHERE Name = %s AND Password = crypt(%s, Password);', (username, password))
            encryptedPassword = cur.fetchall()[0][0]
            cur.execute('SELECT Id FROM Users WHERE Name = %s AND Password = %s;', (username, encryptedPassword))
            id = cur.fetchall()[0][0]
            if id:
                # bool returns True for any string, False for blank/None
                sys.path.insert(0, 'srv')
                from models import User
                user = User(id, username, encryptedPassword, self.URL, self.SSL)
                print("user inited")
                from flask_login import login_user
                login_user(user, remember = bool(remember))
                flash('Logged in successfully.')
                assert(user.is_authenticated)
                print("user authenticated")
            else:
                flash('Login failed.')
                print("authentication failed: invalid credentials")
                raise
            cur.close()
            conn.close()
        except:
            print("authentication failed: no connection to database - ", sys.exc_info()[1])
            flash('Login failed.')
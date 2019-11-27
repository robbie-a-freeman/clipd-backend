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
    
    # get all clips in the db
    def getAllClips(self):
        conn = psycopg2.connect(self.URL, sslmode=self.SSL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM clips")
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

    # get the code of a given clip id
    def getCode(self, cid):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT Code FROM Clips WHERE Id = %s', (cid,))
            code = cur.fetchall()
            cur.close()
            conn.close()
            print('Successfully retrieved clip', cid, 'code')
            return code
        except:
            print('Failed to retrieve clip', cid, 'code because', sys.exc_info()[1])
            return None
    # get the given user's ratings of a given clip
    def getClipUserRatings(self, cid, uid):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT * FROM Ratings WHERE ClipId=%s AND UserId=%s;', (cid, uid))
            u = cur.fetchall()
            ur = []
            for j in u:
                # append rating categoryid and rating number
                ur.append(str(j[3])) # TODO improve with Model concept
                ur.append(str(j[4]))
            print('Fetched ratings for clip', cid, 'for user', uid, 'successfully.')
            cur.close()
            conn.close()
            return ur
        except:
            print('Failed to fetch ratings for clip', cid, 'for user', uid, 'because', sys.exc_info()[1])
            return []
    # get the average ratings of a given clip
    def getAvgClipRatings(self, cid):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT * FROM RatingAvgs WHERE ClipId=%s;', (cid,))
            r = cur.fetchall()
            ar = []
            for j in r:
                # append rating categoryid and rating number
                ar.append(str(j[2])) # TODO improve with Model concept
                ar.append(str(j[4]))
            print('Received average ratings for clip', cid, 'successfully.')
            cur.close()
            conn.close()
            return ar
        except:
            print('Failed to receive average ratings for clip', cid, 'because', sys.exc_info()[1])
            return []

    # TODO improve by minimizing time function possesses lock on the db connection
    def updateRating(self, clipId, userId, categoryId, rating):
        rating = float(rating)
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT Total, Average FROM RatingAvgs WHERE ClipId=%s AND RatingCategoryId=%s;', (clipId, categoryId))
            result = cur.fetchone()
            cur.execute('SELECT * FROM Ratings WHERE ClipId=%s AND UserId=%s AND RatingCategoryId=%s;', (clipId, userId, categoryId))
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
                cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE ClipId=%s AND RatingCategoryId=%s;', (newRating, result[0], clipId, categoryId))
                cur.execute('UPDATE Ratings SET rating=%s WHERE ClipId=%s AND UserId=%s AND RatingCategoryId=%s;', (rating, clipId, userId, categoryId))
            # if rating doesn't exist, insert into db
            else:
                if result != None:
                    newTotal = result[0] + 1
                    newAvg = (newTotal * result[1] + float(rating)) / (newTotal + 1)
                    cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE ClipId=%s AND RatingCategoryId=%s;', (newAvg, newTotal, clipId, categoryId))
                else:
                    cur.execute('INSERT INTO RatingAvgs VALUES(DEFAULT, %s, %s, %s, %s);', (clipId, categoryId, 1, rating))
                cur.execute('INSERT INTO Ratings VALUES(DEFAULT, %s, %s, %s, %s, DEFAULT);', (clipId, userId, categoryId, rating))
            conn.commit()
            print('Sent rating', rating, 'for clip', clipId, 'for user', userId, 'of type', categoryId, 'successfully.')
            cur.close()
            conn.close()
            return "test success"
        except:
            print('Failed to send rating', rating, 'for clip', clipId, 'for user', userId, 'of type', categoryId, 'because', sys.exc_info()[0:2])
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
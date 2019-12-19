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

        clips = []
        from models import Clip
        for c in data:
            print(len(c))
            clips.append(Clip(*c, self))
        return clips

    # returns one row of a matching id from a given table
    def getOneElementById(self, tableName, id):
        conn = psycopg2.connect(self.URL, sslmode=self.SSL)
        cur = conn.cursor()
        # LIMIT 1
        from psycopg2 import sql
        cur.execute(sql.SQL("SELECT * FROM {} WHERE Id = %s").format(sql.Identifier(tableName)), (id,))
        data = cur.fetchone()
        cur.close()
        conn.close()
        return data

    # get a user by just the username
    def getUserByName(self, name):
        conn = psycopg2.connect(self.URL, sslmode=self.SSL)
        cur = conn.cursor()
        from psycopg2 import sql
        cur.execute(sql.SQL("SELECT * FROM {} WHERE Name = %s").format(sql.Identifier('users')), (name,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    # get the user by id, used for auth
    def getUserById(self, id):
        try:
            data = self.getOneElementById('users', id)
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

    # get the event by id
    def getEventById(self, id):
        try:
            data = self.getOneElementById('events', id)
            if data:
                print("Successfully retrieved event")
                from models import Event
                return Event(*data, self)
            else:
                print("Failed to retrieve event: no event")
                return None
        except:
            print("Failed to retrieve event: no connection", sys.exc_info()[1])
            return None

    # get the map by id
    def getMapById(self, id):
        try:
            data = self.getOneElementById('maps', id)
            if data:
                print("Successfully retrieved map")
                from models import Map
                return Map(*data)
            else:
                print("Failed to retrieve map: no map")
                return None
        except:
            print("Failed to retrieve map: no connection", sys.exc_info()[1])
            return None

    # get the player by id
    def getPlayerById(self, id):
        try:
            data = self.getOneElementById('players', id)
            if data:
                print("Successfully retrieved player")
                from models import Player
                return Player(*data)
            else:
                print("Failed to retrieve player: no player")
                return None
        except:
            print("Failed to retrieve player: no connection", sys.exc_info()[1])
            return None

    # get the team by id
    def getTeamById(self, id):
        try:
            data = self.getOneElementById('teams', id)
            if data:
                print("Successfully retrieved team")
                from models import Team
                return Team(*data)
            else:
                print("Failed to retrieve team: no team")
                return None
        except:
            print("Failed to retrieve user: no connection", sys.exc_info()[1])
            return None

    # get the clip by id
    def getClipById(self, id):
        try:
            data = self.getOneElementById('clips', id)
            if data:
                print("Successfully retrieved clip")
                from models import Clip
                return Clip(*data, self)
            else:
                print("Failed to retrieve clip: no clip")
                return None
        except:
            print("Failed to retrieve clip: no connection", sys.exc_info()[1])
            return None

    # get the organizer by id
    def getOrganizerById(self, id):
        try:
            data = self.getOneElementById('organizers', id)
            if data:
                print("Successfully retrieved organizer")
                from models import Organizer
                return Organizer(*data)
            else:
                print("Failed to retrieve organizer: no organizer")
                return None
        except:
            print("Failed to retrieve organizer: no connection", sys.exc_info()[1])
            return None
            
    # get the weaponListing by list of ids
    def getWeaponListingById(self, ids):
        try:
            data = []
            for i in ids:
                print("retrieved weapon: ", self.getOneElementById('weapons', i))
                data.append(self.getOneElementById('weapons', i))
            if data:
                from models import Weapon
                weapons = []
                for r in data:
                    weapons.append(Weapon(*r))
                print("Successfully retrieved weapon")
                return weapons
            else:
                print("Failed to retrieve weapon: no weapon")
                return None
        except:
            print("Failed to retrieve weapon: no connection,", sys.exc_info()[1])
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

    # get all the weapon types
    def getWeaponTypes(self):
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            cur.execute('SELECT Name FROM Weapons')
            t = cur.fetchall()
            print('Fetched Weapon types successfully.')
            cur.close()
            conn.close()
            return t
        except:
            print('Failed to fetch Weapon types because', sys.exc_info()[1])
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
                    print("beginning calculation of new avg")
                    revertedRating = (result[0] * result[1] - oldRatingRow[4]) / (result[0] - 1)
                    print("result[0]:", result[0])
                    print("result[1]:", result[1])
                    print("oldRatingRow[4]:", oldRatingRow[4])
                    print("result[0] - 1:", result[0] - 1)
                    print("revertedRating:", revertedRating)
                    newRating = (revertedRating * (result[0] - 1) + rating) / result[0]
                    print("newRating:", newRating)
                else: # corner case: if there's only one rating to begin with
                    newRating = rating
                cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE ClipId=%s AND RatingCategoryId=%s;', (newRating, result[0], clipId, categoryId))
                cur.execute('UPDATE Ratings SET rating=%s WHERE ClipId=%s AND UserId=%s AND RatingCategoryId=%s;', (rating, clipId, userId, categoryId))
            # if rating doesn't exist, insert into db
            else:
                if result != None:
                    newAvg = (result[0] * result[1] + float(rating)) / (result[0] + 1)
                    cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE ClipId=%s AND RatingCategoryId=%s;', (newAvg, result[0] + 1, clipId, categoryId))
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

    def signUpUser(self, username, email, password, weapon):
        from flask import flash
        try:
            conn = psycopg2.connect(self.URL, sslmode=self.SSL)
            cur = conn.cursor()
            weaponTest = 'mag7'
            cur.execute("INSERT INTO Users VALUES(DEFAULT, %s, %s, crypt(%s, gen_salt('bf')), DEFAULT, DEFAULT, %s)", (username, email, password, weaponTest))
            conn.commit()
            print("Sign up success!")
            flash('Welcome to Clip\'d!')
            cur.close()
            conn.close()
        except:
            print("Sign up failed - ", sys.exc_info()[1])
            flash('Sign up failed.')
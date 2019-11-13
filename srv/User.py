class User:
    username = None
    password = None
    DATABASE_URL = ''
    SSL_MODE = ''

    def __init__(self, i, u, p, db, ssl):
        self.id = i
        self.username = u
        self.password = p
        self.DATABASE_URL = db
        self.SSL_MODE = ssl

    # This property should return True if the user is authenticated,
    # i.e. they have provided valid credentials. (Only authenticated
    # users will fulfill the criteria of login_required.)
    @property
    def is_authenticated(self):
        try:
            import psycopg2
            conn = psycopg2.connect(self.DATABASE_URL, sslmode=self.SSL_MODE)
            cur = conn.cursor()
            cur.execute('SELECT Id FROM Users WHERE Name = %s AND Password = %s;', (self.username, self.password))
            data = cur.fetchall()
            cur.close()
            conn.close()
            if data:
                print("Successfully auth'd user")
                return True
            else:
                print("Failed to auth user: no user")
                return False
        except:
            print("Failed to auth user: no connection to db")
            return False

    # This property should return True if this is an active user - in
    # addition to being authenticated, they also have activated their
    # account, not been suspended, or any condition your application
    # has for rejecting an account. Inactive accounts may not log in
    # (without being forced of course).
    @property
    def is_active(self):
        return self.is_authenticated

    # This property should return True if this is an anonymous user.
    # (Actual users should return False instead.)
    @property
    def is_anonymous(self):
        return False

    # This method must return a unicode that uniquely identifies this
    # user, and can be used to load the user from the user_loader
    # callback. Note that this must be a unicode - if the ID is
    # natively an int or some other type, you will need to convert
    # it to unicode.
    def get_id(self):
        return self.id
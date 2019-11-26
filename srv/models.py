#from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Array

'''class Videos(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)'''

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
'''
# Weapon enum, store different weapons
import enum
class Weapon(enum.Enum):
    cz = 'cz'
    desertEagle = 'desert_eagle'
    dualBerettas = 'dual_berettas'
    fiveSeven = 'five_seven'
    glock = 'glock'
    p2000 = 'p2000'
    p250 = 'p250'
    r8 = 'r8'
    tec9 = 'tec9'
    usp = 'usp'
    mag7 = 'mag7'
    nova = 'nova'
    sawedOff = 'sawed_off'
    xm = 'xm'
    mac10 = 'mac10'
    mp5 = 'mp5'
    mp7 = 'mp7'
    mp9 = 'mp9'
    p90 = 'p90'
    pp_bizon = 'pp_bizon'
    ump = 'ump'
    ak = 'ak'
    aug = 'aug'
    famas = 'famas'
    galil = 'galil'
    m4a1s = 'm4a1s'
    m4a4 = 'm4a4'
    sg = 'sg'
    awp = 'awp'
    g3sg1 = 'g3sg1'
    scar = 'scar'
    ssg = 'ssg'
    m249 = 'm249'
    negev = 'negev'
    knife = 'knife'
    zeus = 'zeus'
    he = 'he'
    fire = 'fire'
    flash = 'flash'
    smoke = 'smoke'


class Video:
    id = Column(Integer, primary_key=True)
    code = Column(String(512))
    event = Column(String(64))
    map = Column(String(32))
    player = Column(String(32))
    team = Column(String(64), nullable=True)
    grandFinal = Column(Boolean)
    armor = Column(Boolean)
    crowd = Column(Boolean)
    kills = Column(Integer)
    clutchkills = Column(Integer)
    weapon = Column(ARRAY(Enum(Weapon)))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)    
'''
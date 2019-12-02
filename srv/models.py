# Weapon enum, store different weapons
from enum import Enum, unique
@unique
class Weapon(Enum):
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

class Clip:
    id = 0
    code = ''
    event = None
    map = None
    player = None
    team = None
    grandFinal = False
    armor = False
    crowd = False
    kills = -1
    clutchKills = -1
    weapon = []
    db = None

    def __init__(self, id, code, eventId, mapId, playerId, teamId, \
                 grandFinal, armor, crowd, kills, clutchKills, \
                 weapon, db):
        # simple assignments
        self.id = id
        self.code = code
        self.grandFinal = grandFinal
        self.armor = armor
        self.crowd = crowd
        self.kills = kills
        self.clutchKills = clutchKills
        self.weapon = weapon
        self.db = db

        # fetching objects from the db
        self.event = db.getEventById(eventId)
        self.map = db.getMapById(mapId)
        self.player = db.getPlayerById(playerId)
        self.team = db.getTeamById(teamId)
    
    def asList(self):
        return [self.id, \
                self.code, \
                self.grandFinal, \
                self.armor, \
                self.crowd, \
                self.kills, \
                self.clutchKills, \
                self.weapon, \
                self.event.name, \
                self.map.name, \
                self.player.alias, \
                self.team.alias]

class Team:
    id = 0
    alias = ''
    alternateAliases = []
    isActive = False

    def __init__(self, id, alias, alternateAliases, isActive):
        # simple assignments
        self.id = id
        self.alias = alias
        self.alternateAliases = alternateAliases
        self.isActive = isActive

class Map:
    id = 0
    name = ''
    isActiveDuty = False
    currentBigVersion = False

    def __init__(self, id, name, isActiveDuty, currentBigVersion):
        # simple assignments
        self.id = id
        self.name = name
        self.isActiveDuty = isActiveDuty
        self.currentBigVersion = currentBigVersion

class Player:
    id = 0
    alias = ''
    name = ''
    country = ''
    alternateAliases = []
    isActive = False

    def __init__(self, id, alias, name, country, alternateAliases, isActive):
        # simple assignments
        self.id = id
        self.alias = alias
        self.name = name
        self.country = country
        self.alternateAliases = alternateAliases
        self.isActive = isActive

class Organizer:
    id = 0
    name = ''
    eventSeries = ''

    def __init__(self, id, name, eventSeries):
        # simple assignments
        self.id = id
        self.name = name
        self.eventSeries = eventSeries

class Event:
    id = 0
    name = ''
    organizer = None
    location = ''
    prizePool = ''
    startDate = None
    endDate = None
    db = None

    def __init__(self, id, name, organizerId, location, prizePool,\
                 startDate, endDate, db):
        # simple assignments
        self.id = id
        self.name = name
        self.location = location
        self.prizePool = prizePool
        self.startDate = startDate
        self.endDate = endDate
        self.db = db

        # fetching db object
        self.organizer = db.getOrganizerById(organizerId)

class User:
    id = 0
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

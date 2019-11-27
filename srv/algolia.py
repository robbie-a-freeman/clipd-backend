from algoliasearch.search_client import SearchClient

def testSearch(query):
    import asyncio
    app_id = '10E1WBKVLO'
    api_key = 'bcf375829b1daec9b14b8b765ec31a58'

    async def test(query):
        async with SearchClient.create(app_id, api_key) as client:
            index = client.init_index('articles')

            response = await index.save_objects_async([
                {'objectID': 1, 'foo': 'bar'},
                {'objectID': 2, 'foo': 'foo'}
            ])

            results = await index.search_async(query)

            print(results)

    asyncio.run(test())


#def searchForVideos():

def oldSearchForVideos(query, data, db, userId):
    results = []
    # each comma separated group represents and AND clause
    for p in query.split(','):
        queryTerms = p.split(" ") # use later to search for specific terms like map
        phraseResults = []
        if query:
            # Assumption: there better only by one instance of 1vX. if not takes the first one
            clutchKills = -1 # -1 means no requirement
            i = query.find("1v")
            if i > -1 and len(query) - i > 2:
                clutchKills = int(query[i + 2])
                if clutchKills and 0 <= clutchKills and 5 >= clutchKills: # if there's a number after v
                    clutchKills = int(query[i + 2])
                else:
                    clutchKills = -1

            for d in data:
                if queryRequirements(query) and (query in d or query.lower() in d or d[4] == clutchKills) and [d[1], d[4], d[2]] not in phraseResults:
                    # get user's past reviews for selected videos
                    ur = db.getVideoUserRatings(d[0], userId)
                    phraseResults.append([d[0], d[1], d[4], d[2], ur])
        for r in phraseResults:
            if r not in results:
                results.append(r)
    return results

# this is a bad function
def queryRequirements(q):
    if q == 'true' or q == 'false':
        return False
    return True

# Index all the clips in the db upon server start
def initializeClipsIndex(db):
    allClips = db.getAllVideos()
    app_id = '10E1WBKVLO'
    api_key = 'bcf375829b1daec9b14b8b765ec31a58'
    client = SearchClient.create(app_id, api_key)
    index = client.init_index('clips')
    for v in allClips:
        index.save_object({
            'objectID': v[0],
            'Code': v[1],
            'Event': v[2],
            'Map': v[3],
            'Player': v[4],
            'Team': v[5],
            'GrandFinal': v[6],
            'Armor': v[7],
            'Crowd': v[8],
            'Kills': v[9],
            'ClutchKills': v[10],
            'Weapon': v[11]
        })

# search the index 'clips' for matching clips
def clipSearch(query):
    import asyncio
    app_id = '10E1WBKVLO'
    api_key = 'bcf375829b1daec9b14b8b765ec31a58'

    async def test(query):
        async with SearchClient.create(app_id, api_key) as client:
            index = client.init_index('clips')

            results = await index.search_async(query)

            return results

    return asyncio.run(test(query))

'''CREATE TABLE Videos(
	Id SERIAL PRIMARY KEY,
	Code VARCHAR(512) NOT NULL,
	Event VARCHAR(64) NULL,
	Map VARCHAR(32) NOT NULL,
	Player VARCHAR(32) NOT NULL,
	Team VARCHAR(64) NULL,
	GrandFinal BOOLEAN NOT NULL,
	Armor BOOLEAN NOT NULL,
	Crowd BOOLEAN NOT NULL,
	Kills INT CHECK (kills >= 0 AND kills <= 5),
	ClutchKills INT CHECK (clutchkills >= 0 AND clutchkills <= 5),
	Weapon WEAPON ARRAY NOT NULL
);'''
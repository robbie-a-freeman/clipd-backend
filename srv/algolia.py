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


#def searchForClips():

def oldSearchForClips(query, data, db, userId):
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
                    # get user's past reviews for selected Clips
                    ur = db.getClipUserRatings(d[0], userId)
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
    app_id = '10E1WBKVLO'
    api_key = 'bcf375829b1daec9b14b8b765ec31a58'
    client = SearchClient.create(app_id, api_key)
    index = client.init_index('clips')
    from models import Clip
    allClips = db.getAllClips()
    for c in allClips:
        grandFinalResult = 'Not a Grand Final'
        if c.grandFinal:
            grandFinalResult = 'Grand Final'
        armorResult = 'No armor'
        if c.armor:
            armorResult = 'Armor'
        crowdResult = 'No crowd'
        if c.crowd:
            crowdResult = 'Crowd'

        index.save_object({
            'objectID': c.id,
            'Code': c.code,
            'Event': c.event.name,
            'Map': c.map.name,
            'Player': c.player.alias,
            'Team': c.team.alias,
            'GrandFinal': grandFinalResult,
            'Armor': armorResult,
            'Crowd': crowdResult,
            'Kills': ' '.join([str(c.kills), ' kills']),
            'ClutchKills': 'v'.join(['1', str(c.clutchKills)]),
            'Weapon': c.weapon
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
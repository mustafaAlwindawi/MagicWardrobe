import json
import requests
import pandas
import numpy #If numpy not working install numpy==1.19.3
import pgeocode


class PlacesRecommendation:
    def __init__(self, zipCode, temperature, rainOrSnow):
        self.zipCode = zipCode
        self.temperature = temperature
        self.rainOrSnow = rainOrSnow
        places = self.recommendPlace()

        if places == []:
            self.place1 = []
            self.place2 = []
        elif places[0] != [] and places[1] == []:
            self.place1 = places[0]
            self.place2 = []
        else:
            self.place1 = places[0]
            self.place2 = places[1]


    def getPlace(self, Query):
        n = pgeocode.Nominatim('ca')
        location = n.query_postal_code(self.zipCode)
        coordin = "{}, {}".format(location.latitude, location.longitude)

        url = 'https://api.foursquare.com/v2/venues/explore'

        parameters = dict(
        client_id = 'NIVZAW3SGIFSRR0IIYCLGMHBDF3KIYPSCAK4KD1BCIETKXQ2',
        client_secret = '10ISH4XSBLDA4OGBHF0XIATDOUHI4R1LTXWJBAPSNZWZLNJV',
        v ='20201110',
        ll = coordin,
        query = Query,
        radius = 5000,
        limit = 1
        )
        req = requests.get(url=url, params=parameters)
        r = json.loads(req.text)

        if r == "[]" or r == "":
            return []

        rawdata = r['response']['groups'][0]['items']
        data = pandas.json_normalize(rawdata)

        def getCategoryType(row):        
            try:
                clist = row['categories']
            except:
                clist = row['venue.categories']
            
            if len(clist) == 0:
                return None
            else:
                return clist[0]['name']

        columns = ['venue.categories', 'venue.name', 'venue.location.address']
        data.reindex(columns)
        if (len(data.columns)) == 0:
            return []

        data['venue.categories'] = data.apply(getCategoryType, axis=1)
        data.columns = [col.split('.')[-1] for col in data.columns]

        if ((data.columns == 'categories').any() == True and (data.columns == 'name').any() == True and (data.columns == 'address').any() == True):
            place = [data['categories'][0], data['name'][0], data['address'][0]]
        else:
            return []


        return place

    def recommendPlace(self):
        # 20 deg celsius or up     
        warmPlaces = ['ice cream' , 'pool', 'winery', 'golf', 'restaurant', 'mall', 'bar', 'starbucks', 'coffee', 'fast food']
        # Between 19 and 14
        mildPlaces = ['restaurant', 'mall', 'bar', 'starbucks', 'coffee', 'fast food']
        # 13 and below
        coldPlaces = ['coffee', 'restaurant', 'bar', 'mall']
        # Is snowing or raining (indoor places)
        snowOrRainPlaces = ['restaurant', 'coffee', 'bar', 'Tim Hortons']

        pcode = self.zipCode
        weather = self.temperature
        snowOrRain = self.rainOrSnow

        place1 = []
        place2 = []
        hasSearched = False

        if snowOrRain == True:
            for x in snowOrRainPlaces:
                if place1 == []:
                    place1 = self.getPlace(x)
                else:
                    place2 = self.getPlace(x)
                if place2 != [] and place2 != place1:
                    break
            hasSearched = True


        if place1 == [] and place2 == [] and hasSearched == False:
            if weather >= 20.0:
                for x in warmPlaces:
                    if place1 == []:
                        place1 = self.getPlace(x)
                    else:
                        place2 = self.getPlace(x)
                    if place2 != [] and place2 != place1:
                        break
                hasSearched = True


        if place1 == [] and place2 == [] and hasSearched == False:
            if weather < 20.0 and weather > 13.0:
                for x in mildPlaces:
                    if place1 == []:
                        place1 = self.getPlace(x)
                    else:
                        place2 = self.getPlace(x)
                    if place2 != [] and place2 != place1:
                        break
                hasSearched = True


        if place1 == [] and place2 == [] and hasSearched == False:
            if weather <= 13.0:
                for x in coldPlaces:
                    if place1 == []:
                        place1 = self.getPlace(x)
                    else:
                        place2 = self.getPlace(x)
                    if place2 != [] and place2 != place1:
                        break

        if place1 == [] and place2 == []:
            return []

        if place2 == []:
            return [place1, ] 
        else:
            places = [place1, place2]
            return places


''' PlacesRecommendation gives 2 recommended places (place1, place2). Each is a String list that has the place category 
(ice Cream Shop, Park, etc), place name and place address that can be gotten through place1/2[0], place1/2[1], place1/2[2] 
respectively. Example below shows how to use the PlacesRecommendation class to get the 2 recommended places based on the 
zip code, temperature (celsius) and whether or not it is snowing/raining. If no places are found then the class variables 
place1 and place2 will be empty. If only one place is found then place2 will be empty. The examples below print this if either
of those scenarios are the case.
'''

places = PlacesRecommendation("N0R 1A0", 20, False)

if places.place1 != []:
    print("Place: " + places.place1[0] + "    Name: " + places.place1[1] + "    Address: " + places.place1[2])
    if places.place2 != []:
        print("Place: " + places.place2[0] + "    Name: " + places.place2[1] + "    Address: " + places.place2[2])
    else:
        print("Place 2 not found")
else:
    print("No places found")

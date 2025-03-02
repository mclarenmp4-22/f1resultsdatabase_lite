'''
This code is supposed to scrape all the F1 race results and put it into a database.

If you want to reset/initialise the database, run reset.py before running this.

AI use disclosure:
    For the record, I did most of this code by myself. 
    Github Copilot is very useful in the completions and reviews.
    It also did the zip('drivers', 'nationalities') part.
    It fully generated only the extract_engine function and the test cases for it.
    Ironically, Github Copiltot suggested me the above three lines.
    It is Github COPILOT, not AUTOPILOT.


I REALLY hate you, shared cars.
I REALLY hate you, sprint races.
You make my life harder.

'''
#importing packages
import sqlite3 #to store data
import urllib.request, urllib.parse, urllib.error #to connect with the internet
from bs4 import BeautifulSoup #for web scraping
import re


conn = sqlite3.connect('sessionresults.db') #connects to the database
cur = conn.cursor() #cursor object

#example link: https://gpracingstats.com/seasons/2019-world-championship/2019-chinese-grand-prix/
#get races: https://gpracingstats.com/seasons/2019-world-championship/

html = urllib.request.urlopen("https://gpracingstats.com/seasons/").read() #open the website with all f1 seasons to loop through the seasons
soup = BeautifulSoup(html, 'html.parser') #initialize the soup object
tags = soup('table') #find the seasons table
#print (str(tags[0]))
soup = BeautifulSoup(str(tags[0]), 'html.parser')
tag2 = soup ('a') #find all the links in this
def extract_engine(team_name):
    # Check for "(privateer)" and remove it
    is_privateer = "(privateer)" in team_name
    team_name = team_name.replace("(privateer)", "").strip()
    
    parts = team_name.split('-')
    
    # If there is no hyphen, assume the engine is the same as the team
    if len(parts) == 1:
        return team_name, team_name, is_privateer  # (team, engine, privateer status)

    # Extract the last part as the engine name
    engine = parts[-1]

    # Special case: If the last part is already in the team name, return it
    if engine in team_name[:-len(engine)]:
        return '-'.join(parts[:-1]), engine, is_privateer  # Remove the last redundant part

    return '-'.join(parts[:-1]), engine, is_privateer  # Return team name without engine

def extract_engine(team_name):
    # Check for "(privateer)" and remove it
    is_privateer = "(privateer)" in team_name
    team_name = team_name.replace("(privateer)", "").strip()
    
    parts = team_name.split('-')
    
    # If there is no hyphen, assume the engine is the same as the team
    if len(parts) == 1:
        return team_name, team_name, is_privateer  # (team, engine, privateer status)

    # Extract the last part as the engine name
    engine = parts[-1]

    # Special case: If the last part is already in the team name, return it
    if engine in team_name[:-len(engine)]:
        return '-'.join(parts[:-1]), engine, is_privateer  # Remove the last redundant part

    return '-'.join(parts[:-1]), engine, is_privateer  # Return team name without engine



'''# Test Cases
teams = [
    "McLaren-Mercedes",  # Should return ("McLaren", "Mercedes")
    "Ferrari",           # Should return ("Ferrari", "Ferrari")
    "Talbot-Lago-Talbot",# Should return ("Talbot-Lago", "Talbot")
    "Red Bull-Honda",    # Should return ("Red Bull", "Honda")
    "Brabham-BMW",       # Should return ("Brabham", "BMW")
]

for team in teams:
    constructor, engine = extract_engine(team)
    print(f"Original: {team} | Constructor: {constructor} | Engine: {engine}")
    
'''
triggered = False
triggered2 = False
#we need to find the current gp and skip all of them because i'm not interested in waiting 15 minutes every time i run this code
select = cur.execute ('SELECT GrandPrix from GrandsPrix ORDER BY GrandPrix DESC LIMIT 1') #selects the most recent Grand Prix
rows = select.fetchall()
if len(rows) == 0:
    lastgp = None    #start from the first race
else:    
    lastgp = rows[0][0] #stores the most recent Grand Prix in a variable
#lastgp = '2024-miami-grand-prix-sprint' #for testing purposes 
if lastgp != None:  
    if lastgp.endswith('-sprint'):
        lastgp = lastgp[:-7]  
    tostart = urllib.request.urlopen(f"https://gpracingstats.com/{lastgp}").read()
    soup = BeautifulSoup(tostart, 'html.parser')
    ts = soup('a')
    for t in ts:
        if t.get('class') == ['breadcrumb-link']:
            year = t.get('href')
            if year is not None and year.startswith('https://gpracingstats.com/seasons/'):
                match = re.match(r"^https://gpracingstats\.com/seasons/(\d{4}-[\w-]+)/?$", year)
                if match and match.group(1):  
                    neededyear = year  
                    #theactualyear =  match.group(1)[0:4]
else:
    neededyear = 'https://gpracingstats.com/seasons/1950-world-championship/'
    #theactualyear = '1950'  
    triggered2 = True                     
#result = any (neededyear == s for s in tag2) #checks if the current season is in the list
#print (bool(neededyear in tag.get('href', None) for tag in tag2))
#string_to_be_found = ' ' + f'<a href="{neededyear}">{theactualyear}</a>'
#print(string_to_be_found)
#print (tag2.index(string_to_be_found))
#time to do a lot of web scraping
tablecount = 0 #to find whether it is a sprint...
for tag in tag2[::-1]:  # [::-1] reverses the list so we can start from 1950 and stop at the current season
    link = tag.get('href', None)  # get the link
    if link is not None and link.startswith('https://gpracingstats.com/seasons/'):  # if it is a season link
        if link == neededyear:
            triggered = True        
        elif link != neededyear and triggered == False:
            print (f"Skipping {link}")
            continue
        html = urllib.request.urlopen(link).read()  # open the season link
        soup = BeautifulSoup(html, 'html.parser')  # initialize the soup object
        tags = soup('table')  # find all tables
        for tag in tags:  # loop through all tables
            forl = tag.get('class', None)  # get the class of the table
            if forl is not None and forl == ['summary', 'season-results', 'align-r-3', 'data-items-3']:  # if it is a season results table
                soup = BeautifulSoup(str(tag), 'html.parser')  # initialize the soup object
                tags = soup('a')  # find all links
                for tag in tags:  # loop through all links
                    link = tag.get('href', None)
                    year_match = re.search(r'/seasons/(\d{4})-', link).group(1)  # gets year
                    if link is not None and link.startswith(f'https://gpracingstats.com/seasons/{year_match}-world-championship/'):  # gets race
                        html = urllib.request.urlopen(link).read()
                        soup = BeautifulSoup(html, 'html.parser')
                        tags = soup('table')
                        currentgp = re.search(r'/([^/]+)/$', link).group(1)  # gets current gp        
                        
                        if currentgp == lastgp:
                            triggered2 = True
                            print (f"Skipping {currentgp}")
                            continue                            
                        elif currentgp != lastgp and triggered2 == False:
                            print (f"Skipping {currentgp}")
                            continue          

                        for tag in tags:  # loops through the tables
                            forl = tag.get('class', None)
                            if forl is not None and forl == ['summary', 'race-results-7-col']:  # if it is a race result table
                                tablecount += 1
                                if tablecount == 2:
                                    currentgp = f"{currentgp}-sprint"                                   
                                soup = BeautifulSoup(str(tag), 'html.parser')
                                tags = soup('tr')

                                for tag in tags:
                                    # make sure it is not the header
                                    if str(tag) != '<tr><th colspan="2" scope="col">Pos</th><th scope="col">Driver</th><th scope="col">Constructor</th><th scope="col">Laps</th><th scope="col">Time</th><th scope="col">Points</th></tr>':
                                        '''
                                        example tag: 
                                        <tr>
                                        <td>1</td>
                                        <td>&nbsp;</td>
                                        <td><span class="brackets nationality">(<abbr title="Great Britain">GBR</abbr>)</span>
                                        <a href="https://gpracingstats.com/drivers/lando-norris/">Lando Norris</a></td>
                                        <td><a href="https://gpracingstats.com/constructors/mclaren/">McLaren</a>-Mercedes</td>
                                        <td>58</td>
                                        <td>1hr 26m 33.291s</td>
                                        <td>25</td>
                                        </tr> '''
                                        soup = BeautifulSoup(str(tag), 'html.parser')
                                        tags = soup('td')
                                        if len(tags) == 7:  # if the driver started the race
                                            soup = BeautifulSoup(str(tags[2]), 'html.parser')  # this is the driver column
                                            pos = tags[0].text
                                            if pos == 'R' or pos == 'DQ' or pos == 'NC':  # if the driver retired, was disqualified or did not start
                                                pos = None
                                            drivers = [a.text for a in soup.find_all('a')]  # Get all driver names
                                            nationalities = [abbr['title'] for abbr in soup.find_all('abbr')]  # Get all nationalities
                                            constructor, engine, privateer = extract_engine(tags[3].text)  # get the constructor and engine
                                            laps = tags[4].text  # get the number of laps completed by said car
                                            time = tags[5].text  # get the time taken by the car to complete/retired the race
                                            points = tags[6].text.strip()  # get the points and strip any whitespace
                                            fl = "FL" in points
                                            points = points.replace("FL", "").strip()
                                            if points == '\xa0' or points == '' or points == '&nbsp;' or len(points) == 0:  # if the points are not available
                                                points = 0
                                            else:
                                                points_list = [li.text.replace("FL", "").strip() for li in BeautifulSoup(str(tags[6]), 'html.parser').find_all('li')]
                                                points_list = [point for point in points_list if point]  # Remove empty strings
                                                if points_list:
                                                    points = float(points_list[0])  # use the first point value
                                                else:
                                                    points = float(points)  # convert points to float
                                        elif str(tags) != '<tr><td colspan="7" class="session-divider">Did not start</td></tr>':
                                            '''
                                            <tr><td>&nbsp;</td><td>&nbsp;</td>
                                            <td><span class="brackets nationality">(<abbr title="Argentina">ARG</abbr>)</span> 
                                            <a href="https://gpracingstats.com/drivers/alfredo-pian/">Alfredo Pian</a></td><td><a href="https://gpracingstats.com/constructors/maserati/">Maserati</a>
                                            <span class="brackets privateer">(privateer)</span></td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
                                            '''
                                            continue
                                        else:
                                            soup = BeautifulSoup(str(tags[2]), 'html.parser')
                                            pos = None
                                            drivers = [a.text for a in soup.find_all('a')]
                                            nationalities = [abbr['title'] for abbr in soup.find_all('abbr')]
                                            constructor, engine, privateer = extract_engine(tags[3].text)
                                            laps = None
                                            time = None
                                            points = 0
                                        for driver, nationality in zip(drivers, nationalities):
                                            cur.execute ('INSERT OR IGNORE INTO Nationalities (Nationality) VALUES (?)', (nationality,))
                                            cur.execute ('SELECT NationalityID FROM Nationalities WHERE Nationality = ?', (nationality,))
                                            nationalityid = cur.fetchone()[0]  
                                            cur.execute ('INSERT OR IGNORE INTO Drivers (DriverName, DriverNationality) VALUES (?,?)', (driver, nationalityid,))
                                            cur.execute ('INSERT OR IGNORE INTO Engines (EngineName) VALUES (?)', (engine,))
                                            cur.execute ('INSERT OR IGNORE INTO GrandsPrix (GrandPrix) VALUES (?)', (currentgp,))
                                            cur.execute ('INSERT OR IGNORE INTO Teams (TeamName) VALUES (?)', (constructor,))
                                            cur.execute ('SELECT DriverID, DriverNationality FROM Drivers WHERE DriverName = ?', (driver,))
                                            d = cur.fetchone()
                                            driverid = d[0]
                                            drivernationality = d[1]
                                            cur.execute ('SELECT EngineID FROM Engines WHERE EngineName = ?', (engine,))
                                            engineid = cur.fetchone()[0]
                                            cur.execute ('SELECT GPID FROM GrandsPrix WHERE GrandPrix = ?', (currentgp,))
                                            grandprixid = cur.fetchone()[0]
                                            cur.execute ('SELECT TeamID FROM Teams WHERE TeamName = ?', (constructor,))
                                            teamid = cur.fetchone()[0]
                                            cur.execute ('INSERT INTO GPResults (Position, Driver, Team, Laps, Engine, TimeRet, GrandPrix, Pts, Privateer, FL) VALUES (?,?,?,?,?,?,?,?,?,?)', (pos, driverid, teamid, laps, engineid, time, grandprixid, points, privateer, fl,))
                                              
                                            print(currentgp, pos, driver, nationality, constructor, engine, privateer, laps, time, points, fl)
                    
                                            

                    tablecount = 0



                                  

    #DON'T FORGET TO COMMIT!!
    conn.commit()    


    
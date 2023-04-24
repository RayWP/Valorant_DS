import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Send a GET request to the website and parse the HTML content
url = 'https://www.vlr.gg/event/stats/1191/champions-tour-2023-pacific-league'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table on the page and extract its headers and rows
table = soup.find('table')
headers = [header.text.strip() for header in table.find_all('th')]
headers.insert(2,'Team') #add Team to column

rows = []
for row in table.find_all('tr')[1:]:
    data_row = []
    cells = row.find_all('td')

    # get Player's name and team
    player_name = cells[0].find("div", {"class": "text-of"}).get_text()
    player_team = cells[0].find("div", {"class": "stats-player-country"}).get_text()

    # get Player's agents
    agent_played_img = cells[1].find_all("img")
    agent_played = []
    for agent in agent_played_img:
        agent_name = re.search(r"/([\w-]+)\.png$", agent["src"]).group(1)
        agent_played.append(agent_name)

    playedRound = cells[2].get_text()

    data_row.append(player_name)
    data_row.append(player_team)
    data_row.append(agent_played)
    data_row.append(playedRound)

    # get "Middle" Stats
    for cell in cells[3:14]:
        span = cell.find('span')
        if span is not None:
            stat = span.get_text().strip()
            data_row.append(stat)

    # get "Ending" stats
    for cell in cells[14:]:
        stat = cell.get_text().strip()
        data_row.append(stat)

    rows.append(data_row)

print(len(rows))
print(len(headers))
# # Store the data in a pandas DataFrame and save it to a CSV file
df = pd.DataFrame(data=rows, columns=headers)
# print(df)
# # print(df)
df.to_markdown()
df.to_json()
df.to_csv('./data/vlr_stats.csv', index=False)

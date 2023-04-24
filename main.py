import sys
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# if you put url in CMD, then it will use that name, or customize it yourself in the script
url_from_cmd = sys.argv[1]
url = ""
if url_from_cmd:
    # url from CMD arguments
    url = url_from_cmd
else:
    # hard-coded url
    url = "https://www.vlr.gg/event/stats/1191/champions-tour-2023-pacific-league" #put your custom URL here

# Send a GET request to the website and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table on the page and extract its headers and rows
table = soup.find('table')
table_headers = [header.text.strip() for header in table.find_all('th')]
table_headers.insert(1, 'Team')  # add Team to column header

table_rows = [] #data_row
for row in table.find_all('tr')[1:]:
    current_player_row = []

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

    # get Player's number of played rounds
    playedRound = cells[2].get_text()

    current_player_row.append(player_name)
    current_player_row.append(player_team)
    current_player_row.append(agent_played)
    current_player_row.append(playedRound)

    # get "Middle" Stats
    for cell in cells[3:14]:
        span = cell.find('span')
        if span is not None:
            stat = span.get_text().strip()
            current_player_row.append(stat)

    # get "Ending" stats
    for cell in cells[14:]:
        stat = cell.get_text().strip()
        current_player_row.append(stat)

    # append current player's stats to the rows
    table_rows.append(current_player_row)


# # Store the data in a pandas DataFrame and save it to a CSV file
df = pd.DataFrame(data=table_rows, columns=table_headers)

# if you put filename in CMD, then it will use that name, default = vlr_data
csv_name = sys.argv[2]
if csv_name:
    df.to_csv('./data/' + csv_name + '.csv', index=False)
else:
    df.to_csv('./data/vlr_data.csv', index=False)

print("DONE")

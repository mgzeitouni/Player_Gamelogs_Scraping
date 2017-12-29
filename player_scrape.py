import urllib
from bs4 import BeautifulSoup
import pdb
import csv
import os

player_ids = [{"name":"Michael-Jordan", "id":1192}, {"name":"Wilt-Chamberlain","id":65950}]


data = []

for player in player_ids:

	print ("Scraping data for player: %s"%player['name'])
	web_page = urllib.urlopen("https://basketball.realgm.com/player/%s/GameLogs/%s/NBA/All" %(player['name'], player['id'])).read()

	soup = BeautifulSoup(web_page, "html.parser")


	table = soup.find("table" )
	
	headers = ['Player_Name','Player_Id']

	# First get Header row from /thead element

	for row in table.findAll("thead"):
		for col in row.findAll("th"):

			header = col.text

			headers.append(header)


	for body in table.findAll("tbody"):

		for row in body.findAll("tr"):

			# Populate row with name and Id
			current_row = [player['name'], player['id']]
		
			for col in row.findAll("td"):

				text = col.text
	
				# Make sure we're not at last 2 rows (Totals and Averages), and append to data matrix
				if text != 'Totals' and text != 'Averages':
					# Append each col of data to this row
					current_row.append(text)

			data.append(current_row)


	print ('Done with player %s'%player['name'])

print ("Writing all data to CSV...")

csv_filename = "Player_Gamelogs.csv"

# Open as new file if exists, else append to it
open_type = 'a' if os.path.exists(csv_filename) else 'w+'

with open(csv_filename, open_type) as file:

	writer = csv.writer(file)

	# Write headers if this is new file
	if open_type=='w+':
		writer.writerow(headers) 
		
	writer.writerows(data)
	



		


		   
		  
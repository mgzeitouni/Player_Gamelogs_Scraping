import urllib
from bs4 import BeautifulSoup
import pdb
import csv
import os
import sys

if __name__ == "__main__":

	try:
		datatype = sys.argv[1]
	except:
		datatype = 'regular'

	print ("Reading players for ref file...")
	with open('Ref_player_ids.csv', 'rU') as ref_file:

		reader = csv.reader(ref_file)

		reader.next()

		ref_data = [row for row in reader]

	total_players = float(len(ref_data))

	print ("%s total players read" %total_players)

	data = []

	count = 0

	for player in ref_data:

		name = player[0]
		player_id = player[1]

		print ("Scraping data for player: %s"%name)

		url = ("https://basketball.realgm.com/player/%s/GameLogs/%s/NBA/All" %(name, player_id))

		url = url + '/' + datatype

		try:
			web_page = urllib.urlopen(url).read()

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
					current_row = [name, player_id]
				
					for col in row.findAll("td"):

						text = col.text
			
						# Make sure we're not at last 2 rows (Totals and Averages), and append to data matrix
						if text != 'Totals' and text != 'Averages':
							# Append each col of data to this row
							current_row.append(text)

					data.append(current_row)
		except:
			print("No data available for player %s for datatype %s" %(name, datatype))


		print ('Done with player %s'%name)
		print (count/total_players)
		print ('---------%.2f %% DONE with set --------' %((count/total_players)*100.0))

		count+=1

	print ("Writing all data to CSV...")

	csv_filename = "Player_Gamelogs_%s.csv" %datatype

	# Open as new file if exists, else append to it
	open_type = 'a' if os.path.exists(csv_filename) else 'w+'

	with open(csv_filename, open_type) as file:

		writer = csv.writer(file)

		# Write headers if this is new file
		if open_type=='w+':
			writer.writerow(headers) 
			
		writer.writerows(data)
		



			


			   
			  
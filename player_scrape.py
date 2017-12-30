import urllib
from bs4 import BeautifulSoup
import pdb
import csv
import os
import sys
import threading
import logging
import time


def worker(datatype, logger):

	start = time.time()
	
	logger.info ("Reading players for ref file...")
	with open('Ref_player_ids.csv', 'rU') as ref_file:

		reader = csv.reader(ref_file)

		reader.next()
		
		ref_data = [row for row in reader]

	total_players = float(len(ref_data))

	logger.info ("%s total players read" %total_players)

	count = 0

	for player in ref_data:

		data = []

		name = player[0]
		player_id = player[1]

		logger.info ("Scraping data for player: %s"%name)

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
			logger.info("No data available for player %s for datatype %s" %(name, datatype))


		logger.info ('Done with player %s'%name)

		logger.info ('---------%.2f %% DONE with set --------' %((count/total_players)*100.0))

		count+=1

		logger.info ("Writing player data to CSV...")

		csv_filename = "Player_Gamelogs_%s.csv" %datatype

		# Open as new file if exists, else append to it
		open_type = 'a' if os.path.exists(csv_filename) else 'w+'

		with open(csv_filename, open_type) as file:

			writer = csv.writer(file)

			# Write headers if this is new file
			if open_type=='w+':
				writer.writerow(headers) 
				
			writer.writerows(data)
		
	end = time.time()

	logger.info("Total minutes to run: %.2f" %((end-start)/60))
	logger.info("Total hours to run: %.2f" %((end-start)/3600))

if __name__ == "__main__":


	datatypes = ['regular', 'preseason', 'playoffs']


	for i in range(len(datatypes)):
		
		logger = logging.getLogger('%s' % (datatypes[i]))
		logger.setLevel(logging.DEBUG)

		# create a file handler writing to a file named after the thread
		file_handler = logging.FileHandler('thread-%s.log' % (datatypes[i]))

		# create a custom formatter and register it for the file handler
		formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
		file_handler.setFormatter(formatter)

		# register the file handler for the thread-specific logger
		logger.addHandler(file_handler)

		t = threading.Thread(target=worker, args=(datatypes[i],logger,))
		t.start()




			   
			  
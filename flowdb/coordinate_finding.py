import csv
import requests

with open('locations.csv', 'rb') as csvFile:
	with open('coordinates.csv', 'wb') as writeFile:
		dataReader = csv.reader(csvFile, delimiter=',', quotechar='"')
		dataWriter = csv.writer(writeFile, delimiter=',', quotechar='"')
		for row in dataReader:
			location = row[0]
			new_location = ""
			while len(location) != 0:
				index = str.find(location, " ")
				new_location = new_location + "+" + location[:index]
				location = location[index + 1:]
			new_address = new_location[1:] + ",+Ithaca,+NY"
			web = "https://maps.googleapis.com/maps/api/geocode/json?address=" + new_address + "&sensor=false"
			resp = requests.get(web)
			json_resp = resp.json()
			lat = json_resp["results"][0]["geometry"]["location"]["lat"]
			longitude = json_resp["results"][0]["geometry"]["location"]["lng"]
			dataWriter.writerow([row[0], lat, longitude])
		
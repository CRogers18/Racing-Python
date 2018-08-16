import requests
from xlrd import open_workbook
from xlwt import Workbook
from bs4 import BeautifulSoup

result = open("raceData.txt", "a")

pg_links = []
errors = []

for year in range(1998, 2019):

	for month in range(2, 11):

		url = "https://www.dragracecentral.com/SeriesIndex.asp?Series=NHRA-SUMMIT&Filter=Year" + str(year) + "&EventFilter=&Month=" + str(month)
		page_return = requests.get(url)

		print("Getting: " + url + "\n")

		if(page_return.status_code == 200):

			soup = BeautifulSoup(page_return.text, 'html.parser')
			links = soup.find_all("a")

			for l in links:

				if "Stock Eliminator" in l.text and len(l.text) < 200:
						if "Qualifying" in l.text:
			 				pg_links.append(l['href'])

				if len(l.text) > 200:
			 		errors.append(l)

i = 0
count = len(pg_links)

for l in pg_links:
	
	url = "https://www.dragracecentral.com/" + str(l)

	page_return = requests.get(url.rstrip())

	if(page_return.status_code == 200):

		soup = BeautifulSoup(page_return.text, 'html.parser')
	
		timestamp = soup.find_all("span")
		
		runOnce = True

		for item in timestamp:

			if "datetime" in str(item):
				result.write(item.text)

			if "storylocation" in str(item):
				result.write("\n" + item.text)

			if "storytitle" in str(item) and runOnce:
				result.write(item.text)
				runOnce = False

		data = soup.find("p")
#		print(data.text)
		if data is not None:
			result.write(data.text)

		result.flush()
		result.write("\n\n=====================================================================================\n\n")
		i += 1
		print("Progress: " + str( (i / count) * 100 ) + "%")  

	else:
		print("bad response")

result.write("ERRORS: \n")
for err in errors:

	result.write(str(err))
	result.flush()

result.close()
		
#	wb = Workbook()	
#	testSheet  = wb.add_sheet('Test')

#	i = 0

#	for lineData in data.text.splitlines():

#		j = 0

#		for splitData in lineData.split(" "):
#			print(splitData)
#			testSheet.write(i, j, str(splitData))
#			j += 1

#		i += 1

#	wb.save("uhh.xls")
#	print("all good")


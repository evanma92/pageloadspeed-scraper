import urllib
import json
import csv
import pandas
import datetime

urls = ['https://www.sensodyne.com.ph',
		'https://www.hagashimiru.jp',
		'https://www.sensodyne.com.au',
		'https://www.sensodyne.in',
		'http://www.panadol.com.sg',
		'https://www.voltaren.co.id']

api_url = 'https://www.googleapis.com/pagespeedonline/v1/runPagespeed?url='

for url in urls:

	brand = url.split(".")[1]
	country = url[-2:]

	date_today = datetime.datetime.today().strftime('%Y-%m-%d')
	url_to_send = api_url + url

	print("Getting results for %s..." % url)
	results = json.loads(urllib.urlopen(url_to_send).read())
	formatted_results = results['formattedResults']['ruleResults']

	print("Writing results to CSV...")
	df = pandas.DataFrame.from_dict(formatted_results, orient='index')
	df.to_csv("%s_%s_performance_analysis_%s.csv" % (brand, country, date_today))
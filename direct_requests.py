import requests
import time
import csv
import datetime
from threading import Timer
import os.path


class Results():
	"""
	Class to store results
	"""

	def __init__(self, url):

		# data to store
		self.date = datetime.datetime.today().strftime('%Y-%m-%d')
		self.country = url[-2:] # gets last two characters of the url

		self.data = {'url': url}

		self.brand = url.split(".")[1]

		self.location_to_id = {'au': '3',
							   'nz': '3',
							   'in': '5',
							   'pk': '5',
							   'bd': '5',
							   'lk': '5',
							   'hk': '7',
							   'cn': '7',
							   'jp': '7',
							   'kr': '7',
							   'my': '7',
							   'id': '7',
							   'th': '7',
							   'vn': '7',
							   'sg': '7'}

		self.pagespeed_score = 0
		self.fully_loaded_time = 0
		self.dom_content_loaded_time = 0
		self.redirect_duration = 0
		self.dom_interactive_time = 0

		# data to access GT Metrix API
		self.api_url = 'https://gtmetrix.com/api/0.1/test'
		self.username = 'evan.x.asavaaree@gsk.com'
		self.api_key = 'e4bd074d80a2a8adf170a5f005b8329b'
		self.auth = (self.username, self.api_key)

		# to retrieve results from GT Metrix
		self.test_id = ''
		self.poll_state_url = ''


	def __str__(self):
		return "url: %s,\
				\nbrand: %s\
				\ncountry: %s,\
				\npagespeed_score: %s,\
				\nfully_loaded_time: %s" % (self.data['url'],
											self.brand,
			   								self.country,
			   								self.pagespeed_score,
			   								self.fully_loaded_time)


	def __iter__(self):
		return iter([self.date, self.brand, self.data['url'], 
					 self.country, self.pagespeed_score, 
					 self.fully_loaded_time, self.dom_content_loaded_time,
					 self.redirect_duration, self.dom_interactive_time])


	def assign_country_id(self):
		self.data['location'] = self.location_to_id[self.country]


	def send_data_to_gtmetrix(self):
		self.assign_country_id

		try:
			response = requests.post(self.api_url, data=self.data, auth=self.auth, timeout=5)
		except:
			print("Request Timeout, trying again...")
			response = requests.post(self.api_url, data=self.data, auth=self.auth, timeout=5)

		response = response.json()

		self.test_id = response['test_id']
		self.poll_state_url = response['poll_state_url']

		return response


	def get_result_from_gtmetrix(self):

		response = requests.get(self.poll_state_url, auth=self.auth)
		status = response.json()['state']

		# If we don't get a response, keep sending a get request
		while (status != 'completed'):
			print("waiting for result for %s..." % self.data['url'])
			try:
				response = requests.get(self.poll_state_url, auth=self.auth, timeout=10)
			except:
				print("Request Timeout, trying again...")
				pass
			status = response.json()['state']

			if status == 'error':
				raise ValueError('URL likely has a typo')

			print(status)
			time.sleep(1)

		print("Analysis for %s done" % self.data['url'])
		response = response.json()
		results = response['results']
		print(results)
		self.save_results(results)


	def save_results(self, results):
		"""
		:param: results - results from getting data from gtmetrix
		"""

		self.pagespeed_score = results['pagespeed_score']
		self.fully_loaded_time = results['fully_loaded_time']
		self.dom_content_loaded_time = results['dom_content_loaded_time']
		self.redirect_duration = results['redirect_duration']
		self.dom_interactive_time = results['dom_interactive_time']

urls = ['https://www.sensodyne.com.ph',
		'https://www.hagashimiru.jp',
		'https://www.sensodyne.com.au',
		'https://www.sensodyne.in',
		'http://www.panadol.com.sg',
		'https://www.voltaren.co.id']


def get_pageload_performance():
	
	# instantiate list of result objects
	# where each object contains website performance data for each website

	website_results = [Results(u) for u in urls]

	filename = 'website_performance.csv'

	file_exists = os.path.isfile(filename)
	print("Does the file exist: %s" % file_exists)

	with open(filename, 'ab') as csv_file:
		wr = csv.writer(csv_file, delimiter=',')

		headers = ["Date", "Brand", "Hostname", "Country", 
		 		   "Page Speed Score", "Fully Loaded Time", "DOM Content Loaded Time",
		 		   "Redirect Duration", "DOM Interactive Time"]

		if not file_exists:
			wr.writerow([h for h in headers])

		for w in website_results:
			w.send_data_to_gtmetrix()
			w.get_result_from_gtmetrix()

			wr.writerow(list(w))


start_time = time.time()
i = 0
while True:
	print "Iteration %s" % (i + 1)
	get_pageload_performance()
	time.sleep(300.0 - ((time.time() - start_time) % 300.0))
	i = 1+1
	





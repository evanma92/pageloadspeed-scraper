import urllib
import json
import csv
import pandas
import datetime

urls = ['flixonase.com.cn',
'scottskids.com/id',
'aquafresh.jp',
'growthplus.horlicks.in',
'breatheright.jp',
'proteinplus.horlicks.in',
'oats.horlicks.in',
'physiogel.com/sg',
'horlicks.com.bd',
'japan.biotene.com',
'voltaren.co.nz',
'biotene.com.au',
'scottskids.com/my',
'kamutect.jp',
'lite.horlicks.in',
'mydenturecare.cn',
'scottskids.com/sg',
'zovirax.com.au',
'crocin.com', 
'mydenturecare.com/ko-kr',
'scottskids.com/ph',
'physiogel.com/vn',
'lamisil.com.hk',
'sensodyne.com.pk',
'mydenturecare.com/zh-hk',
'horlicks.com.my',
'sensodyne.com.bd',
'scottskids.com/hk',
'physiogel.com/ph',
'horlicks.com.sg',
'parodontax.co.th',
'flixonase.com.au',
'aquafresh.com.vn',
'mydenturecare.com/en-ph',
'macleans.co.nz',
'cardiaplus.horlicks.in',
'lamisil.com.tw',
'mydenturecare.com/zh-tw',
'ostocalcium.com',
'physiogel.com/th',
'panadol.com.sg',
'otrivin.co.in',
'flixonase.co.nz',
'panadol.lk',
'panadol.co.th',
'sensodyne.lk',
'zovirax.co.nz',
'lamisil-at.jp',
'physiogel.hk',
'sinecod.com.ph',
'physiogel.com/my',
'panadol.com.au',
'voltaren.com.au',
'sensodyne.com.au',
'osteoactive.com.au',
'sensodyne.co.nz',
'panadol.co.nz',
'sensodyne.cn',
'physiogel.com/hk',
'panadol.com.hk',
'sensodyne.com.hk',
'sensodyne.com.tw',
'parodontax.com.tw',
'parodontax.com.hk',
'mydenturecare.com/zh-hk',
'boostenergy.com',
'eno.co.in',
'horlicks.in',
'junior.horlicks.in',
'sensodyne.in',
'mothers.horlicks.in',
'women.horlicks.in',
'mydenturecare.com/ja-jp',
'hagashimiru.jp',
'sensodyne.co.kr',
'sensodyne.co.id',
'panadol.co.id',
'sensodyne.com.my',
'sensodyne.com.ph',
'sensodyne.com.sg',
'sensodyne.co.th',
'sensodyne.com/vn',
'panadol.com.vn']



api_url = 'https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url='
url_prefix = 'http://www.'

suggested_fixes = {}

for url in urls:

	url = url_prefix + url
	brand = url.split(".")[1]
	if 'ostocalcium' in url:
		country = 'in'
	else:
		country = url[-2:]

	suggested_fixes[url] = {}
	suggested_fixes[url]['Brand'] = brand
	suggested_fixes[url]['Market'] = country

	date_today = datetime.datetime.today().strftime('%Y-%m-%d')
	url_to_send = api_url + url

	print("Getting results for %s..." % url)
	results = json.loads(urllib.urlopen(url_to_send).read())

	# print("results: %s" % results)
	formatted_results = results['formattedResults']['ruleResults']

	keys = formatted_results.keys()

	for key in keys:
		element_to_optimize = formatted_results[key]['localizedRuleName']
		rule_impact = formatted_results[key]['ruleImpact']
		suggested_fixes[url][element_to_optimize] = rule_impact

print("Writing results to CSV...")
df = pandas.DataFrame.from_dict(suggested_fixes, orient='index')
df.to_csv("websites_suggested_fixes_%s.csv" % date_today)
import requests
import sys

word = sys.argv[1].lower()
url = 'http://dict-co.iciba.com/api/dictionary.php?key=100113A76C05A2D043654247C29BDF50&type=json&wA='+word
json = requests.get(url).json()
print('The word you search is :',word)
print()
print('results: ')
print(json)
for d in json['symbols'][0]['parts'][0]['means']:
	print(d['word_mean'])


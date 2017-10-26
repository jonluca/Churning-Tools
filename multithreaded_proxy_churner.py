import itertools
import random
import threading

import requests
from fake_useragent import UserAgent

ua = UserAgent()

# Update this with 20 - 100 proxies from https://free-proxy-list.net/ on every run
# If your URL requires https, make sure you filter proxies on whether they support it
list_of_proxies = ["IP Address:Port", "190.0.0.174:8080",
                   "114.142.146.114:3128", "176.31.174.1:9999",
                   "164.160.142.60:53281", "162.243.22.39:80",
                   "103.252.163.76:80", "13.78.125.167:8080",
                   "110.77.201.53:52335", "45.77.119.206:8118",
                   "190.38.82.63:52335", "45.6.216.66:3128",
                   "61.7.190.130:52335", "90.150.87.130:3128",
                   "77.104.250.236:53281", "35.161.196.69:3128",
                   "179.165.106.37:8080", "185.42.223.194:3128",
                   "110.77.177.201:52335", "159.192.226.35:52335",
                   "145.239.80.105:3128", "74.208.131.36:1080",
                   "130.211.132.149:3128", "110.77.177.119:52335",
                   "52.186.124.212:3128", "91.222.222.60:3128",
                   "5.196.189.50:8080", "89.236.17.106:3128",
                   "137.74.254.198:3128", "35.196.41.101:80",
                   "153.149.162.121:3128", "178.170.185.171:53281",
                   "110.77.239.220:52335", "137.74.163.137:3128",
                   "170.239.39.105:8080", "110.77.186.5:52335",
                   "216.56.48.118:9000", "119.42.85.194:52335",
                   "35.161.5.60:3128", "42.116.18.180:53281",
                   "110.77.188.160:52335", "110.77.213.203:52335",
                   "61.7.181.183:52335", "52.37.255.36:3128",
                   "177.159.252.218:8080", "189.111.253.20:3128",
                   "200.123.50.43:53281", "154.72.74.82:53281",
                   "110.77.177.24:52335", "52.11.133.220:80",
                   "198.50.219.232:8080", "14.142.167.178:3128",
                   "165.84.167.54:8080", "94.247.61.204:8080",
                   "178.216.34.165:53281", "70.35.197.31:1080",
                   "36.67.86.253:62225", "195.154.163.181:3128",
                   "116.72.50.122:3128", "104.236.48.95:3128",
                   "103.74.246.113:52305", "218.54.201.166:8080",
                   "110.77.212.21:52335", "137.74.254.242:3128",
                   "117.4.246.95:8080", "14.102.46.133:53005",
                   "177.128.156.135:52335", "54.64.237.2:60088",
                   "190.184.200.182:53281", "62.182.207.26:53281",
                   "191.252.111.73:3128", "46.151.145.4:53281",
                   "191.102.122.3:65301", "181.193.60.194:53281",
                   "110.77.232.94:52335", "69.144.49.11:8080",
                   "49.48.50.240:8080", "103.74.245.112:65301",
                   "177.128.157.162:52335", "46.151.253.17:53281",
                   "190.44.84.131:53281", "94.41.201.209:8080",
                   "50.233.0.195:8888", "201.16.197.149:3128",
                   "186.227.8.21:3128", "213.163.72.234:80",
                   "110.77.232.204:52335", "110.77.240.30:51205",
                   "186.46.156.202:65309", "185.61.254.53:53281",
                   "145.255.28.218:53281", "91.214.62.168:53281",
                   "138.185.246.204:52305", "36.255.134.12:51205",
                   "45.6.65.179:65309", "110.77.232.198:52335",
                   "110.77.210.128:52335", "138.185.245.19:52335",
                   "61.7.177.97:52335", "35.196.254.190:80",
                   "138.185.245.16:52335"]

# Globals
proxy = list_of_proxies[0]
connectionPerSec = 50
prefix = "cap_one"

# Useful combinations
num = '0123456789'
a_z = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numAZ = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# URL parameters
barc_front = "https://www.barclaycardus.com/apply/Landing.action?campaignId="
boa_front = "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=c&campaignid=402"
cap_front = "https://applynow.capitalone.com/?productId="

barc_end = "&cellNumber="
boa_end = "&productoffercode=PS&locale=en_US"

lines = []
current_line = 0


def generate_boa_urls():
	for permutation in map(''.join, itertools.product(num, repeat=4)):
		# for (b) in itertools.imap(''.join, itertools.product(numAZ, repeat=2)):
		line = boa_front
		line += permutation
		line += boa_end
		lines.append(line)


def generate_cap_one():
	for permutation in map(''.join, itertools.product(num, repeat=4)):
		# for (b) in itertools.imap(''.join, itertools.product(numAZ, repeat=2)):
		line = cap_front
		line += permutation
		lines.append(line)


# Creates all URL combinations based on parameters above and stores them in a lines global var
def generate_barclay_urls():
	for (a) in map(''.join, itertools.product(num, repeat=4)):
		# for (b) in itertools.imap(''.join, itertools.product(numAZ, repeat=2)):
		for (cell) in map(''.join, itertools.product(num, repeat=1)):
			line = barc_front
			line += a
			line += barc_end
			line += cell
			lines.append(line)


# Create file locks
valid_url_file_lock = threading.Lock()
invalid_url_file_lock = threading.Lock()


# Often times, the script will need to be interrupted midway through. This will remove all invalid from the testing lines
# Pretty fast (roughly 20s to check 100,000 urls)
def remove_completed():
	try:
		with open("logs/" + prefix + "_invalid.txt") as completed:
			for line in completed:
				temp_line = line[5:]
				if temp_line.rstrip("\n") in lines:
					lines.remove(temp_line.rstrip("\n"))
	except:
		pass


# Write a valid url to file
def write_valid_url(res):
	valid_url_file_lock.acquire()  # thread stops at this line until it can obtain valid_url_file_lock

	with open("logs/" + prefix + "_valid.txt", "a") as myfile:
		myfile.write(res)
		myfile.write('\n')
	valid_url_file_lock.release()


# Writes an invalid url to file
def write_invalid_url(ret):
	invalid_url_file_lock.acquire()  # thread stops at this line until it can obtain valid_url_file_lock

	with open("logs/" + prefix + "_invalid.txt", "a") as myfile:
		myfile.write(ret)
		myfile.write('\n')
	invalid_url_file_lock.release()


def retry(ret):
	invalid_url_file_lock.acquire()  # thread stops at this line until it can obtain valid_url_file_lock

	with open("logs/" + prefix + "_retry.txt", "a") as myfile:
		myfile.write(ret)
		myfile.write('\n')
	invalid_url_file_lock.release()


def retry_urls():
	with open("logs/" + prefix + "_retry.txt") as myfile:
		for line in myfile:
			lines.append(line)


def get_url():
	global current_line
	current_line = current_line + 1
	if current_line >= len(lines):
		return False
	return lines[current_line]


def generate_req(reqSession):
	headers = {"Connection": "close", 'User-Agent': ua.random}
	proxy = list_of_proxies[0]

	while True:
		# Get the next URL
		url = get_url()
		if not url:
			break

		# If it fails for any reason, add it to the retry list
		try:
			response = reqSession.get(url, headers=headers, proxies={"http": proxy},
			                          allow_redirects=True)
		except:
			retry(url)
		print('Completed url: ' + url, end='\r')

		# In case we get ratelimited, set up a new proxy and add file to retry
		if response.status_code == 403:
			random_proxy = random.randint(0, len(list_of_proxies) - 1)
			proxy = list_of_proxies[random_proxy]
			retry(url)
			continue

		# This part needs to change based on what company you're scrpaing. For Barclays, valid app links will include the following in the header
		if response.status_code > 400:
			write_invalid_url(url)
			continue
		write_valid_url(url)


def main():
	generate_cap_one()
	remove_completed()

	# Uncomment this to only check the ones that need to be retried
	# retry_urls()


	# generate threads based on conccurent connections global
	for cnum in range(connectionPerSec):
		s1 = requests.session()
		th = threading.Thread(target=generate_req, args=(s1,),
		                      name='thread-{:03d}'.format(cnum), )
		th.start()

	for th in threading.enumerate():
		if th != threading.current_thread():
			th.join()


if __name__ == '__main__':
	main()

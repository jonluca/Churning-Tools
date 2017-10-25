import random
import threading
import requests
import itertools
from fake_useragent import UserAgent

ua = UserAgent()

# Update this with 20 - 100 proxies from https://free-proxy-list.net/ on every run
# If your URL requires https, make sure you filter proxies on whether they support it
list_of_proxies = ["210.212.73.61:80", "35.161.5.60:3128", "203.74.4.3:80", "204.12.155.204:3128", "203.74.4.6:80", "117.4.246.95:8080", "203.74.4.4:80", "110.78.148.68:52305", "46.229.136.202:8080", "149.255.154.4:8080", "203.74.4.1:80", "163.172.217.103:3128", "109.71.181.234:53281", "189.206.107.6:8080", "89.236.17.106:3128", "189.111.253.20:3128", "212.117.19.215:62225", "203.74.4.2:80", "203.146.82.253:3128", "80.83.20.14:80", "203.153.113.226:52335", "198.50.219.232:8080", "115.79.43.156:8888", "185.42.223.194:3128", "203.74.4.5:80", "195.154.42.249:3128", "45.32.19.109:3128", "52.186.124.212:3128", "213.136.89.121:80", "58.26.10.67:8080", "62.255.12.3:80", "213.136.77.246:80", "203.74.4.7:80", "45.77.136.105:80", "62.182.207.26:53281", "171.101.236.116:3128", "45.6.216.66:3128", "143.0.188.26:80", "203.74.4.0:80", "47.91.235.15:80"]

# Globals
proxy = list_of_proxies[0]
connectionPerSec = 50

# Useful combinations
num = '0123456789'
a_z = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numAZ = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# URL parameters
front = "https://www.barclaycardus.com/apply/Landing.action?campaignId="
end = "&cellNumber="
lines = []
current_line = 0


# Creates all URL combinations based on parameters above and stores them in a lines global var
def generate_urls():
	for (a) in map(''.join, itertools.product(num, repeat=4)):
		# for (b) in itertools.imap(''.join, itertools.product(numAZ, repeat=2)):
		for (cell) in map(''.join, itertools.product(num, repeat=1)):
			line = front
			line += a
			line += end
			line += cell
			lines.append(line)


# Create file locks
valid_url_file_lock = threading.Lock()
invalid_url_file_valid_url_file_lock = threading.Lock()


# Often times, the script will need to be interrupted midway through. This will remove all invalid from the testing lines
# Pretty fast (roughly 20s to check 100,000 urls)
def remove_completed():
	with open("logs/invalid.txt") as completed:
		for line in completed:
			temp_line = line[5:]
			if temp_line.rstrip("\n") in lines:
				lines.remove(temp_line.rstrip("\n"))


# Write a valid url to file
def write_valid_url(res):
	valid_url_file_lock.acquire()  # thread bvalid_url_file_locks at this line until it can obtain valid_url_file_lock

	with open("logs/valid.txt", "a") as myfile:
		myfile.write(res)
		myfile.write('\n')
	valid_url_file_lock.release()


# Writes an invalid url to file
def write_invalid_url(ret):
	invalid_url_file_valid_url_file_lock.acquire()  # thread bvalid_url_file_locks at this line until it can obtain valid_url_file_lock

	with open("logs/invalid.txt", "a") as myfile:
		myfile.write(ret)
		myfile.write('\n')
	invalid_url_file_valid_url_file_lock.release()


def retry(ret):
	invalid_url_file_valid_url_file_lock.acquire()  # thread bvalid_url_file_locks at this line until it can obtain valid_url_file_lock

	with open("logs/retry.txt", "a") as myfile:
		myfile.write(ret)
		myfile.write('\n')
	invalid_url_file_valid_url_file_lock.release()


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
			response = reqSession.get(url, headers=headers, proxies={"http": proxy}, allow_redirects=False)
		except:
			retry(url)
		print('Completed url: ' + url, end='\r')

		# This part needs to change based on what company you're scrpaing. For Barclays, valid app links will include the following in the header
		if "Secure Credit Card Application" not in response.text:
			write_invalid_url(url)
			continue
		# In case we get ratelimited, set up a new proxy and add file to retry
		if response.status_code == 429:
			random_proxy = random.randint(0, len(list_of_proxies))
			proxy = list_of_proxies[random_proxy]
			retry(url)
			continue
		write_valid_url(url)


def main():
	generate_urls()
	remove_completed()

	proxy = list_of_proxies[0]
	current_line = 0

	# generate threads based on conccurent connections global
	for cnum in range(connectionPerSec):
		s1 = requests.session()
		th = threading.Thread(target=generate_req, args=(s1,), name='thread-{:03d}'.format(cnum), )
		th.start()

	for th in threading.enumerate():
		if th != threading.current_thread():
			th.join()


if __name__ == '__main__':
	main()

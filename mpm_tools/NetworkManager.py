import sys
import requests
import json
import ast
import git 
from progress.bar import ChargingBar



class Progress(git.remote.RemoteProgress):
	def update(self, op_code, cur_count, max_count=None, message=''):
		bar = ChargingBar('Processing', max=100)
		for i in range(0, op_code):
			bar.next()
		bar.finish()
		#print ('downloading ', op_code, cur_cou	nt, max_count, message)



class NetworkManager:

	def downloadFile(self, url, fileName):
		with open(fileName, 'wb') as f:
			response = requests.get(url, stream=True)
			total = response.headers.get('content-length')
			if total is None:
				f.write(response.content)	
			else: 
				downloaded = 0
				total = int(total)
				for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
					downloaded += len(data)
					f.write(data)
					done = int(50*downloaded/total)
					sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
					sys.stdout.flush()

		sys.stdout.write('\n')			

		#sys.stdout.write('\n')
		# return request

	def getWebData(self, url):
		response = requests.get(url, allow_redirects=True)
		# print(type(response.text))
		# remote_data = json.dumps(response.text)
		remote_data = ast.literal_eval(str(response.text))
		return remote_data

	def gitClone(self, gitUrl, repoDir):
		try:
			git.Repo.clone_from(gitUrl, repoDir, progress=Progress())
			return True
		except Exception as e:
			return False
			print("Somehting went wrong. maybe the -d parameter contains an exsisting value or is not set")

		
	def readFileFromUrl(self, url):
		try:
			f = requests.get(url)
			return str(f.text)
		except Exception as e:
			print(e)
			return False


		
		

			
			
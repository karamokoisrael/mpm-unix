import uuid

class Tools:

	def perfect_array(self, array):
		new_array = []
		for i in array:
			if not i in new_array:
				new_array.append(i)

 		
		return new_array

	def in_json_array(self, elem, key, array):
		result = [False]
		count = 0
		for i in array:
			if elem in i[key]:
				result = [True, count]

			count+=1

		return result

	def combine_arrays(self, array1, array2):
		for i in array2:
			if not i in array1: 
				array1.append(i)
		return array1	

	
	def generateSessionId(self):
		return str(uuid.uuid1())	
			

				
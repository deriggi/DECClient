from http.client import HTTPSConnection
import base64
import json
from io import StringIO
import urllib

def constructQuery(term, format):
	""" builds the encoded query for the API call

	Args
		term: 	the query string
		format: the response format, CSV, JSON, XML...

	Returns
		api_call: the url for the response  

	"""
	baseUrl = "https://dec.usaid.gov/api/qsearch.ashx?"
	encoded = str(base64.b64encode(term))
	encoded = encoded[2:len(encoded)-1]
	encoded = urllib.parse.urlencode({'q':encoded})

	print("encoded {0}".format(str(encoded)))

	api_call = baseUrl  + str(encoded) + "&rtype=" + format
	print(api_call)
	return api_call

def makeDecCall(path):
	res_obj = makeGetRequest(path)
	res_obj[0]

def makeGetRequest(url):
	start_index = url.find("://")+3;
	stem_index = url.find("/", start_index) 
	base = url[start_index:stem_index]
	stem = url[stem_index:]
	filename = url[url.rfind("/")+1:] 
	print("base: " + base)
	print("stem: " + stem)

	h1 = HTTPSConnection(base);
	h1.request("GET", stem)
	res = h1.getresponse()


	print("res status: {0}".format(res.status))
	data = res.read();
	h1.close()
	return (data, filename);

def saveResponse(data, filename):
	pdf_bytes = bytearray(data)
	out_file = open(filename, "wb")
	out_file.write(pdf_bytes)
	out_file.close();

## downloading a thing from the web
# res_obj = makeGetRequest("http://pdf.usaid.gov/pdf_docs/PNADY390.pdf")
# saveResponse(res_obj[0], res_obj[1])

## calling dec api
search_string = input("please enter a query for the Development Experience Clearninghouse: ")
dec_response = makeGetRequest(constructQuery(bytearray(search_string, 'utf-8'), "JSON"))
io = StringIO( dec_response[0].decode('utf-8') )
dec_obj = json.load(io)
print("{0} records found!".format(dec_obj['RecordsFound']));


file_count = 0
for record in dec_obj['Records']:

	for i in record['File']['value']:
		file_count = file_count + 1;
		res = makeGetRequest(i)
		filename = res[1]
		if filename.rfind('.pdf') != len(filename) - 4:
			filename = 'decFile_' + str(file_count) + '.pdf'
			# saveResponse(res[0], res[1])
		saveResponse(res[0], "downloads/" + filename)

# numRecords = str(len(dec_obj['Records']))

# print ( str(dec_obj['RecordsFound'] )+ " should equal " + numRecords )


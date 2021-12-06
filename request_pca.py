import os
import sys
import argparse
import warnings
from configparser import ConfigParser 
from time import gmtime, strftime
import json
import requests

import random
import string


def send_request(args):
	config_file = os.path.join(args.config_path, 'config') 
	credential_file = os.path.join(args.config_path, 'credentials')

	config_region = ConfigParser(allow_no_value=True)
	config_region.read(config_file)

	config_credentials = ConfigParser(allow_no_value=True)
	config_credentials.read(credential_file)

	aws_region = config_region.get('default', 'region')
	aws_access_key_id = config_credentials.get('default', 'aws_access_key_id')
	aws_secret_access_key = config_credentials.get('default', 'aws_secret_access_key')

	# RESTful 
	project_name_updated = 'data/' + args.project_name + '-' + strftime("%Y-%m-%d-%H-%M-%S%z", gmtime())

	output_model_dir =  project_name_updated + "/output" 
	output_data_dir =  project_name_updated + "/output_data" 
	output_file = "result.npy"  # which is fixed

	# check if the args.PCA_component is a float between 0 and 1 or an integer.
	if '.' in args.PCA_component:	
		float_converted = float(args.PCA_component)	
		if float_converted > 1:
			print ('The PCA_component is automatically set to 0.9 since the input was bigger than 1.')
			checked_value = 0.9
		elif float_converted < 0:
			print ('The PCA_component is automatically set to 0.9 since the input was smaller than 0.')
			checked_value = 0.9
		else:
			checked_value = float_converted
	else:	
		checked_value =  int(args.PCA_component)


	data = {}	
	data['aws_access_key_id'] = aws_access_key_id 
	data['aws_secret_access_key'] = aws_secret_access_key
	data['bucket_name'] = args.bucket_name
	data['region'] = aws_region
	data['input_file'] = args.input_file
	data['output_model_dir'] = output_model_dir
	data['output_data_dir'] = output_data_dir
	data['output_file'] = output_file
	data['csv_encoding'] = args.csv_encoding
	data['PCA_component'] = checked_value

	# refer to this
	# https://curl.trillworks.com/#python
	headers = {'Content-Type': 'application/json',}
	url = 'http://' + args.host + ':' + args.port + '/receive'
	response = requests.post(url, headers=headers, data=json.dumps(data))

	print (response)

	if response.status_code == 200:
		print('PCA has been successfully processed!')
	elif response.status_code == 404:
		print('Wrong Request Found.')

	# no longer store credentials
	data['aws_access_key_id'] =  ''.join(random.choice(string.digits+string.ascii_letters) for i in range(24))
	data['aws_secret_access_key'] =  ''.join(random.choice(string.digits+string.ascii_letters) for i in range(24))

	# dump this for other processes
	with open(args.json_prefix + '_pca.json', 'w') as outfile:
		json.dump(data, outfile)

	# flushing
	data.clear()

if __name__ == '__main__':
	warnings.filterwarnings("ignore", category=FutureWarning)

	parser = argparse.ArgumentParser()
	
	# usage
	# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
	parser.add_argument('--json_prefix', type=str, default="this_path")
	parser.add_argument('--config_path', type=str, default="")
	parser.add_argument('--bucket_name', type=str, default="")
	parser.add_argument('--input_file', type=str, default="data/sklearn-ecr-demo-dataset/data_new.csv")  #"data/sklearn-ecr-demo-dataset/data_new.csv"
	parser.add_argument('--project_name', type=str, default="sklearn-pca-AMI-EC2")
	parser.add_argument('--csv_encoding', type=str, default="default")
	parser.add_argument('--PCA_component', type=str, default='0.9')
	parser.add_argument('--host', type=str, default='localhost')
	parser.add_argument('--port', type=str, default="50000")


	args, _ = parser.parse_known_args()

	send_request(args)	
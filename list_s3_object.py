import boto3
session=boto3.session.Session()
bucket_name="test"

s3_cli=session.client(server_name="s3",region_name="us-east-2")

cnt=1
'''
for each_object in s3_cli.list_objects(Bucket=bucket_name)['Content'])
  print(cnt,each_object['Key'])
  cnt=cnt+1
'''
paginator=s3_cli.get_paginator('list_objects')

for each_page in paginator.paginate(Bucket=bucket_name):
  for each_object in each_page['Contents']:
      print(cnt,each_object['key'])
	  cnt=cnt+1

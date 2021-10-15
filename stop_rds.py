import boto3
session=boto3.session.Session()
client=session.client(service_name="rds",region_name="eu-central-1")
#f_bkp={"Name":"tag:stop","Values":["yes"]}
Key='stop'
Value='yes'
response = client.describe_db_instances()
for i in response['DBInstances']:
   db_arn = i['DBInstanceArn']
   response = client.list_tags_for_resource(ResourceName=i['DBInstanceArn'])
   for tag in response['TagList']:
      if tag['Key'] == str(Key) and tag['Value'] == str(Value):
        db_instance_name = i['DBInstanceIdentifier']
        db_status = i['DBInstanceStatus']
        print (db_instance_name,db_status)
        if db_status == 'available':
          print("shutting down %s " % db_instance_name)
          client.stop_db_instance(DBInstanceIdentifier= db_instance_name)
        else:
          print("The database is " + db_status + " status!")

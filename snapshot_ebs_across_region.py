import boto3
session=boto3.session.session()
ec2_client=session.client(service_name="ec2", region_name="us-east-1")
all_region=[]
for each_region in ec2.client.describe_region()['Regions']:
   all_regions.append(each_region.get('RegionName'))
for each_region in all_regions:
   print("working on{}".format(each_region))
   ec2_client=session.client(service_name="ec2", region_name=each_region)
   list_of_volids=[]
   f_prod_bkp={'Name':'tag:Prod','Values':['backup','Backup']}
   paginator = ec2_client.get_paginator(describe_volumes)
   for each_page in paginator.paginate(Filters=[f_prod_bkp])
      for each_vol in each_page['Volumes']
	     list_of_volids.append(each_vol['VolumeId'])
	print ("The list of volds are {}".format(list_of_volids))
	if bool(list_of_volids)==False:
	   continue
	snapids=[]
	for each_volid in list_of_volids:
	   print ("Taking snap of {}".format(each_volid))
	   res=ec2_client.create_snapshot(
	       Description="Taking snap with Lambda and CW",
		   VolumeId=each_volid,
		   TagSpecifications=[
		   {
			   'ResourceType':'snapshot',
			   'Tags': [
			   {
				   'Key': 'Delete_on',
				   'Value': '90'
			   }]
		   }])
		snapids.append(res.get('SnapshotId'))
    print ("The snap ids are: ", snapids)
    waiter =  ec2_client.get_waiter('snapshot_completed')
    waiter.wait(SnapshotIds=snapids)
    print ("Successfully completed snaps for the volumes of {}".format(list_of_volids))	
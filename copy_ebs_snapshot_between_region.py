import boto3,os,sys
source_region='us-east-1'
dest_region='us-east-2'
session=boto3.session.Session()
ec2_source_client=session.client(service_name="ec2",region_name=source_region)
sts_client=session.client(service_name='sts',region_name='us-east-2')
account_id=sts.client.get_caller_identity().get('Account')
bkp_snap=[]
f_bkp={'Name':'tag:backup','Values':['yes']}
for each_snap in ec2_source_client.describe_snapshot(OwnerIds=[account_id],Filters=[f_bkp].get('Snapshots'))
  bkp_snap.append(each_snap.get['SnapshotID'])
ec2_dest_client=session.client(service_name="ec2",region_name=dest_region)
for ec2_source_snapid in bkp_snap:
  print("Taking backup for id of {} into {}".format(ec2_source_snapid,dest_region))
  ec2_dest_client.copy_snapshot(
     Description='Disator Recovery',
	 SourceRegion=source_region,
	 SourceSnapshotId=ec2_source_snapid
	 )
print ("EBS snapshot copy to destination region is completed")
print ("Modifing tags for the snapshots for which backup is completed")
for each_source_snapid in bkp_snap:
  ec2_source_client.delete_tags(
     Resources=[each_source_snapid],
	 Tags=[
	 {  
	    'Key':'backup',
		'Value':'yes'
	 }])
  print("Creating new tags for {}".format(each_source_snapid))
  ec2_source_client.create_tags(
     Resources=[each_source_snapid],
	 Tags=[
	 {  
	    'Key':'backup',
		'Value':'completed'
	 }])	 
  

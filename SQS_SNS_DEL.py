import boto3
import json
import os
import datetime

sqs = boto3.client('sqs')
s3 = boto3.resource('s3')
client = boto3.client('s3')
dnow=datetime.datetime.now()
rdate=dnow.strftime("%Y%m%d%I")
f_log= "snslog" + rdate
formattxt=f_log + '.txt'
path="D:\\working\\" + formattxt


buckets=[]
for bucket in s3.buckets.all():
    buckets.append(bucket.name)
    
if 'snssqslogbucket' in buckets:
    print('snssqslogbucket is already in S3')
else:
    s3.create_bucket(Bucket='snssqslogbucket',CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})



response = sqs.receive_message(
    QueueUrl='https://sqs.us-east-2.amazonaws.com/707079114649/myQueue',
    AttributeNames=[
        'All',
    ],
    MessageAttributeNames=[
        'All',
    ],
    )
for x in response['Messages']:
    recp_handle=x['ReceiptHandle']
    y=x['Body']
    j= json.loads(y)
    pj=j['Message']
    print(pj)
    file=open(formattxt,'a')
    file.write('\n' + pj)
    s3.Bucket('snssqslogbucket').upload_file(path, formattxt)
    sqs.delete_message(QueueUrl='https://sqs.us-east-2.amazonaws.com/707079114649/myQueue',ReceiptHandle=recp_handle)

    

    
    

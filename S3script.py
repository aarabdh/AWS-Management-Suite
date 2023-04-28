import boto3
from collections import defaultdict 
from typing import *
import threading
import os
from tqdm import tqdm


# get the AWS credentials
def get_aws_credentials():
    access_key_id = input("Enter your AWS access key ID: ")
    secret_access_key = input("Enter your AWS secret access key: ")
    return access_key_id, secret_access_key

# create an S3 client
def get_s3_client(access_key_id, secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                    region_name='ap-south-1')
    return s3

# get all the S3 buckets
def get_s3_buckets(s3):
    buckets = s3.list_buckets()
    buckets = buckets['Buckets']
    print("List of buckets acquired.")
    return buckets

def get_bucket_tags(s3, bucket_name):
    try:
        tags = s3.get_bucket_tagging(Bucket=bucket_name)
        tags = tags['TagSet']
    except:
        tags = []
    return tags

# loop through each bucket and get its tags

# Using multi-threading to speed up the process

def get_s3_bucket_info(buckets, s3):
    print("Starting tag collection.")
    bucket_tags = {}
    def task1():
        i = 0
        while(i<len(buckets)):
            y = get_bucket_tags(s3, buckets[i]['Name'])
            bucket_tags[buckets[i]['Name']] = y
            i+=3

    def task2():
        i = 1
        while(i<len(buckets)):
            y = get_bucket_tags(s3, buckets[i]['Name'])
            bucket_tags[buckets[i]['Name']] = y
            i+=3

    def task3():
        i = 2
        x = (len(buckets) - i)%3-1
        pbar = tqdm(total = len(buckets)-x, desc='Processing Bucket Tags')
        while(i<len(buckets)):
            # print(i, "task3")
            y = get_bucket_tags(s3, buckets[i]['Name'])
            bucket_tags[buckets[i]['Name']] = y
            i+=3
            pbar.update(3)
        pbar.close()
        
        
    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2')
    t3 = threading.Thread(target=task3, name='t3')

    # starting threads
    t1.start()
    t2.start()
    t3.start()

    # wait until all threads finish
    t1.join()
    t2.join()
    t3.join()
    return bucket_tags

def untagged_buckets(bucket_tags):
    untagged_buckets = defaultdict(list)
    for key, value in bucket_tags.items():
        req_tags = ["team", "environment", "project", "maintainer"]
        for i in value:
            if i['Key'] in req_tags:
                req_tags.remove(i['Key'])
        untagged_buckets[key] = req_tags
    return untagged_buckets

def writing_to_csv(untagged_buckets):
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('out/untagged_S3.csv', 'w') as f:
        f.write("S3 Bucket Name, Untagged Tags\n")
        for key in untagged_buckets.keys():
            x = untagged_buckets[key]
            y = ','.join(i for i in x)
            f.write("%s, %s\n"%(key,y))

# main function
def main():
    access_key_id, secret_access_key = get_aws_credentials()
    s3 = get_s3_client(access_key_id, secret_access_key)
    buckets = get_s3_buckets(s3)
    bucket_tags = get_s3_bucket_info(buckets, s3)
    untagged_buckets_ = untagged_buckets(bucket_tags)
    writing_to_csv(untagged_buckets_)

if __name__ == "__main__":
    main()

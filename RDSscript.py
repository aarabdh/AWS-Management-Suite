import boto3
from collections import defaultdict
from typing import *
import threading
import os

# Prompt the user for AWS credentials
def get_aws_credentials():
    access_key_id = input("Enter your AWS access key ID: ")
    secret_access_key = input("Enter your AWS secret access key: ")
    account_id = input("Enter your AWS account ID: ")
    return access_key_id, secret_access_key, account_id

# Create an RDS client object with the provided credentials
def get_rds_client(access_key_id, secret_access_key):
    rds = boto3.client('rds', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                    region_name='ap-south-1')
    return rds

# Call the describe_db_instances() method to get the list of all RDS instances
def get_rds_instances(rds):
    response = rds.describe_db_instances()
    response = response['DBInstances']
    return response

def get_rds_tags(rds, rds_name, account_id):
    final_tags = []
    try:
        tags = rds.list_tags_for_resource(ResourceName=f'arn:aws:rds:ap-south-1:{account_id}:db:{rds_name}')
        tags = tags['TagList']
        for tag in tags:
            final_tags.append(tag['Key'])
    except:
        pass
    return final_tags

def get_rds_instance_info(rds, response, account_id):
    rds_tags = defaultdict(list)
    def task1():
        i = 0
        while(i<len(response)):
            instance_identifier = response[i]
            name = instance_identifier['DBInstanceIdentifier']
            y = get_rds_tags(rds, name, account_id)
            rds_tags[name] = y
            i+=3

    def task2():
        i = 1
        while(i<len(response)):
            instance_identifier = response[i]
            name = instance_identifier['DBInstanceIdentifier']
            y = get_rds_tags(rds, name, account_id)
            rds_tags[name] = y
            i+=3

    def task3():
        i = 2
        while(i<len(response)):
            instance_identifier = response[i]
            name = instance_identifier['DBInstanceIdentifier']
            y = get_rds_tags(rds, name, account_id)
            rds_tags[name] = y
            i+=3
        
        
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
    print("RDS tags fetched successfully.")
    return rds_tags

def untagged_rds_instances(rds_tags):
    untagged_instances = defaultdict(list)
    for key, value in rds_tags.items():
        req_tags = ["team", "environment", "project", "maintainer"]
        for i in value:
            if i in req_tags:
                req_tags.remove(i)
        untagged_instances[key] = req_tags
    return untagged_instances

def writing_to_csv(untagged_instances):
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('out/untagged_RDS.csv', 'w') as f:
        f.write("S3 Bucket Name, Untagged Tags\n")
        for key in untagged_instances.keys():
            x = untagged_instances[key]
            y = ','.join(i for i in x)
            f.write("%s, %s\n"%(key,y))

def main():
    access_key_id, secret_access_key, account_id = get_aws_credentials()
    rds = get_rds_client(access_key_id, secret_access_key)
    response = get_rds_instances(rds)
    rds_tags = get_rds_instance_info(rds, response, account_id)
    untagged_instances = untagged_rds_instances(rds_tags)
    writing_to_csv(untagged_instances)

if __name__ == "__main__":
    main()
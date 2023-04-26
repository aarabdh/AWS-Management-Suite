import boto3
from collections import defaultdict 
from typing import * 

# Prompt the user for AWS credentials
def get_aws_credentials():
    access_key_id = input("Enter your AWS access key ID: ")
    secret_access_key = input("Enter your AWS secret access key: ")
    return access_key_id, secret_access_key

# Create an EC2 client object with the provided credentials
def get_ec2_client(access_key_id, secret_access_key):
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                    region_name='ap-south-1')
    return ec2

# Call the describe_instances() method to get the list of all EC2 instances
def get_ec2_instances(ec2):
    response = ec2.describe_instances()
    return response


# Extract the instance information from the response object
def get_ec2_instance_info(response):
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    return instances

# Check if the instances are tagged with the required tags
def untagged_instances(instances) -> dict:
    untagged_instances = defaultdict(list)
    for instance in instances:
        try:
            instance_tags = [tag['Key'] for tag in instance['Tags']]
            req_tags = ["team", "environment", "project", "maintainer"]
            for tag in req_tags:
                if tag not in instance_tags:
                    untagged_instances[instance['InstanceId']].append(tag)
        except:
            untagged_instances[instance['InstanceId']] = req_tags
    return untagged_instances

# Driver code
def main():
    access_key_id, secret_access_key = get_aws_credentials()
    ec2 = get_ec2_client(access_key_id, secret_access_key)
    response = get_ec2_instances(ec2)
    instances = get_ec2_instance_info(response)
    untagged_instances_ = untagged_instances(instances)
    print("Number of untagged instances: ", len(untagged_instances_), "\n")
    print("List of untagged instances: ")
    for key, value in untagged_instances_.items():
        print(f"instanceID = {key} and tags missing = {value}")

if __name__ == "__main__":
    main()
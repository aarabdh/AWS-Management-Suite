import boto3
from collections import defaultdict 
from typing import *
import threading


# get the AWS credentials
def get_aws_credentials():
    access_key_id = input("Enter your AWS access key ID: ")
    secret_access_key = input("Enter your AWS secret access key: ")
    return access_key_id, secret_access_key

# create an Lambda client
def get_Lambda_client(access_key_id, secret_access_key):
    Lambda = boto3.client("lambda", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                    region_name='ap-south-1')
    return Lambda

# get all the Lambda functions
def get_Lambda_functions(Lambda):
    functions = Lambda.list_functions()
    functions = functions['Functions']
    print("List of functions acquired.")
    return functions

def get_lambda_tags(Lambda, resource_arn):
    final_tags = []
    try:
        tags = Lambda.list_tags_for_resource(Resource=resource_arn)
        tags = tags.get("Tags", {})
        for tag in tags:
            final_tags.append(tag['Key'])
    except:
        pass
    return final_tags

# loop through each function and get its tags

# Using multi-threading to speed up the process

def get_Lambda_function_info(functions, Lambda):
    print("Starting tag collection.")
    function_tags = {}
    def task1():
        i = 0
        while(i<len(functions)):
            y = get_lambda_tags(Lambda, functions[i]["FunctionArn"])
            function_tags[functions[i]['FunctionName']] = y
            i+=3

    def task2():
        i = 1
        while(i<len(functions)):
            y = get_lambda_tags(Lambda, functions[i]["FunctionArn"])
            function_tags[functions[i]['FunctionName']] = y
            i+=3

    def task3():
        i = 2
        # x = (len(functions) - i)%3-1
        # pbar = tqdm(total = len(functions)-x, desc='Processing function Tags')
        while(i<len(functions)):
            # print(i, "task3")
            y = get_lambda_tags(Lambda, functions[i]["FunctionArn"])
            function_tags[functions[i]['FunctionName']] = y
            i+=3
            # pbar.update(3)
        # pbar.close()
        
        
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
    return function_tags

def untagged_functions(function_tags):
    untagged_functions = defaultdict(list)
    for key, value in function_tags.items():
        req_tags = ["team", "environment", "project", "maintainer"]
        for i in value:
            if i['Key'] in req_tags:
                req_tags.remove(i['Key'])
        untagged_functions[key] = req_tags
    return untagged_functions

def writing_to_csv(untagged_functions, path):
    with open(path + '/untagged_Lambda.csv', 'w') as f:
        f.write("Lambda function Name, Untagged Tags\n")
        for key in untagged_functions.keys():
            x = untagged_functions[key]
            y = ','.join(i for i in x)
            f.write("%s, %s\n"%(key,y))

# main function
def main(access_key_id, secret_access_key, path):
    # access_key_id, secret_access_key = get_aws_credentials()
    Lambda = get_Lambda_client(access_key_id, secret_access_key)
    # path = f"./OUT/"
    functions = get_Lambda_functions(Lambda)
    function_tags = get_Lambda_function_info(functions, Lambda)
    untagged_functions_ = untagged_functions(function_tags)
    writing_to_csv(untagged_functions_, path)

if __name__ == "__main__":
    main()

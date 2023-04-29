# AWS-Management-Suite

## EC2 Script

Run this code to get a list of all EC2 instances that do not have the specified tags.

The response will be saved in a CSV file in ./out directory.

## S3 Script

Similarly, this code will get you all S3 buckets and their associated tags. It uses multithreading to speed up the process.

The response will be saved in a CSV file in ./out directory.

## Dependencies

```pip install boto3```
```pip install tqdm```

import boto3
import pytest
from moto import mock_aws


@mock_aws
def test_s3_bucket_creation():
    """Example test: Create an S3 bucket using mocked AWS."""
    s3 = boto3.client('s3', region_name='us-east-1')

    bucket_name = 'test-bucket'
    s3.create_bucket(Bucket=bucket_name)

    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    assert bucket_name in bucket_names


@mock_aws
def test_s3_put_and_get_object():
    """Example test: Put and retrieve an object from S3."""
    s3 = boto3.client('s3', region_name='us-east-1')

    bucket_name = 'test-bucket'
    s3.create_bucket(Bucket=bucket_name)

    test_data = b'{"name": "test", "value": 123}'
    s3.put_object(Bucket=bucket_name, Key='test.json', Body=test_data)

    response = s3.get_object(Bucket=bucket_name, Key='test.json')
    retrieved_data = response['Body'].read()

    assert retrieved_data == test_data

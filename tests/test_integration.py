import boto3
import pytest
import os


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get('RUN_INTEGRATION_TESTS'),
    reason="Integration tests require RUN_INTEGRATION_TESTS=1 and valid AWS credentials"
)
def test_s3_real_bucket_operations():
    """
    Integration test: Test S3 operations against real AWS.

    Requires:
    - AWS credentials configured (via ~/.aws/credentials or environment variables)
    - RUN_INTEGRATION_TESTS=1 environment variable
    - Permissions to create/delete S3 buckets
    """
    s3 = boto3.client('s3', region_name='us-east-1')

    # Use a unique bucket name to avoid conflicts
    import time
    bucket_name = f'test-integration-bucket-{int(time.time())}'

    try:
        # Create bucket
        s3.create_bucket(Bucket=bucket_name)

        # Verify bucket exists
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        assert bucket_name in bucket_names

        # Test put/get object
        test_data = b'{"name": "integration-test", "value": 456}'
        s3.put_object(Bucket=bucket_name, Key='test.json', Body=test_data)

        response = s3.get_object(Bucket=bucket_name, Key='test.json')
        retrieved_data = response['Body'].read()
        assert retrieved_data == test_data

    finally:
        # Cleanup: Delete object and bucket
        try:
            s3.delete_object(Bucket=bucket_name, Key='test.json')
            s3.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            print(f"Cleanup failed: {e}")

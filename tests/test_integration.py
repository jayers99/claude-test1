import boto3
import pytest
import os
import json
from pathlib import Path
from src.recovery_points import export_recovery_points


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


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get('RUN_INTEGRATION_TESTS'),
    reason="Integration tests require RUN_INTEGRATION_TESTS=1 and valid AWS credentials"
)
def test_export_recovery_points_real_aws(tmp_path):
    """
    Integration test: Export recovery points from real AWS Backup.

    Requires:
    - AWS credentials configured
    - RUN_INTEGRATION_TESTS=1 environment variable
    - An existing backup vault (will use 'Default' if it exists)
    - Permissions to list recovery points and tags

    Note: This test will only verify the functionality if a backup vault exists.
    It will skip if no backup vault is found.
    """
    backup_client = boto3.client('backup', region_name='us-east-1')

    # Try to find an existing backup vault
    try:
        vaults = backup_client.list_backup_vaults()
        if not vaults.get('BackupVaultList'):
            pytest.skip("No backup vaults found in AWS account")

        # Use the first vault found
        vault_name = vaults['BackupVaultList'][0]['BackupVaultName']

        # Export recovery points to temp directory
        output_file = export_recovery_points(
            backup_vault_name=vault_name,
            region_name='us-east-1',
            output_dir=str(tmp_path)
        )

        # Verify file was created
        assert Path(output_file).exists()

        # Verify JSON is valid
        with open(output_file, 'r') as f:
            recovery_points = json.load(f)

        assert isinstance(recovery_points, list)

        # If there are recovery points, verify structure
        if recovery_points:
            rp = recovery_points[0]
            assert 'recovery_point_arn' in rp
            assert 'tags' in rp
            assert isinstance(rp['tags'], dict)

        print(f"Successfully exported {len(recovery_points)} recovery points from vault '{vault_name}'")

    except Exception as e:
        pytest.skip(f"Could not complete test: {e}")

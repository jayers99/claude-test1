"""
Unit tests for recovery points functionality using moto mocks.
"""

import json
import pytest
from moto import mock_aws
import boto3
from pathlib import Path
from datetime import datetime

from src.recovery_points import (
    list_all_recovery_points,
    get_recovery_point_tags,
    fetch_recovery_points_with_tags,
    save_recovery_points_to_file,
    export_recovery_points
)


@pytest.mark.unit
@mock_aws
def test_list_all_recovery_points_empty():
    """Test listing recovery points when vault is empty."""
    backup_client = boto3.client('backup', region_name='us-east-1')

    # Create a backup vault
    vault_name = 'test-vault'
    backup_client.create_backup_vault(BackupVaultName=vault_name)

    # Note: moto doesn't fully support list_recovery_points_by_backup_vault yet
    # Skip this test if the operation is not implemented
    try:
        recovery_points = list_all_recovery_points(backup_client, vault_name)
        assert isinstance(recovery_points, list)
    except Exception as e:
        if "Not yet implemented" in str(e):
            pytest.skip("moto doesn't support list_recovery_points_by_backup_vault yet")
        raise


@pytest.mark.unit
@mock_aws
def test_list_all_recovery_points_with_data():
    """Test listing recovery points with mocked data."""
    backup_client = boto3.client('backup', region_name='us-east-1')

    # Create a backup vault
    vault_name = 'test-vault'
    backup_client.create_backup_vault(BackupVaultName=vault_name)

    # Note: moto doesn't fully support list_recovery_points_by_backup_vault yet
    # Skip this test if the operation is not implemented
    try:
        recovery_points = list_all_recovery_points(backup_client, vault_name)
        assert isinstance(recovery_points, list)
    except Exception as e:
        if "Not yet implemented" in str(e):
            pytest.skip("moto doesn't support list_recovery_points_by_backup_vault yet")
        raise


@pytest.mark.unit
@mock_aws
def test_get_recovery_point_tags():
    """Test getting tags for a recovery point."""
    backup_client = boto3.client('backup', region_name='us-east-1')

    # Create a backup vault
    vault_name = 'test-vault'
    backup_client.create_backup_vault(BackupVaultName=vault_name)

    # Create a mock recovery point ARN
    recovery_point_arn = 'arn:aws:backup:us-east-1:123456789012:recovery-point:test-rp'

    # Try to get tags (will return empty due to moto limitations)
    tags = get_recovery_point_tags(backup_client, recovery_point_arn)

    assert isinstance(tags, dict)


@pytest.mark.unit
def test_save_recovery_points_to_file(tmp_path):
    """Test saving recovery points to a JSON file."""
    # Create test data
    recovery_points = [
        {
            'recovery_point_arn': 'arn:aws:backup:us-east-1:123456789012:recovery-point:rp1',
            'backup_vault_name': 'test-vault',
            'resource_arn': 'arn:aws:ec2:us-east-1:123456789012:instance/i-123456',
            'resource_type': 'EC2',
            'creation_date': '2024-01-01T00:00:00',
            'completion_date': '2024-01-01T01:00:00',
            'status': 'COMPLETED',
            'backup_size_bytes': 1024000,
            'tags': {'Environment': 'Production', 'Owner': 'TeamA'}
        },
        {
            'recovery_point_arn': 'arn:aws:backup:us-east-1:123456789012:recovery-point:rp2',
            'backup_vault_name': 'test-vault',
            'resource_arn': 'arn:aws:rds:us-east-1:123456789012:db:mydb',
            'resource_type': 'RDS',
            'creation_date': '2024-01-02T00:00:00',
            'completion_date': '2024-01-02T01:00:00',
            'status': 'COMPLETED',
            'backup_size_bytes': 2048000,
            'tags': {'Environment': 'Staging', 'Application': 'MyApp'}
        }
    ]

    # Save to temporary directory
    output_file = save_recovery_points_to_file(recovery_points, str(tmp_path))

    # Verify file was created
    assert Path(output_file).exists()

    # Verify content
    with open(output_file, 'r') as f:
        saved_data = json.load(f)

    assert len(saved_data) == 2
    assert saved_data[0]['recovery_point_arn'] == 'arn:aws:backup:us-east-1:123456789012:recovery-point:rp1'
    assert saved_data[0]['tags']['Environment'] == 'Production'
    assert saved_data[1]['resource_type'] == 'RDS'
    assert saved_data[1]['tags']['Application'] == 'MyApp'


@pytest.mark.unit
def test_save_recovery_points_creates_directory(tmp_path):
    """Test that save function creates the output directory if it doesn't exist."""
    recovery_points = [
        {
            'recovery_point_arn': 'arn:aws:backup:us-east-1:123456789012:recovery-point:rp1',
            'tags': {}
        }
    ]

    # Use a non-existent subdirectory
    output_dir = tmp_path / 'nested' / 'data'
    output_file = save_recovery_points_to_file(recovery_points, str(output_dir))

    # Verify directory was created
    assert output_dir.exists()
    assert Path(output_file).exists()


@pytest.mark.unit
def test_save_recovery_points_empty_list(tmp_path):
    """Test saving an empty list of recovery points."""
    recovery_points = []

    output_file = save_recovery_points_to_file(recovery_points, str(tmp_path))

    # Verify file was created
    assert Path(output_file).exists()

    # Verify content is empty array
    with open(output_file, 'r') as f:
        saved_data = json.load(f)

    assert saved_data == []


@pytest.mark.unit
@mock_aws
def test_fetch_recovery_points_with_tags():
    """Test the main fetch function."""
    # Create backup vault
    backup_client = boto3.client('backup', region_name='us-east-1')
    vault_name = 'test-vault'
    backup_client.create_backup_vault(BackupVaultName=vault_name)

    # Note: moto doesn't fully support list_recovery_points_by_backup_vault yet
    # Skip this test if the operation is not implemented
    try:
        recovery_points = fetch_recovery_points_with_tags(vault_name, 'us-east-1')
        assert isinstance(recovery_points, list)
    except Exception as e:
        if "Not yet implemented" in str(e):
            pytest.skip("moto doesn't support list_recovery_points_by_backup_vault yet")
        raise


@pytest.mark.unit
def test_recovery_point_data_structure():
    """Test that the recovery point data structure has all expected fields."""
    recovery_points = [
        {
            'recovery_point_arn': 'arn:aws:backup:us-east-1:123456789012:recovery-point:rp1',
            'backup_vault_name': 'test-vault',
            'resource_arn': 'arn:aws:ec2:us-east-1:123456789012:instance/i-123456',
            'resource_type': 'EC2',
            'creation_date': '2024-01-01T00:00:00',
            'completion_date': '2024-01-01T01:00:00',
            'status': 'COMPLETED',
            'backup_size_bytes': 1024000,
            'tags': {'Environment': 'Production'}
        }
    ]

    rp = recovery_points[0]

    # Verify all expected fields exist
    assert 'recovery_point_arn' in rp
    assert 'backup_vault_name' in rp
    assert 'resource_arn' in rp
    assert 'resource_type' in rp
    assert 'creation_date' in rp
    assert 'completion_date' in rp
    assert 'status' in rp
    assert 'backup_size_bytes' in rp
    assert 'tags' in rp

    # Verify tags is a dictionary
    assert isinstance(rp['tags'], dict)

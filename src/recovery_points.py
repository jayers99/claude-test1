"""
AWS Backup Recovery Points Manager

This module provides functionality to:
- List all recovery points from AWS Backup with pagination
- Retrieve tags for each recovery point
- Save recovery point data with tags to a local JSON file
"""

import json
import boto3
from typing import List, Dict, Any
from pathlib import Path


def list_all_recovery_points(backup_client, backup_vault_name: str) -> List[Dict[str, Any]]:
    """
    List all recovery points from a specific backup vault with pagination.

    Args:
        backup_client: boto3 Backup client
        backup_vault_name: Name of the backup vault

    Returns:
        List of recovery point dictionaries
    """
    recovery_points = []
    next_token = None

    while True:
        if next_token:
            response = backup_client.list_recovery_points_by_backup_vault(
                BackupVaultName=backup_vault_name,
                NextToken=next_token
            )
        else:
            response = backup_client.list_recovery_points_by_backup_vault(
                BackupVaultName=backup_vault_name
            )

        recovery_points.extend(response.get('RecoveryPoints', []))

        next_token = response.get('NextToken')
        if not next_token:
            break

    return recovery_points


def get_recovery_point_tags(backup_client, recovery_point_arn: str) -> Dict[str, str]:
    """
    Get all tags for a specific recovery point.

    Args:
        backup_client: boto3 Backup client
        recovery_point_arn: ARN of the recovery point

    Returns:
        Dictionary of tag key-value pairs
    """
    try:
        response = backup_client.list_tags(
            ResourceArn=recovery_point_arn
        )
        return response.get('Tags', {})
    except Exception as e:
        print(f"Error getting tags for {recovery_point_arn}: {e}")
        return {}


def fetch_recovery_points_with_tags(backup_vault_name: str, region_name: str = 'us-east-1') -> List[Dict[str, Any]]:
    """
    Fetch all recovery points with their tags from AWS Backup.

    Args:
        backup_vault_name: Name of the backup vault
        region_name: AWS region (default: us-east-1)

    Returns:
        List of recovery point dictionaries with tags included
    """
    backup_client = boto3.client('backup', region_name=region_name)

    # Get all recovery points
    recovery_points = list_all_recovery_points(backup_client, backup_vault_name)

    # Enrich each recovery point with its tags
    enriched_recovery_points = []
    for rp in recovery_points:
        recovery_point_arn = rp.get('RecoveryPointArn')
        tags = get_recovery_point_tags(backup_client, recovery_point_arn)

        enriched_rp = {
            'recovery_point_arn': recovery_point_arn,
            'backup_vault_name': rp.get('BackupVaultName'),
            'resource_arn': rp.get('ResourceArn'),
            'resource_type': rp.get('ResourceType'),
            'creation_date': rp.get('CreationDate').isoformat() if rp.get('CreationDate') else None,
            'completion_date': rp.get('CompletionDate').isoformat() if rp.get('CompletionDate') else None,
            'status': rp.get('Status'),
            'backup_size_bytes': rp.get('BackupSizeInBytes'),
            'tags': tags
        }
        enriched_recovery_points.append(enriched_rp)

    return enriched_recovery_points


def save_recovery_points_to_file(recovery_points: List[Dict[str, Any]], output_dir: str = './data') -> str:
    """
    Save recovery points data to a JSON file in the specified directory.

    Args:
        recovery_points: List of recovery point dictionaries
        output_dir: Directory to save the file (default: ./data)

    Returns:
        Path to the saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / 'recovery_points.json'

    with open(output_file, 'w') as f:
        json.dump(recovery_points, f, indent=2)

    return str(output_file)


def export_recovery_points(backup_vault_name: str, region_name: str = 'us-east-1', output_dir: str = './data') -> str:
    """
    Main function to export all recovery points with tags to a JSON file.

    Args:
        backup_vault_name: Name of the backup vault
        region_name: AWS region (default: us-east-1)
        output_dir: Directory to save the file (default: ./data)

    Returns:
        Path to the saved file
    """
    recovery_points = fetch_recovery_points_with_tags(backup_vault_name, region_name)
    output_file = save_recovery_points_to_file(recovery_points, output_dir)

    print(f"Exported {len(recovery_points)} recovery points to {output_file}")

    return output_file

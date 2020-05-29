import io
import json
import logging
import oci

from fdk import response

def create_backup(compartment_id):
    signer = oci.auth.signers.get_resource_principals_signer()
    blockStorageClient = oci.core.BlockstorageClient(config={}, signer=signer)
    volume_group_lists = blockStorageClient.list_volume_groups(compartment_id).data
    for volume_group in volume_group_lists:
        details = oci.core.models.CreateVolumeGroupBackupDetails(compartment_id=compartment_id, type="FULL", volume_group_id=volume_group.id)
        blockStorageClient.create_volume_group_backup(details)


def handler(ctx, data: io.BytesIO=None):
    
    try:
        body = json.loads(data.getvalue())
        # name = body.get("name")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))
    
    compartment_id="ocid1.compartment.oc1..aaaaaaaajho77wsetgsyq4oqywzfl6pgw7cu4xnqbtvo3tdyo7uo7cusmsgq"
    create_backup(compartment_id)
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Successfully created Volume Group Backups"}),
        headers={"Content-Type": "application/json"}
    )

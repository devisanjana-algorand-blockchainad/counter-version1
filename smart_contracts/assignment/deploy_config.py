import logging

import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.assignment.assignment_client import (
        AssignmentClient,
    )

    app_client = AssignmentClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )
    counter = app_client.get_counter().return_value
    logger.info(f"Counter value after deployment: {counter}")

    response = app_client.increment()
    logger.info(
        f"Called increment on {app_spec.contract.name} ({app_client.app_id}), "
        f"new counter value: {response.return_value}"
    )

    response = app_client.increment()
    logger.info(
        f"Called increment on {app_spec.contract.name} ({app_client.app_id}), "
        f"new counter value: {response.return_value}"
    )

    response = app_client.increment()
    logger.info(
        f"Called increment on {app_spec.contract.name} ({app_client.app_id}), "
        f"new counter value: {response.return_value}"
    )

    response = app_client.decrement()
    logger.info(
        f"Called decrement on {app_spec.contract.name} ({app_client.app_id}), "
        f"new counter value: {response.return_value}"
    )

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
    
    logger.info(f"Deployed Counter app with app_id: {app_client.app_id}")

    try:
        result = app_client.opt_in_opt_in()
        logger.info(f"Opted in deployer account [{deployer.address}] with result: {result.tx_id}")
    except:
        logger.info(f"Deployer account [{deployer.address}] already opted in")
        
    localState = app_client.get_local_state(deployer.address)
    logger.info(f"Local state for deployer account [{deployer.address}]: {localState.counter}")

    result = app_client.increment()
    logger.info(f"Incremented counter with result: {result.tx_id}")

    localState = app_client.get_local_state(deployer.address)
    logger.info(f"Local state for deployer account [{deployer.address}]: {localState.counter}")

    result = app_client.decrement()
    logger.info(f"Decremented counter with result: {result.tx_id}")

    localState = app_client.get_local_state(deployer.address)
    logger.info(f"Local state for deployer account [{deployer.address}]: {localState.counter}")
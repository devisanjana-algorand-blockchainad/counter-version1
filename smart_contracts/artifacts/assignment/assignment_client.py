# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "increment()void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "decrement()void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "get()uint64": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "opt_in()void": {
            "call_config": {
                "opt_in": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMuYXNzaWdubWVudC5jb250cmFjdC5Bc3NpZ25tZW50LmFwcHJvdmFsX3Byb2dyYW06CiAgICBpbnRjYmxvY2sgMSAwCiAgICBieXRlY2Jsb2NrICJjb3VudGVyIgogICAgY2FsbHN1YiBfX3B1eWFfYXJjNF9yb3V0ZXJfXwogICAgcmV0dXJuCgoKLy8gc21hcnRfY29udHJhY3RzLmFzc2lnbm1lbnQuY29udHJhY3QuQXNzaWdubWVudC5fX3B1eWFfYXJjNF9yb3V0ZXJfXygpIC0+IHVpbnQ2NDoKX19wdXlhX2FyYzRfcm91dGVyX186CiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weTo1CiAgICAvLyBjbGFzcyBBc3NpZ25tZW50KEFSQzRDb250cmFjdCk6CiAgICBwcm90byAwIDEKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBfX3B1eWFfYXJjNF9yb3V0ZXJfX19iYXJlX3JvdXRpbmdAOAogICAgcHVzaGJ5dGVzcyAweDJmYTQ3MzI4IDB4NGI1YmRkZmQgMHg1MGVhODFjYiAweDMwYzZkNThhIC8vIG1ldGhvZCAiaW5jcmVtZW50KCl2b2lkIiwgbWV0aG9kICJkZWNyZW1lbnQoKXZvaWQiLCBtZXRob2QgImdldCgpdWludDY0IiwgbWV0aG9kICJvcHRfaW4oKXZvaWQiCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBfX3B1eWFfYXJjNF9yb3V0ZXJfX19pbmNyZW1lbnRfcm91dGVAMiBfX3B1eWFfYXJjNF9yb3V0ZXJfX19kZWNyZW1lbnRfcm91dGVAMyBfX3B1eWFfYXJjNF9yb3V0ZXJfX19nZXRfcm91dGVANCBfX3B1eWFfYXJjNF9yb3V0ZXJfX19vcHRfaW5fcm91dGVANQogICAgaW50Y18xIC8vIDAKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19faW5jcmVtZW50X3JvdXRlQDI6CiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weTo5CiAgICAvLyBAYWJpbWV0aG9kKCkKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgbm90IE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIG5vdCBjcmVhdGluZwogICAgY2FsbHN1YiBpbmNyZW1lbnQKICAgIGludGNfMCAvLyAxCiAgICByZXRzdWIKCl9fcHV5YV9hcmM0X3JvdXRlcl9fX2RlY3JlbWVudF9yb3V0ZUAzOgogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MTQKICAgIC8vIEBhYmltZXRob2QoKQogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGRlY3JlbWVudAogICAgaW50Y18wIC8vIDEKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fZ2V0X3JvdXRlQDQ6CiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weToxOQogICAgLy8gQGFiaW1ldGhvZCgpCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIG5vdCBOb09wCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgYXNzZXJ0IC8vIGNhbiBvbmx5IGNhbGwgd2hlbiBub3QgY3JlYXRpbmcKICAgIGNhbGxzdWIgZ2V0CiAgICBpdG9iCiAgICBwdXNoYnl0ZXMgMHgxNTFmN2M3NQogICAgc3dhcAogICAgY29uY2F0CiAgICBsb2cKICAgIGludGNfMCAvLyAxCiAgICByZXRzdWIKCl9fcHV5YV9hcmM0X3JvdXRlcl9fX29wdF9pbl9yb3V0ZUA1OgogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MjQKICAgIC8vIEBhYmltZXRob2QoYWxsb3dfYWN0aW9ucz1bJ09wdEluJ10pCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBpbnRjXzAgLy8gT3B0SW4KICAgID09CiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIG5vdCBPcHRJbgogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIG9wdF9pbgogICAgaW50Y18wIC8vIDEKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fYmFyZV9yb3V0aW5nQDg6CiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weTo1CiAgICAvLyBjbGFzcyBBc3NpZ25tZW50KEFSQzRDb250cmFjdCk6CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBibnogX19wdXlhX2FyYzRfcm91dGVyX19fYWZ0ZXJfaWZfZWxzZUAxMgogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgICEKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gY3JlYXRpbmcKICAgIGludGNfMCAvLyAxCiAgICByZXRzdWIKCl9fcHV5YV9hcmM0X3JvdXRlcl9fX2FmdGVyX2lmX2Vsc2VAMTI6CiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weTo1CiAgICAvLyBjbGFzcyBBc3NpZ25tZW50KEFSQzRDb250cmFjdCk6CiAgICBpbnRjXzEgLy8gMAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmFzc2lnbm1lbnQuY29udHJhY3QuQXNzaWdubWVudC5pbmNyZW1lbnQoKSAtPiB2b2lkOgppbmNyZW1lbnQ6CiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weTo5LTEwCiAgICAvLyBAYWJpbWV0aG9kKCkKICAgIC8vIGRlZiBpbmNyZW1lbnQoc2VsZikgLT4gTm9uZToKICAgIHByb3RvIDAgMAogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MTEKICAgIC8vIGFzc2VydCBUeG4uc2VuZGVyLmlzX29wdGVkX2luKEdsb2JhbC5jdXJyZW50X2FwcGxpY2F0aW9uX2lkKSwgIk11c3Qgb3B0IGluIHRvIGNhbGwiCiAgICB0eG4gU2VuZGVyCiAgICBnbG9iYWwgQ3VycmVudEFwcGxpY2F0aW9uSUQKICAgIGFwcF9vcHRlZF9pbgogICAgYXNzZXJ0IC8vIE11c3Qgb3B0IGluIHRvIGNhbGwKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9hc3NpZ25tZW50L2NvbnRyYWN0LnB5OjEyCiAgICAvLyBzZWxmLmNvdW50ZXJbVHhuLnNlbmRlcl0gKz0gMQogICAgdHhuIFNlbmRlcgogICAgZHVwCiAgICBpbnRjXzEgLy8gMAogICAgYnl0ZWNfMCAvLyAiY291bnRlciIKICAgIGFwcF9sb2NhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBzZWxmLmNvdW50ZXIgZXhpc3RzIGZvciBhY2NvdW50CiAgICBpbnRjXzAgLy8gMQogICAgKwogICAgYnl0ZWNfMCAvLyAiY291bnRlciIKICAgIHN3YXAKICAgIGFwcF9sb2NhbF9wdXQKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5hc3NpZ25tZW50LmNvbnRyYWN0LkFzc2lnbm1lbnQuZGVjcmVtZW50KCkgLT4gdm9pZDoKZGVjcmVtZW50OgogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MTQtMTUKICAgIC8vIEBhYmltZXRob2QoKQogICAgLy8gZGVmIGRlY3JlbWVudChzZWxmKSAtPiBOb25lOgogICAgcHJvdG8gMCAwCiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weToxNgogICAgLy8gYXNzZXJ0IFR4bi5zZW5kZXIuaXNfb3B0ZWRfaW4oR2xvYmFsLmN1cnJlbnRfYXBwbGljYXRpb25faWQpLCAiTXVzdCBvcHQgaW4gdG8gY2FsbCIKICAgIHR4biBTZW5kZXIKICAgIGdsb2JhbCBDdXJyZW50QXBwbGljYXRpb25JRAogICAgYXBwX29wdGVkX2luCiAgICBhc3NlcnQgLy8gTXVzdCBvcHQgaW4gdG8gY2FsbAogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MTcKICAgIC8vIHNlbGYuY291bnRlcltUeG4uc2VuZGVyXSAtPSAxCiAgICB0eG4gU2VuZGVyCiAgICBkdXAKICAgIGludGNfMSAvLyAwCiAgICBieXRlY18wIC8vICJjb3VudGVyIgogICAgYXBwX2xvY2FsX2dldF9leAogICAgYXNzZXJ0IC8vIGNoZWNrIHNlbGYuY291bnRlciBleGlzdHMgZm9yIGFjY291bnQKICAgIGludGNfMCAvLyAxCiAgICAtCiAgICBieXRlY18wIC8vICJjb3VudGVyIgogICAgc3dhcAogICAgYXBwX2xvY2FsX3B1dAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmFzc2lnbm1lbnQuY29udHJhY3QuQXNzaWdubWVudC5nZXQoKSAtPiB1aW50NjQ6CmdldDoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9hc3NpZ25tZW50L2NvbnRyYWN0LnB5OjE5LTIwCiAgICAvLyBAYWJpbWV0aG9kKCkKICAgIC8vIGRlZiBnZXQoc2VsZikgLT4gVUludDY0OgogICAgcHJvdG8gMCAxCiAgICAvLyBzbWFydF9jb250cmFjdHMvYXNzaWdubWVudC9jb250cmFjdC5weToyMQogICAgLy8gYXNzZXJ0IFR4bi5zZW5kZXIuaXNfb3B0ZWRfaW4oR2xvYmFsLmN1cnJlbnRfYXBwbGljYXRpb25faWQpLCAiTXVzdCBvcHQgaW4gdG8gY2FsbCIKICAgIHR4biBTZW5kZXIKICAgIGdsb2JhbCBDdXJyZW50QXBwbGljYXRpb25JRAogICAgYXBwX29wdGVkX2luCiAgICBhc3NlcnQgLy8gTXVzdCBvcHQgaW4gdG8gY2FsbAogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MjIKICAgIC8vIHJldHVybiBzZWxmLmNvdW50ZXJbVHhuLnNlbmRlcl0KICAgIHR4biBTZW5kZXIKICAgIGludGNfMSAvLyAwCiAgICBieXRlY18wIC8vICJjb3VudGVyIgogICAgYXBwX2xvY2FsX2dldF9leAogICAgYXNzZXJ0IC8vIGNoZWNrIHNlbGYuY291bnRlciBleGlzdHMgZm9yIGFjY291bnQKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5hc3NpZ25tZW50LmNvbnRyYWN0LkFzc2lnbm1lbnQub3B0X2luKCkgLT4gdm9pZDoKb3B0X2luOgogICAgLy8gc21hcnRfY29udHJhY3RzL2Fzc2lnbm1lbnQvY29udHJhY3QucHk6MjQtMjUKICAgIC8vIEBhYmltZXRob2QoYWxsb3dfYWN0aW9ucz1bJ09wdEluJ10pCiAgICAvLyBkZWYgb3B0X2luKHNlbGYpIC0+IE5vbmU6CiAgICBwcm90byAwIDAKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9hc3NpZ25tZW50L2NvbnRyYWN0LnB5OjI2CiAgICAvLyBzZWxmLmNvdW50ZXJbVHhuLnNlbmRlcl0gPSBVSW50NjQoMCkKICAgIHR4biBTZW5kZXIKICAgIGJ5dGVjXzAgLy8gImNvdW50ZXIiCiAgICBpbnRjXzEgLy8gMAogICAgYXBwX2xvY2FsX3B1dAogICAgcmV0c3ViCg==",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMuYXNzaWdubWVudC5jb250cmFjdC5Bc3NpZ25tZW50LmNsZWFyX3N0YXRlX3Byb2dyYW06CiAgICBwdXNoaW50IDEgLy8gMQogICAgcmV0dXJuCg=="
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 0
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 1
        }
    },
    "schema": {
        "global": {
            "declared": {},
            "reserved": {}
        },
        "local": {
            "declared": {
                "counter": {
                    "type": "uint64",
                    "key": "counter"
                }
            },
            "reserved": {}
        }
    },
    "contract": {
        "name": "Assignment",
        "methods": [
            {
                "name": "increment",
                "args": [],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "decrement",
                "args": [],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "get",
                "args": [],
                "returns": {
                    "type": "uint64"
                }
            },
            {
                "name": "opt_in",
                "args": [],
                "returns": {
                    "type": "void"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data) # type: ignore[call-overload]
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class IncrementArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "increment()void"


@dataclasses.dataclass(kw_only=True)
class DecrementArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "decrement()void"


@dataclasses.dataclass(kw_only=True)
class GetArgs(_ArgsBase[int]):
    @staticmethod
    def method() -> str:
        return "get()uint64"


@dataclasses.dataclass(kw_only=True)
class OptInArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "opt_in()void"


class LocalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.counter = typing.cast(int, data.get(b"counter"))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def increment(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `increment()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = IncrementArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def decrement(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `decrement()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = DecrementArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def get(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `get()uint64` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = GetArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def opt_in_opt_in(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `opt_in()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = OptInArgs()
        self.app_client.compose_opt_in(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class AssignmentClient:
    """A class for interacting with the Assignment app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        AssignmentClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_local_state(self, account: str | None = None) -> LocalState:
        """Returns the application's local state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_local_state(account, raw=True))
        return LocalState(state)

    def increment(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `increment()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = IncrementArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def decrement(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `decrement()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = DecrementArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def get(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[int]:
        """Calls `get()uint64` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[int]: The result of the transaction"""

        args = GetArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def opt_in_opt_in(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `opt_in()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = OptInArgs()
        result = self.app_client.opt_in(
            call_abi_method=args.method(),
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())

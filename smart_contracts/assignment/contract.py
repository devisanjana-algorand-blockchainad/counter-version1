from algopy import ARC4Contract, String, UInt64
from algopy.arc4 import abimethod

counter = UInt64
class Assignment(ARC4Contract):

    def __init__(self) -> None:
        self.counter = UInt64(0)

    @abimethod()
    def get_counter(self) -> UInt64:
        return self.counter

    @abimethod()
    def increment(self) -> UInt64:
        self.counter += 1
        return self.counter
    
    @abimethod()
    def decrement(self) -> UInt64:
        self.counter -= 1
        return self.counter
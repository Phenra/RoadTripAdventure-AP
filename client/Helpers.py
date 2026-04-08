import time

from .pine import Pine
from ..names import ItemName

BITS_IN_BYTE = 8

def set_bit(bytes : bytes, bitIndex : int, endianness="little") -> bytes:
    # if not isinstance(bytes, int):
    #     val = bytes_to_int(bytes, endianness)
    # else:
    #     val = bytes
    val = bytes_to_int(bytes, endianness)

    if(len(bytes) * BITS_IN_BYTE > bitIndex):
        val = val | (1 << bitIndex)
        val = int_to_bytes(val, len(bytes), endianness)
    else:
        raise ValueError("Error in setBit: Bit index out of range")
    
    return val

def clear_bit(bytes : bytes, bitIndex : int, endianness="little") -> bytes:
    # if not isinstance(bytes, int):
    #     val = bytes_to_int(bytes, endianness)
    # else:
    #     val = bytes
    val = bytes_to_int(bytes, endianness)

    if(len(bytes) * BITS_IN_BYTE > bitIndex):
        val = val & ~(1 << bitIndex)
        val = int_to_bytes(val, len(bytes), endianness)
    else:
        raise ValueError("Error in clearBit: Bit index out of range")
    
    return val

def is_bit_set(bytes : bytes, bit : int, endianness="little") -> bool:
    # If clearBit does not change the value, that means the bit is not set
    return bytes != clear_bit(bytes, bit, endianness)

# https://stackoverflow.com/a/30375198
# Changed function to require a length value - Python removes leading 0s from bytes, which was causing problems.
def int_to_bytes(x: int, len : int, endianness="little") -> bytes:
    return x.to_bytes(len, endianness)

def bytes_to_int(xbytes: bytes, endianness="little") -> int:
    return int.from_bytes(xbytes, endianness)

def bytes_length(x : int) -> int:
    return (x.bit_length() + 7) // 8

# This is used for writes to the player's inventory, just to avoid the possible scenario where a write doesn't
#   complete before the next read starts.
# That would cause some inventory writes to overwrite others (since the 2nd read would use the old inventory state).
def write_bytes_and_verify(pine : Pine, address: int, data: bytes):
    pine.write_bytes(address, data)

    # MAX_WAITS is here just in case this function could otherwise somehow cause an infinite loop in some scenario
    MAX_WAITS = 4 # 1 second
    wait_num = 0
    while pine.read_bytes(address, len(data)) != data and wait_num < MAX_WAITS:
        time.sleep(0.25)
        wait_num += 1

progressive_part_order = {
    ItemName.Progressive_Tires: [
        ItemName.Off_Road_Tires,
        ItemName.Sports_Tires,
        ItemName.Studless_Tires,
        ItemName.Semi_Racing_Tires,
        ItemName.Wet_Tires,
        ItemName.HG_Off_Road_Tires,
        ItemName.HG_Studless_Tires,
        ItemName.HG_Wet_Tires,
        ItemName.Racing_Tires,
        ItemName.Big_Tires,
        ItemName.HG_Racing_Tires,
        #ItemName.Devil_Tires,
    ],
    ItemName.Progressive_Engine: [
        ItemName.Panther_Engine,
        ItemName.Blue_MAX_Engine,
        ItemName.Blue_MAX_v2_Engine,
        ItemName.MAD_Engine,
        ItemName.MAD_v2_Engine,
        ItemName.Long_MAD_Engine,
        ItemName.Black_MAX_Engine,
        ItemName.RS_Magnum_Engine,
        ItemName.Speed_MAX_Engine,
        ItemName.Hyper_MAX_Engine,
        # ItemName.Devil_Engine,       
    ],
    ItemName.Progressive_Chassis: [
        ItemName.Light_Chassis,
        ItemName.Feather_Chassis,
        ItemName.Phantom_Chassis,
        ItemName.Hyper_Chassis,
    ],
    ItemName.Progressive_Transmission: [
        ItemName.Sports_Transmission,
        ItemName.Power_Transmission,
        ItemName.Speed_Transmission,
        ItemName.Wide_Transmission,
        ItemName.Hyper_Transmission,
    ],
    ItemName.Progressive_Steering: [
        ItemName.Quick_Steering,
        ItemName.X2_Quick_Steering,
        ItemName.X3_Quick_Steering,
    ],
    ItemName.Progressive_Brakes: [
        ItemName.Soft_Pad,
        ItemName.Hard_Pad,
        ItemName.Metal_Pad,
    ],
}

class PineMock():
    # Storage container for the data Pine would have written to the game
    class Write():
        def __init__(self, address : int, data : bytes):
            self.address = address
            self.data = data

    def __init__(self):
        self.writes = [] # list[Write]

    # Override of Pine's write_bytes function
    def write_bytes(self, address: int, data: bytes) -> None:
        write = self.Write(address, data)
        self.writes.append(write)

    def compare_writes_to_game_ram(self, game_pine : Pine) -> bool:
        for write in self.writes:
            game_data = game_pine.read_bytes(write.address, len(write.data))

            if write.data != game_data:
                return False
        
        return True

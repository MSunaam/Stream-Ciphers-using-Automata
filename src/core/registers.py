from bitarray import bitarray
from typing import List, Dict

class LFSR:
    def __init__(self, size: int, taps: List[int], clock_bit: int):
        """
        Initialize Linear Feedback Shift Register
        
        Args:
            size (int): Size of the register
            taps (List[int]): Feedback tap positions
            clock_bit (int): Position of the clock control bit
        """
        self.size = size
        self.taps = taps
        self.clock_bit = clock_bit
        self.register = bitarray('0' * size)
    
    def clock(self) -> None:
        """Clock the register one step"""
        feedback = 0
        for tap in self.taps:
            feedback ^= self.register[tap]
        
        # Shift right and insert new feedback bit
        self.register.pop()
        self.register.insert(0, feedback)
    
    def get_clock_bit(self) -> int:
        """Get the current clock control bit"""
        return self.register[self.clock_bit]
    
    def get_output_bit(self) -> int:
        """Get the output bit (last bit)"""
        return self.register[-1]
    
    def get_state(self) -> str:
        """Get current register state as string"""
        return self.register.to01()

class RegisterBank:
    def __init__(self):
        """Initialize the three registers used in A5/1"""
        self.R1 = LFSR(19, [13, 16, 17, 18], 8)
        self.R2 = LFSR(22, [20, 21], 10)
        self.R3 = LFSR(23, [7, 20, 21, 22], 10)
        
    def initialize_key(self, key: str, frame: str = None) -> None:
        """
        Initialize registers with key and frame number
        
        Args:
            key (str): 64-bit initialization key
            frame (str, optional): 22-bit frame number
        """
        key_bits = bitarray(key)
        if len(key_bits) != 64:
            raise ValueError("Key must be 64 bits")
        
        # Reset registers
        self.R1.register = bitarray('0' * 19)
        self.R2.register = bitarray('0' * 22)
        self.R3.register = bitarray('0' * 23)
        
        # Key loading phase
        for i in range(64):
            feedback_bit = key_bits[i]
            self.R1.register.insert(0, feedback_bit)
            self.R2.register.insert(0, feedback_bit)
            self.R3.register.insert(0, feedback_bit)
            self.clock_all()
        
        # Frame loading phase (if provided)
        if frame:
            frame_bits = bitarray(frame)
            if len(frame_bits) != 22:
                raise ValueError("Frame number must be 22 bits")
            
            for i in range(22):
                feedback_bit = frame_bits[i]
                self.R1.register.insert(0, feedback_bit)
                self.R2.register.insert(0, feedback_bit)
                self.R3.register.insert(0, feedback_bit)
                self.clock_all()
        
        # Initial clockings
        for _ in range(100):
            self.clock_registers()
    
    def clock_registers(self) -> int:
        """
        Clock registers according to majority rule
        Returns:
            int: Output bit
        """
        majority = self.get_majority()
        
        # Clock registers whose clock bit matches majority
        if self.R1.get_clock_bit() == majority:
            self.R1.clock()
        if self.R2.get_clock_bit() == majority:
            self.R2.clock()
        if self.R3.get_clock_bit() == majority:
            self.R3.clock()
        
        # Generate output
        return (self.R1.get_output_bit() ^ 
                self.R2.get_output_bit() ^ 
                self.R3.get_output_bit())
    
    def clock_all(self) -> None:
        """Clock all registers regardless of majority"""
        self.R1.clock()
        self.R2.clock()
        self.R3.clock()
    
    def get_majority(self) -> int:
        """Calculate majority bit from clock control bits"""
        bits = [
            self.R1.get_clock_bit(),
            self.R2.get_clock_bit(),
            self.R3.get_clock_bit()
        ]
        return 1 if sum(bits) >= 2 else 0
    
    def get_state(self) -> Dict[str, str]:
        """Get current state of all registers"""
        return {
            'R1': self.R1.get_state(),
            'R2': self.R2.get_state(),
            'R3': self.R3.get_state()
        }
from bitarray import bitarray
from typing import Tuple, List, Dict
from .registers import RegisterBank
from src.analysis.statistics import A51Statistics
from src.analysis.visualizer import A51Visualizer

class A51Cipher:
    def __init__(self):
        self.registers = RegisterBank()
        self.keystream = bitarray()
        self.state_history = []
        self.statistics = A51Statistics()
        self.visualizer = A51Visualizer(self.statistics)
    
    def initialize(self, key: str, frame: str = None) -> None:
        """Initialize cipher with key and optional frame number"""
        self.registers.initialize_key(key, frame)
        self.keystream.clear()
        self.state_history.clear()
    
    def generate_keystream(self, length: int) -> bitarray:
        self.keystream.clear()
        self.state_history.clear()
        
        prev_state = self.registers.get_state()  # Initialize prev_state here
        
        for _ in range(length):
            self.state_history.append(self.registers.get_state())
            output_bit = self.registers.clock_registers()
            self.keystream.append(output_bit)
            
            current_state = self.registers.get_state()
            self.statistics.record_transition(prev_state, current_state)
            prev_state = current_state
        
        return self.keystream

    def generate_state_transition_graph(self, max_nodes: int = 100, output_file: str = 'a51_state_transition.png'):
        G = self.visualizer.generate_graph(max_nodes)
        self.visualizer.visualize_graph(G, output_file)
    def encrypt_decrypt(self, message: bitarray) -> bitarray:
        """
        Encrypt or decrypt message
        Note: Stream ciphers use same operation for both
        """
        if len(message) > len(self.keystream):
            self.generate_keystream(len(message))
        
        return message ^ self.keystream[:len(message)]
    
    def get_state_history(self) -> List[Dict[str, str]]:
        """Get history of states for visualization"""
        return self.state_history
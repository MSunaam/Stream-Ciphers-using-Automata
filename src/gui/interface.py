import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from bitarray import bitarray
import re

class A51GUI:
    def __init__(self, cipher):
        self.cipher = cipher
        self.root = tk.Tk()
        self.root.title("A5/1 Stream Cipher Simulator")
        self.root.geometry("800x600")
        
        self.create_input_frame()
        self.create_output_frame()
        self.create_visualization_frame()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Input", padding="10")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Key input
        ttk.Label(input_frame, text="Key (64-bit binary):").grid(row=0, column=0, sticky="w")
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(input_frame, textvariable=self.key_var, width=70)
        self.key_entry.grid(row=0, column=1, padx=5)
        
        # Frame number input
        ttk.Label(input_frame, text="Frame (22-bit binary):").grid(row=1, column=0, sticky="w")
        self.frame_var = tk.StringVar()
        self.frame_entry = ttk.Entry(input_frame, textvariable=self.frame_var, width=70)
        self.frame_entry.grid(row=1, column=1, padx=5)
        
        # Message input
        ttk.Label(input_frame, text="Message (binary):").grid(row=2, column=0, sticky="w")
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(input_frame, textvariable=self.message_var, width=70)
        self.message_entry.grid(row=2, column=1, padx=5)
        
        # Process button
        self.process_btn = ttk.Button(input_frame, text="Process", command=self.process_message)
        self.process_btn.grid(row=3, column=1, pady=10)
        
    def create_output_frame(self):
        output_frame = ttk.LabelFrame(self.root, text="Output", padding="10")
        output_frame.pack(fill="x", padx=5, pady=5)
        
        # Encrypted output
        ttk.Label(output_frame, text="Encrypted:").grid(row=0, column=0, sticky="w")
        self.encrypted_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.encrypted_var, width=70, state="readonly").grid(row=0, column=1, padx=5)
        
        # Decrypted output
        ttk.Label(output_frame, text="Decrypted:").grid(row=1, column=0, sticky="w")
        self.decrypted_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.decrypted_var, width=70, state="readonly").grid(row=1, column=1, padx=5)
        
        # Keystream output
        ttk.Label(output_frame, text="Keystream:").grid(row=2, column=0, sticky="w")
        self.keystream_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.keystream_var, width=70, state="readonly").grid(row=2, column=1, padx=5)
        
    def create_visualization_frame(self):
        viz_frame = ttk.LabelFrame(self.root, text="Register States", padding="10")
        viz_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def validate_binary_input(self, input_str, length):
        if not re.match(f"^[01]{{{length}}}$", input_str):
            return False
        return True
        
    def process_message(self):
        # Validate inputs
        key = self.key_var.get()
        frame = self.frame_var.get()
        message = self.message_var.get()
        
        if not self.validate_binary_input(key, 64):
            messagebox.showerror("Error", "Key must be 64 bits binary")
            return
            
        if frame and not self.validate_binary_input(frame, 22):
            messagebox.showerror("Error", "Frame must be 22 bits binary")
            return
            
        if not re.match("^[01]+$", message):
            messagebox.showerror("Error", "Message must be binary")
            return
        
        try:
            # Initialize cipher
            self.cipher.initialize(key, frame)
            
            # Process message
            message_bits = bitarray(message)
            encrypted = self.cipher.encrypt_decrypt(message_bits)
            decrypted = self.cipher.encrypt_decrypt(encrypted)
            
            # Update outputs
            self.encrypted_var.set(encrypted.to01())
            self.decrypted_var.set(decrypted.to01())
            self.keystream_var.set(self.cipher.keystream.to01())
            
            # Update visualization
            self.update_visualization()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_visualization(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        states = self.cipher.get_state_history()
        if not states:
            return
            
        # Create visualization
        rows = []
        for state in states:
            row = []
            for reg in ['R1', 'R2', 'R3']:
                row.extend([int(bit) for bit in state[reg]])
            rows.append(row)
        
        # Plot heatmap
        ax.imshow(rows, cmap='Blues', aspect='auto')
        ax.set_xlabel('Bit Position')
        ax.set_ylabel('Clock Cycle')
        
        # Add register separators
        ax.axvline(x=18.5, color='red', linestyle='-', linewidth=0.5)
        ax.axvline(x=40.5, color='red', linestyle='-', linewidth=0.5)
        
        self.canvas.draw()
    
    def run(self):
        self.root.mainloop()
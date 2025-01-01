import argparse
from bitarray import bitarray
import bitarray
from src.core.cipher import A51Cipher
from src.gui.interface import A51GUI


def main():
    parser = argparse.ArgumentParser(description="A5/1 Stream Cipher Simulator")
    parser.add_argument("--key", type=str, help="64-bit initialization key")
    parser.add_argument("--frame", type=str, help="22-bit frame number", default=None)
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument(
        "--graph", action="store_true", help="Generate state transition graph"
    )
    parser.add_argument(
        "--graph_steps",
        type=int,
        default=1000,
        help="Number of steps for graph generation",
    )

    args = parser.parse_args()

    cipher = A51Cipher()
    if args.graph:
        if not args.key:
            print("Error: Key is required for graph generation")
            return
        cipher.initialize(args.key, args.frame)
        cipher.generate_keystream(args.graph_steps)
        cipher.generate_state_transition_graph()
        print("State transition graph saved as 'a51_state_transition.png'")
    elif args.gui:
        gui = A51GUI(cipher)
        gui.run()
    else:
        # Command line mode
        if not args.key:
            print("Error: Key is required in command line mode")
            return

        cipher.initialize(args.key, args.frame)

        # Example usage
        message = input("Enter message (as binary string): ")
        message_bits = bitarray.bitarray(message)

        encrypted = cipher.encrypt_decrypt(message_bits)
        print(f"Encrypted: {encrypted.to01()}")

        decrypted = cipher.encrypt_decrypt(encrypted)
        print(f"Decrypted: {decrypted.to01()}")


if __name__ == "__main__":
    main()

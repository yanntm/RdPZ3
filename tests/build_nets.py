# tests/build_nets.py
import argparse
from rdpz3.exportpnml import export_to_pnml
from tests.example_nets import net1, net2, net3

def main():
    parser = argparse.ArgumentParser(description='Build and export example Petri nets to PNML format.')
    parser.add_argument('net', choices=['net1', 'net2', 'net3'], help='The example net to build and export')
    parser.add_argument('output', type=str, help='The output PNML file path')

    args = parser.parse_args()
    net_name = args.net
    output_path = args.output

    # Build the selected net
    if net_name == 'net1':
        rdp = net1()
    elif net_name == 'net2':
        rdp = net2()
    elif net_name == 'net3':
        rdp = net3()

    # Export the net to PNML
    export_to_pnml(rdp, output_path)
    print(f"Exported {net_name} to {output_path}")

if __name__ == "__main__":
    main()

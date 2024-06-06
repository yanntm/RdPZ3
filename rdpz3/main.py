import argparse
from rdpz3.pnmlParser import PNMLParser
from rdpz3.exportdot import export_rdp_to_dot
from rdpz3.Prop import Prop

def parse_pnml_to_rdp(pnml_path):
    parser = PNMLParser()
    return parser.parse(pnml_path)

def main():
    parser = argparse.ArgumentParser(description='Parse a PNML file, export to DOT format, and check properties.')
    parser.add_argument('-pnml', type=str, required=True, help='Path to the PNML file')
    parser.add_argument('-d', '--exportDot', action='store_true', help='Export to DOT format')
    parser.add_argument('-prop', type=str, help='Property to check')

    args = parser.parse_args()
    pnml_path = args.pnml
    dot_path = pnml_path.replace('.pnml', '.dot')
    
    # Parse PNML file to RdP
    rdp = parse_pnml_to_rdp(pnml_path)

    # Export to DOT format if the flag is set
    if args.exportDot:
        export_rdp_to_dot(rdp, dot_path, net_name=pnml_path.split('/')[-1].replace('.pnml', ''))
        print(f"Exported {pnml_path} to {dot_path}")

    # Check property if provided
    if args.prop:
        prop = Prop(rdp)
        # Evaluate the property string in the context of the Prop instance
        property_condition = eval(args.prop, {'prop': prop})
        result = prop.algo(property_condition)
        print(f"Property check result: {result}")

if __name__ == "__main__":
    main()

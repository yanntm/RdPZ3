from rdpz3.RdP import RdP

def export_rdp_to_dot(rdp, filename, net_name="net"):
    dot = []
    dot.append('digraph {')
    dot.append('  overlap="false";')
    dot.append('  labelloc="t";')
    dot.append(f'  label="places: {len(rdp.place)} trans: {len(rdp.trans)} {net_name}";')
    
    # Dump places
    for i, place in enumerate(rdp.place):
        if rdp.m0[i] > 0:
            dot.append(f'  p{i} [shape="oval", label="{place}({rdp.m0[i]})"];')
        else:
            dot.append(f'  p{i} [shape="oval", label="{place}"];')

    # Dump transitions and related arcs
    for t_idx, trans in enumerate(rdp.trans):
        dot.append(f'  t{t_idx} [shape="rectangle", label="{trans}"];')
        # Pre-conditions (input arcs)
        for p, v in rdp.pre[t_idx]:
            if v == 1:
                dot.append(f'  p{p} -> t{t_idx};')
            else:
                dot.append(f'  p{p} -> t{t_idx} [label="{v}"];')
        # Post-conditions (output arcs)
        for p, v in rdp.post[t_idx]:
            if v == 1:
                dot.append(f'  t{t_idx} -> p{p};')
            else:
                dot.append(f'  t{t_idx} -> p{p} [label="{v}"];')
    
    dot.append('}')
    
    # Write to file
    with open(filename, 'w') as file:
        file.write('\n'.join(dot))

# Usage example
place = ['A', 'B']
trans = ['t0', 't1']
pre = [[(0, 1), (1, 2)], [(0, 1)]]
post = [[(0, 1), (1, 1)], [(1, 1)]]
m0 = [1, 0]

rdp = RdP(place, trans, pre, post, m0)
export_rdp_to_dot(rdp, 'output.dot', net_name="net1")

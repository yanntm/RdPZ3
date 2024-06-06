# rdpz3/exportpnml.py

def export_to_pnml(rdp, filename):
    import xml.etree.ElementTree as ET

    pnml = ET.Element("pnml", xmlns="http://www.pnml.org/version-2009/grammar/pnml")
    net = ET.SubElement(pnml, "net", id="net1", type="http://www.pnml.org/version-2009/grammar/ptnet")

    for i, place in enumerate(rdp.place):
        place_element = ET.SubElement(net, "place", id=f"p{i}")
        name_element = ET.SubElement(place_element, "name")
        text_element = ET.SubElement(name_element, "text")
        text_element.text = place
        if rdp.m0[i] > 0:
            marking_element = ET.SubElement(place_element, "initialMarking")
            text_element = ET.SubElement(marking_element, "text")
            text_element.text = str(rdp.m0[i])

    for i, trans in enumerate(rdp.trans):
        trans_element = ET.SubElement(net, "transition", id=f"t{i}")
        name_element = ET.SubElement(trans_element, "name")
        text_element = ET.SubElement(name_element, "text")
        text_element.text = trans

    arc_id = 0
    for t_idx, pre_list in enumerate(rdp.pre):
        for p_idx, weight in pre_list:
            arc_element = ET.SubElement(net, "arc", id=f"arc{arc_id}", source=f"p{p_idx}", target=f"t{t_idx}")
            if weight > 1:
                inscription_element = ET.SubElement(arc_element, "inscription")
                text_element = ET.SubElement(inscription_element, "text")
                text_element.text = str(weight)
            arc_id += 1

    for t_idx, post_list in enumerate(rdp.post):
        for p_idx, weight in post_list:
            arc_element = ET.SubElement(net, "arc", id=f"arc{arc_id}", source=f"t{t_idx}", target=f"p{p_idx}")
            if weight > 1:
                inscription_element = ET.SubElement(arc_element, "inscription")
                text_element = ET.SubElement(inscription_element, "text")
                text_element.text = str(weight)
            arc_id += 1

    tree = ET.ElementTree(pnml)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

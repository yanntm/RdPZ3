# rdpz3/pnmlParser.py

import xml.parsers.expat
from rdpz3.RdP import RdP

class PNMLParser:
    def __init__(self):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.StartElementHandler = self.start_element
        self.parser.EndElementHandler = self.end_element
        self.parser.CharacterDataHandler = self.char_data

        self.stack = []
        self.net = {'places': {}, 'transitions': {}, 'pre': [], 'post': [], 'm0': []}
        self.index = {}
        self.topatch = []
        self.last_seen = ""
        self.read_text = False
        self.last_int = -1
        self.read_int = False
        self.in_opaque_toolspecific = False
        self.do_it = False

    def parse(self, filename):
        with open(filename, 'rb') as file:
            self.parser.ParseFile(file)
        return self.construct_rdp()

    def start_element(self, name, attrs):
        if self.in_opaque_toolspecific:
            return

        if name == "net":
            for key, value in attrs.items():
                if key == "id":
                    self.net['id'] = value
                elif key == "type":
                    if value != "http://www.pnml.org/version-2009/grammar/ptnet":
                        raise ValueError("Net is not a P/T net. Colors are not supported currently.")
            self.stack.append(self.net)
        
        elif name == "name":
            self.read_text = True

        elif name == "place":
            id = attrs['id']
            place_index = len(self.net['places'])
            self.net['places'][id] = place_index
            self.index[id] = (True, place_index)
            self.net['m0'].append(0)  # Initialize marking to 0
            self.stack.append(place_index)

        elif name == "initialMarking":
            self.read_int = True

        elif name == "transition":
            id = attrs['id']
            self.net['transitions'][id] = len(self.net['transitions'])
            self.index[id] = (False, self.net['transitions'][id])
            self.stack.append(self.net['transitions'][id])

        elif name == "arc":
            source = attrs['source']
            target = attrs['target']
            arc = {'source': source, 'target': target, 'value': 1}
            self.stack.append(arc)
        
        elif name == "toolspecific":
            self.in_opaque_toolspecific = True
        
        elif name == "text":
            self.do_it = True

    def end_element(self, name):
        if name == "toolspecific":
            self.in_opaque_toolspecific = False
            return

        if self.in_opaque_toolspecific:
            return

        if name == "net":
            self.stack.pop()

        elif name == "name":
            self.read_text = False
            self.last_seen = ""

        elif name == "place":
            self.stack.pop()

        elif name == "transition":
            self.stack.pop()

        elif name == "arc":
            arc = self.stack.pop()
            src = arc['source']
            tgt = arc['target']

            if src in self.index and tgt in self.index:
                if self.index[src][0]:
                    # Source is a place
                    self.net['pre'].append((self.index[src][1], self.index[tgt][1], arc['value']))
                else:
                    # Source is a transition
                    self.net['post'].append((self.index[tgt][1], self.index[src][1], arc['value']))
            else:
                self.topatch.append(arc)

        elif name == "text":
            self.do_it = False

        elif name == "initialMarking":
            place_id = self.stack[-1]
            self.net['m0'][place_id] = self.last_int
            self.read_int = False
            self.last_int = -1

        elif name == "pnml":
            # Patch missing arc targets
            for arc in self.topatch:
                src = arc['source']
                tgt = arc['target']

                if src in self.index and tgt in self.index:
                    if self.index[src][0]:
                        # Source is a place
                        self.net['pre'].append((self.index[src][1], self.index[tgt][1], arc['value']))
                    else:
                        # Source is a transition
                        self.net['post'].append((self.index[tgt][1], self.index[src][1], arc['value']))
                else:
                    raise ValueError(f"Problem when linking arc: source or target node not found <{src}, {tgt}>")
            self.topatch.clear()

    def char_data(self, data):
        if self.in_opaque_toolspecific:
            return

        if self.do_it:
            if self.read_text:
                self.last_seen = data.strip()
            elif self.read_int:
                self.last_int = int(data.strip())

    def construct_rdp(self):
        places = list(self.net['places'].keys())
        transitions = list(self.net['transitions'].keys())
        pre = [[] for _ in transitions]
        post = [[] for _ in transitions]

        for p, t, v in self.net['pre']:
            pre[t].append((p, v))

        for p, t, v in self.net['post']:
            post[t].append((p, v))

        return RdP(places, transitions, pre, post, self.net['m0'])

# Example usage
if __name__ == "__main__":
    parser = PNMLParser()
    rdp = parser.parse("examples/net2.pnml")
    print(rdp)

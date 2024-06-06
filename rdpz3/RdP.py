class RdP(object):
    def __init__(self, place, trans, pre, post, m0):
        self.place = place
        self.trans = trans
        self.pre = pre
        self.post = post
        self.m0 = m0
        self.succ = self.succPlace()
        self.pred = self.predPlace()
    def predPlace(self):
        res = [];
        for p in range(len(self.place)):
            res.append([])

        for t in range(len(self.trans)):
            for p, v in self.post[t]:
                res[p].append(t)
        return res

    def succPlace(self):
        res = [];
        for p in range(len(self.place)):
            res.append([])

        for t in range(len(self.trans)):
            for p, v in self.pre[t]:
                res[p].append(t)
        return res

    def maxtrap(self, E):
        m = E.copy()
        todo = []
        nbsucc = []

        for i in range(len(self.trans)):
            nbsucc.append(len(self.post[i]))

        for p in range(len(self.place)):
            if p not in m:
                for t in self.pred[p]:
                    nbsucc[t] -= 1
                    if nbsucc[t] == 0:
                        todo.append(t)

        while len(todo) > 0:
            t = todo.pop()
            for p, v in self.pre[t]:
                if p in m:
                    m.discard(p)
                    for t in self.pred[p]:
                        nbsucc[t] -= 1
                        if nbsucc[t] == 0:
                            todo.append(t)
        return m

    def checkmarked(self,trap):
        for p in trap:
            if self.m0[p]>0:
                return True
        return False
from z3 import *
class Prop:
    def __init__(self, rdp):
        self.rdp = rdp
        self.solver = Solver()
        self.place = IntVector('p', len(self.rdp.place))
        self.trans = IntVector('t', len(self.rdp.trans))

    def equationEtat(self):
        for i in range(len(self.place)):
            self.solver.add(self.place[i] >= 0)

        for i in range(len(self.trans)):
            self.solver.add(self.trans[i] >= 0)

        m = self.rdp.m0.copy()
        for i in range(len(self.rdp.trans)):
            for p, v in self.rdp.pre[i]:
                m[p] = m[p] - v * self.trans[i]

        for i in range(len(self.rdp.trans)):
            for p, v in self.rdp.post[i]:
                m[p] = m[p] + v * self.trans[i]

        for p in range(len(self.place)):
            self.solver.add(self.place[p] == m[p])

    def add(self, *propriete):
        self.solver.add(propriete)

    def solve(self):
        if self.solver.check() == sat:
            return self.solver.model()
        else:
            return None

    def addtrap(self, trap):
        trapprop = 0
        for p in trap:
            trapprop = trapprop + self.place[p]
        self.solver.add(trapprop >= 1)

    def addtrapmodel(self, trap,predtrapmodel):
        trapprop = 0
        for p in trap:
            trapprop = trapprop + self.place[p]
        trapprop=trapprop >= 1
        for t in predtrapmodel:
            trapprop = Or(trapprop,self.trans[t]==0)
        self.solver.add(trapprop)

    def gettrap(self, model):
        res = set()
        for p in range(len(self.place)):
            if model[self.place[p]] == 0:
                res.add(p)
        res = self.rdp.maxtrap(res)
        return res

    def predtrapmodel(self, trap,model):
        res = set()
        for p in trap:
            for t in self.rdp.pred[p]:
                if not model[self.trans[t]] == 0:
                    res.add(t)
        return res

    def algo(self, *propriete):
        self.solver.add(propriete)
        self.equationEtat()
        while True:
            check = self.solver.check()
            if check == unsat:
                return False
            else:
                model = self.solver.model()
                trap = self.gettrap(model)
                if len(trap) == 0:
                    return model
                elif not self.rdp.checkmarked(trap):
                    predtrapmodel= self.predtrapmodel(trap,model)
                    if len(predtrapmodel)==0:
                        return model
                    else:
                        self.addtrapmodel(trap,predtrapmodel)
                else:
                    self.addtrap(trap)

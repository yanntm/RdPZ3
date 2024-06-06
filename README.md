# RdPZ3
Experimental project playing with Z3 and Petri nets in python.


```
pip install z3-solver
# build some examples as pnml
for i in net1 net2 net3 ;  do python -m tests.build_nets $i examples/${i}_exported.pnml ; done
# export pnml to dot for debugging
for i in examples/*.pnml ; do python -m rdpz3.main -pnml $i -d ; done
# look at dot models
cd examples ; for i in *.dot ; do dot -Tpdf $i -o $i.pdf ; done ; cd ..
# open the pdf
evince examples/*.dot.pdf
# check property
for i in examples/*.pnml ; do python -m rdpz3.main -pnml $i -prop "prop.place[1] == 1"; done
```




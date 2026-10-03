import networkx as nx
def compile_plan(p):
 keys={x.key for x in p.tasks}
 if len(keys)!=len(p.tasks):raise ValueError("duplicate task")
 g=nx.DiGraph()
 for t in p.tasks:
  g.add_node(t.key)
  for d in t.depends_on:
   if d not in keys:raise ValueError(f"missing dependency {d}")
   g.add_edge(d,t.key)
 if not nx.is_directed_acyclic_graph(g):raise ValueError("task graph cycle")
 return g

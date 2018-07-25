from quanto.util.Scripting import *

simps0 = load_rules([
  "rules/axioms/red_copy", "rules/axioms/green_copy",
  "rules/axioms/red_sp", "rules/axioms/green_sp",
  "rules/axioms/hopf",
  "rules/axioms/red_scalar", "rules/axioms/green_scalar",
  "rules/axioms/red_loop", "rules/axioms/green_loop"])

simps = simps0 + load_rules(["rules/axioms/green_id", "rules/axioms/red_id"])

green_id_inv = load_rule("rules/axioms/green_id").inverse()
red_id_inv = load_rule("rules/axioms/red_id").inverse()
rotate = load_rule("rules/theorems/rotate_targeted")


def num_boundary_X(g):
  return len([v for v in verts(g)
    if g.isBoundary(v) and g.isAdjacentToType(v, 'X')])

def next_rotation_Z(g):
  vs = [(g.arity(v),v) for v in verts(g)
    if g.typeOf(v) == 'Z' and
       vertex_angle_is(g, v, '0') and
       not g.isAdjacentToBoundary(v)]
  if (len(vs) == 0): return None
  else: return min(vs)[1]


simproc = (
  REDUCE(simps) >>
  REDUCE_METRIC(green_id_inv, num_boundary_X) >>
  REPEAT(
    REDUCE_TARGETED(rotate, "v10", next_rotation_Z) >>
    REDUCE(simps0)
  ) >>
  REDUCE(simps)
)


register_simproc("rotate-simp", simproc)



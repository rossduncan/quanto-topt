from quanto.util.Scripting import *

simps = load_rules([
  "rules/axioms/red_copy", "rules/axioms/red_sp", "rules/axioms/green_sp",
  "rules/axioms/hopf","rules/axioms/red_scalar", "rules/axioms/green_scalar",
  "rules/axioms/green_id","rules/axioms/red_id", "rules/axioms/red_loop",
  "rules/axioms/green_loop"])

register_simproc("basic-simp", REDUCE(simps))



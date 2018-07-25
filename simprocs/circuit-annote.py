from quanto.util.Scripting import *

annotes = load_rules([
    "rules/annotations/green-to-red", "rules/annotations/red-to-green",
    "rules/annotations/green-to-red2", "rules/annotations/red-to-green2",
	"rules/annotations/green-from-red", "rules/annotations/red-from-green",
	"rules/annotations/green-unspider","rules/annotations/red-unspider",
	"rules/annotations/cnot-succ"])

# let's use the internal definition of input vertex


def has_marked_edge(g,v) :
    for e in each(g.adjacentEdges(v)) :
        if g.edata().get(e).get().isDirected() :
            return True
    return False


def get_unmarked_inputs(g) :    
    uns = [v for v in each(g.inputs()) if not has_marked_edge(g,v) ]
    print(uns)
    return uns

def get_input_targets(g,type="X") :
    succs = [ each(g.succVerts(i)) for i in get_unmarked_inputs(g) ]    
    flat = [v for ss in succs for v in ss]
    return [v for v in flat if g.typeOf(v)==type]

def next_input_target(g,type="X") :
    tgts = get_input_targets(g,type)
    if (len(tgts) > 0) :
        return tgts[0]
    else :
        return None

def next_input_target_green(g) :
    print("Next GREEEN green green")
    return next_input_target(g,"Z")

def next_input_target_red(g) :
    print("Next pish posh called")
    return next_input_target(g,"X")



in_green = load_rule("rules/annotations/any-to-green")
in_red = load_rule("rules/annotations/any-to-red")

mark_red_ins = REDUCE_TARGETED(in_red,"v0",next_input_target_red)
mark_green_ins = REDUCE_TARGETED(in_green,"v0",next_input_target_green)

mark_inputs = (mark_red_ins >> mark_green_ins)

register_simproc("mark_inputs", mark_inputs)









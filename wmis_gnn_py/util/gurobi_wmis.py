import networkx as nx
import gurobipy as gp
from gurobipy import GRB


def wmis_ilp(G: nx.Graph):
    try:
        m = gp.Model("Weighted Maximum Independent Set")
        m.Params.LogToConsole = 0

        m.setAttr("ModelSense", -1)

        nodes = list(G.nodes)
        node_weights = nx.get_node_attributes(G, "weight")

        x = m.addVars(nodes, vtype=GRB.BINARY, obj=node_weights, name="vertices")

        m.addConstrs((x[u] + x[v] <= 1 for u, v in G.edges), "cap")

        m.optimize()

        if m.status == GRB.OPTIMAL:
            solution = m.getAttr("x", x)
            binary_solution = {k: int(v) for k, v in solution.items()}
            nx.set_node_attributes(G, binary_solution, name="solution")
        else:
            raise Exception("Did not found optimal solution!")

    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")
    except AttributeError:
        print("Encountered an attribute error")


def wmis_lp(G: nx.Graph):
    try:
        m = gp.Model("Weighted Maximum Independent Set")
        m.Params.LogToConsole = 0

        m.setAttr("ModelSense", -1)

        nodes = list(G.nodes)
        node_weights = nx.get_node_attributes(G, "weight")

        x = m.addVars(
            nodes,
            lb=0.0,
            ub=1.0,
            obj=node_weights,
            vtype=GRB.CONTINUOUS,
            name="vertices",
        )

        m.addConstrs((x[u] + x[v] <= 1 for u, v in G.edges), "cap")

        m.optimize()

        if m.status == GRB.OPTIMAL:
            solution = m.getAttr("x", x)
            solution = {k: v for k, v in solution.items()}
            nx.set_node_attributes(G, solution, name="solution")
        else:
            raise Exception("Did not found optimal solution!")

    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")
    except AttributeError:
        print("Encountered an attribute error")

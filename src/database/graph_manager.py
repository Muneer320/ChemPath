"""Read-only, validated teaching graph for ChemPath."""

from heapq import heappop, heappush
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "reactions.json"


class ChemicalGraph:
    def __init__(self, data_file=DATA_FILE):
        data = json.loads(Path(data_file).read_text(encoding="utf-8"))
        self.compounds = {}
        self.lookup = {}
        self.adjacency = {}
        self.reactions = []
        for compound in data["compounds"]:
            identifier = compound["id"]
            if identifier in self.compounds or not compound["name"] or not compound["formula"]:
                raise ValueError(f"Invalid or duplicate compound: {identifier}")
            self.compounds[identifier] = compound
            self.adjacency[identifier] = []
            for alias in [identifier, compound["name"], compound["formula"], *compound.get("aliases", [])]:
                key = alias.casefold().strip()
                if key in self.lookup and self.lookup[key] != identifier:
                    raise ValueError(f"Ambiguous compound alias: {alias}")
                self.lookup[key] = identifier
        seen = set()
        for reaction in data["reactions"]:
            source, target = reaction["reactant"], reaction["product"]
            conditions = reaction["conditions"]
            identity = (source, target, conditions["reagent"].casefold())
            if (source not in self.compounds or target not in self.compounds or source == target
                    or not 1 <= reaction["teaching_cost"] <= 3 or identity in seen):
                raise ValueError(f"Invalid or duplicate reaction: {reaction['id']}")
            seen.add(identity)
            self.reactions.append(reaction)
            self.adjacency[source].append(reaction)
        for edges in self.adjacency.values():
            edges.sort(key=lambda item: (item["teaching_cost"], item["product"], item["id"]))

    def resolve(self, identifier):
        return self.lookup.get(identifier.casefold().strip())

    def get_compound(self, identifier):
        key = self.resolve(identifier)
        return self.compounds.get(key)

    def get_compounds(self, search=None):
        compounds = sorted(self.compounds.values(), key=lambda item: item["name"])
        if search:
            term = search.casefold().strip()
            compounds = [item for item in compounds if any(
                term in value.casefold() for value in [item["id"], item["name"], item["formula"], *item.get("aliases", [])]
            )]
        return compounds

    def get_compound_suggestions(self, prefix, limit=10):
        term = prefix.casefold().strip()
        return [item for item in self.get_compounds() if any(
            value.casefold().startswith(term) for value in [item["id"], item["name"], item["formula"], *item.get("aliases", [])]
        )][:limit]

    def find_paths(self, start, end, max_steps=5, limit=10):
        source, target = self.resolve(start), self.resolve(end)
        if source is None or target is None:
            raise KeyError("Unknown start or end compound")
        if source == target:
            return []
        queue = [(0, 0, 0, (source,), ())]
        sequence = 0
        results = []
        while queue and len(results) < limit:
            cost, steps, _, nodes, edges = heappop(queue)
            current = nodes[-1]
            if current == target:
                results.append({
                    "compounds": [self.compounds[node] for node in nodes],
                    "reactions": [edge["conditions"] for edge in edges],
                    "reagents": [edge["conditions"]["reagent"] for edge in edges],
                    "total_steps": steps,
                    "teaching_cost": cost,
                })
                continue
            if steps >= max_steps:
                continue
            for edge in self.adjacency[current]:
                if edge["product"] not in nodes:
                    sequence += 1
                    heappush(queue, (cost + edge["teaching_cost"], steps + 1, sequence,
                                     (*nodes, edge["product"]), (*edges, edge)))
        return results

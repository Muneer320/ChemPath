"""Non-destructive contracts for the read-only teaching graph."""

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from main import app
from src.database.graph_manager import ChemicalGraph


class GraphContracts(unittest.TestCase):
    def setUp(self):
        self.graph = ChemicalGraph()

    def test_data_and_name_lookup(self):
        self.assertEqual(len(self.graph.compounds), 21)
        self.assertEqual(len(self.graph.reactions), 23)
        self.assertEqual(self.graph.get_compound("acetic acid")["id"], "ethanoic-acid")
        self.assertEqual(self.graph.get_compound("CH2CH2")["id"], "ethene")
        self.assertEqual(self.graph.get_compound_suggestions("etha")[0]["id"], "ethanal")

    def test_parallel_edges_and_loop_free_ranked_paths(self):
        paths = self.graph.find_paths("ethene", "ethanoic acid", max_steps=4)
        self.assertGreaterEqual(len(paths), 4)
        self.assertEqual(paths[0]["total_steps"], 2)
        for path in paths:
            ids = [compound["id"] for compound in path["compounds"]]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertLessEqual(path["total_steps"], 4)
            self.assertEqual(path["total_steps"], len(path["reactions"]))
        variants = self.graph.find_paths("ethanol", "ethanal", max_steps=1)
        self.assertEqual({path["reagents"][0] for path in variants}, {"Cu, heat", "CuO, heat"})
        self.assertEqual(self.graph.find_paths("ethene", "ethanoic acid", max_steps=1), [])

    def test_bad_data_fails_validation(self):
        sample = json.loads((Path(__file__).resolve().parents[1] / "data" / "reactions.json").read_text(encoding="utf-8"))
        sample["reactions"][0]["product"] = "missing"
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "bad.json"
            bad.write_text(json.dumps(sample), encoding="utf-8")
            with self.assertRaises(ValueError):
                ChemicalGraph(bad)

    def test_read_only_api(self):
        with TestClient(app) as client:
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()["reactions"], 23)
            self.assertEqual(client.get("/compounds/suggestions/?prefix=acetic").json()[0]["id"], "ethanoic-acid")
            self.assertEqual(client.get("/compounds/unknown").status_code, 404)
            self.assertEqual(client.get("/paths/?start=ethene&end=ethanoic-acid").status_code, 200)
            self.assertEqual(client.get("/paths/?start=phenol&end=ethene").status_code, 404)
            self.assertEqual(client.post("/compounds/", json={"formula": "C"}).status_code, 405)


if __name__ == "__main__":
    unittest.main()

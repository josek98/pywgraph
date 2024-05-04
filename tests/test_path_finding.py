from pywgraph import WeightedDirectedGraph


def graph() -> WeightedDirectedGraph:
    dictionary = {
        "A": {"B": 1.0, "C": 2.5},
        "B": {"C": 3.0},
        "C": {"A": 2.0, "D": 1.3},
        "D": {"E": 3.4},
        "E": {"C": 4.0, "A": 13.0},
    }
    return WeightedDirectedGraph.from_dict(dictionary)


class TestPathFinding:

    def test_ab(self): 
        assert graph().find_path("A", "B") == ["A", "B"]

    def test_ac(self):
        assert graph().find_path("A", "C") == ["A", "C"]

    def test_ad(self):
        assert graph().find_path("A", "D") == ["A", "C", "D"]

    def test_ae(self):
        assert graph().find_path("A", "E") == ["A", "C", "D", "E"]

    def test_ba(self):
        assert graph().find_path("B", "A") == ["B", "C", "A"]

    def test_bc(self):
        assert graph().find_path("B", "C") == ["B", "C"]

    def test_bd(self):
        assert graph().find_path("B", "D") == ["B", "C", "D"]

    def test_be(self):
        assert graph().find_path("B", "E") == ["B", "C", "D", "E"]

    def test_ca(self):
        assert graph().find_path("C", "A") == ["C", "A"]

    def test_cb(self):
        assert graph().find_path("C", "B") == ["C", "A", "B"]

    def test_cd(self):
        assert graph().find_path("C", "D") == ["C", "D"]

    def test_ce(self):
        assert graph().find_path("C", "E") == ["C", "D", "E"]

    def test_da(self):
        assert graph().find_path("D", "A") == ["D", "E", "A"]

    def test_db(self):
        assert graph().find_path("D", "B") == ["D", "E", "A", "B"]

    def test_dc(self):
        assert graph().find_path("D", "C") == ["D", "E", "C"]

    def test_de(self):
        assert graph().find_path("D", "E") == ["D", "E"]

    def test_ea(self):
        assert graph().find_path("E", "A") == ["E", "A"]

    def test_eb(self):
        assert graph().find_path("E", "B") == ["E", "A", "B"]

    def test_ec(self):
        assert graph().find_path("E", "C") == ["E", "C"]

    def test_ed(self):
        assert graph().find_path("E", "D") == ["E", "C", "D"]

    def test_self_node(self):
        for node in graph().nodes:
            assert graph().find_path(node, node) == [node]

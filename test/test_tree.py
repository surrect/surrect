from unittest import TestCase

from surrect.scroll.tree import *


class TestNodeMethods(TestCase):
    def test_init(self):
        v = object()
        n = ScrollNode(NODE_ROOT, v)
        self.assertEqual(n.kind, NODE_ROOT)
        self.assertIs(n.value, v)
        self.assertRaises(ScrollNodeError, ScrollNode, "random", "foo")

    def test_eq(self):
        a = ScrollNode(NODE_TEXT, "hello!")
        b = ScrollNode(NODE_TEXT, "hello!")
        self.assertTrue(a == b)

    def test_copy(self):
        a = ScrollNode(NODE_TEXT, "hello!")
        a.nodes.append(ScrollNode(NODE_TEXT, "I'm a node!"))
        a.nodes.append(ScrollNode(NODE_BLANK, None))
        b = a.copy()
        self.assertIsNot(a, b)
        self.assertIs(a.kind, b.kind)
        self.assertIs(a.value, b.value)
        self.assertIsNot(a.nodes, b.nodes)
        self.assertEqual(a.nodes, b.nodes)
        for n in range(0, len(a.nodes)):
            self.assertIs(a.nodes[n], b.nodes[n])

    def test_deepcopy(self):
        a = ScrollNode(NODE_TEXT, "hello!")
        a.nodes.append(ScrollNode(NODE_TEXT, "I'm a node!"))
        a.nodes.append(ScrollNode(NODE_BLANK, None))
        b = a.deepcopy()
        self.assertIsNot(a, b)
        self.assertIs(a.kind, b.kind)
        self.assertIs(a.value, b.value)
        self.assertIsNot(a.nodes, b.nodes)
        self.assertEqual(a.nodes, b.nodes)
        for n in range(0, len(a.nodes)):
            self.assertIsNot(a.nodes[n], b.nodes[n])
            self.assertEqual(a.nodes[n], b.nodes[n])


class TestCollation(TestCase):
    def test_collect_nodes(self):
        nds = [ScrollNode(NODE_TEXT, str(i)) for i in range(0, 3)] + \
              [ScrollNode(NODE_BLANK, None)] + \
              [ScrollNode(NODE_TEXT, str(i)) for i in range(3, 6)]
        cnds = []
        gen = iter(nds)
        tail = collect_nodes(NODE_TEXT, cnds, gen)
        self.assertEqual(len(cnds), 3)
        self.assertIs(tail, nds[3], "tail incorrect")
        self.assertEqual(nds[4:], [n for n in gen], "remaining incorrect")

    def test_collate(self):
        def test_collator(nodes):
            ngen = (n.value for n in nodes)

            def coll(string):
                tstr = next(ngen)
                self.assertEqual(tstr, string)
                return string
            return " ", coll

        nds = [ScrollNode(NODE_TEXT, str(i)) for i in range(0, 3)] + \
              [ScrollNode(NODE_BLANK, None)] + \
              [ScrollNode(NODE_TEXT, str(i)) for i in range(3, 6)]

        collators = {
            NODE_TEXT: test_collator(nds[0:3] + nds[4:7])
        }

        root = ScrollNode(NODE_ROOT, None)
        root.nodes[:] = nds
        collate(root, collators=collators)
        self.assertEqual(len(root.nodes), 3)

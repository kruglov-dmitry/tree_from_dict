from collections import defaultdict


class Node(object):
    def __init__(self, term, node_id, parent_id, level, childs=[]):
        self.term = term
        self.node_id = node_id
        self.parent_id = parent_id
        self.childs = childs
        self.level = level

    def add_child(self, child):
        self.childs.append(child)

    def __str__(self):
        if self.childs:
            childs_terms = [o.term for o in self.childs]
        else:
            childs_terms = []
        res_str = " ".join([self.term, "CHILDS:" + str(childs_terms)])
        for b in range(0, self.level):
            res_str = "\t" + res_str
        return res_str


class Tree(object):
    def __init__(self, dict):
        self.ROOT_NODE = Node("ROOT", "ROOT", None, 0, [])
        self.__nodes = defaultdict(list)
        self.__nodes["ROOT"].append(self.ROOT_NODE)
        self.dict = dict

    def add_child(self, child, parent_term, parent_id):
        if parent_term not in self.__nodes:
            print parent_term, parent_id
            raise Exception()
        else:
            was_added = False
            if child.term in self.__nodes:
                was_added = False
                for b in self.__nodes[parent_term]:
                    if b.node_id == parent_id:
                        b.add_child(child)
                        was_added = True
                        count = 0
                        for z in b.childs:
                            if z.term == child.term:
                                count += 1
                        if count > 1:
                            self.print_tree()
                            raise Exception()
                        break
                if not was_added:
                    self.print_tree()
                    raise Exception()
            else:
                self.__nodes[child.term].append(child)
                for b in self.__nodes[parent_term]:
                    if b.node_id == parent_id:
                        b.add_child(child)
                        was_added = True
                        break
                if not was_added:
                    raise Exception()

    def build_tree(self):
        level = 1
        for key in self.dict:
            # note efficient but for represent idea
            new_node_id = str(level) + "_" + key + "_" + self.ROOT_NODE.node_id
            new_child = Node(key, new_node_id, self.ROOT_NODE.node_id, level, [])
            self.__nodes[key].append(new_child)
            self.add_child(new_child, self.ROOT_NODE.term, self.ROOT_NODE.node_id)
            self.build_by_dict(key, new_child, level)

    def build_by_dict(self, term, new_node, level):
        if term not in self.dict or len(self.dict[term]) == 0:
            return

        level += 1
        for w in self.dict[term]:
            new_node_id = str(level) + "_" + w + "_" + new_node.node_id
            even_new_node = Node(w, new_node_id, new_node.node_id, level, [])
            self.__nodes[w].append(even_new_node)
            self.add_child(even_new_node, new_node.term, new_node.node_id)
            self.build_by_dict(w, even_new_node, level)

    def print_child_nodes(self, node):
        for b in node.childs:
            print b
            self.print_child_nodes(b)

    def print_tree(self):
        print self.ROOT_NODE
        self.print_child_nodes(self.ROOT_NODE)

some_dict = {"a": ["b", "c", "d"], "b": ["c", "d"], "c": ["e"], "d": ["c"], "e": ["z"], "z": []}

my_tree = Tree(some_dict)
my_tree.build_tree()
my_tree.print_tree()

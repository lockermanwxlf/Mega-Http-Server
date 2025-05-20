from mega import MegaNodeList, MegaNode

def mega_node_list_iter(self: MegaNodeList) -> MegaNodeList:
    self._iter_index = 0
    return self
    
def mega_node_list_next(self: MegaNodeList) -> MegaNode:
    node = self.get(self._iter_index)
    self._iter_index += 1
    if node is None:
        raise StopIteration
    return node

MegaNodeList.__iter__ = mega_node_list_iter
MegaNodeList.__next__ = mega_node_list_next

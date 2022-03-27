import functools as fn
from typing import Union, Any


class SearchTree():
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def member(self, x):
        if self is None:
            return False

        if x == self.value:
            return self

        if x > self.value:
            if self.right is None:
                return False
            return self.right.member(x)

        if self.left is None:
            return False
        return self.left.member(x)

    def min(self):
        if self.left is None:
            return self.value
        return self.left.min()

    def max(self):
        if self.right is None:
            return self.value
        return self.right.max()

    def insert(self, x):
        if x == self.value:
            return
        if x > self.value:
            if self.right is not None:
                self.right.insert(x)
            else:
                u = SearchTree(x, parent=self)
                self.right = u
        else:
            if self.left is not None:
                self.left.insert(x)
            else:
                u = SearchTree(x, parent=self)
                self.left = u

    def sucssesor(self, x, from_r=False):
        if x.right is not None and not from_r:
            x = x.right
            while x.left is not None:
                x = x.left
            return x
        else:
            # אם אני בן שמאלי של אבי
            if x.parent.left is not None and x.parent.left.value == x.value:
                return x.parent
            else:
                # בן ימני של אבי
                if x.parent.value == self.value:  # הגעתי לשורש
                    return False
                return self.sucssesor(x.parent, True)

    def delete(self, x):
        ptr = self.member(x)
        parent = ptr.parent
        if ptr is False:
            return
        # leaf
        if ptr.left is None and ptr.right is None:
            if not parent:
                self = None
            else:
                if parent.left and parent.left.value == ptr.value:
                    parent.left = None
                else:
                    parent.right = None
            return
        # only has left son
        if ptr.left is not None and ptr.right is None:
            if not parent:
                self.value = ptr.left.value
                self.left = ptr.left.left
            else:
                if parent.left and parent.left.value == ptr.value:
                    parent.left = ptr.left
                else:
                    parent.right = ptr.left
            return
        # only has right son
        if ptr.right is not None and ptr.left is None:
            if not parent:
                self.value = ptr.right.value
                self.right = ptr.right.right
            else:
                if parent.left and parent.left.value == ptr.value:
                    parent.left = ptr.right
                else:
                    parent.right = ptr.right
            return
        # full parent
        s = self.sucssesor(ptr)
        if not parent:
            self.value = s.value
            if s.right:
                s.parent.left = s.right
            else:
                s.parent.left = None
        else:
            ptr.value = s.value
            if s.right:
                ptr.right = s.right.right
            else:
                ptr.right = None


def printBTree(node, nodeInfo=None, inverted=False, isTop=True):

   # node value string and sub nodes
   stringValue, leftNode, rightNode = str(node.value), node.left, node.right

   stringValueWidth  = len(stringValue)

   # recurse to sub nodes to obtain line blocks on left and right
   leftTextBlock     = [] if not leftNode else printBTree(leftNode,nodeInfo,inverted,False)

   rightTextBlock    = [] if not rightNode else printBTree(rightNode,nodeInfo,inverted,False)

   # count common and maximum number of sub node lines
   commonLines       = min(len(leftTextBlock),len(rightTextBlock))
   subLevelLines     = max(len(rightTextBlock),len(leftTextBlock))

   # extend lines on shallower side to get same number of lines on both sides
   leftSubLines      = leftTextBlock  + [""] *  (subLevelLines - len(leftTextBlock))
   rightSubLines     = rightTextBlock + [""] *  (subLevelLines - len(rightTextBlock))

   # compute location of value or link bar for all left and right sub nodes
   #   * left node's value ends at line's width
   #   * right node's value starts after initial spaces
   leftLineWidths    = [ len(line) for line in leftSubLines  ]
   rightLineIndents  = [ len(line)-len(line.lstrip(" ")) for line in rightSubLines ]

   # top line value locations, will be used to determine position of current node & link bars
   firstLeftWidth    = (leftLineWidths   + [0])[0]
   firstRightIndent  = (rightLineIndents + [0])[0]

   # width of sub node link under node value (i.e. with slashes if any)
   # aims to center link bars under the value if value is wide enough
   #
   # ValueLine:    v     vv    vvvvvv   vvvvv
   # LinkLine:    / \   /  \    /  \     / \
   #
   linkSpacing       = min(stringValueWidth, 2 - stringValueWidth % 2)
   leftLinkBar       = 1 if leftNode  else 0
   rightLinkBar      = 1 if rightNode else 0
   minLinkWidth      = leftLinkBar + linkSpacing + rightLinkBar
   valueOffset       = (stringValueWidth - linkSpacing) // 2

   # find optimal position for right side top node
   #   * must allow room for link bars above and between left and right top nodes
   #   * must not overlap lower level nodes on any given line (allow gap of minSpacing)
   #   * can be offset to the left if lower subNodes of right node
   #     have no overlap with subNodes of left node
   minSpacing        = 2
   rightNodePosition = fn.reduce(lambda r,i: max(r,i[0] + minSpacing + firstRightIndent - i[1]), \
                                 zip(leftLineWidths,rightLineIndents[0:commonLines]), \
                                 firstLeftWidth + minLinkWidth)

   # extend basic link bars (slashes) with underlines to reach left and right
   # top nodes.
   #
   #        vvvvv
   #       __/ \__
   #      L       R
   #
   linkExtraWidth    = max(0, rightNodePosition - firstLeftWidth - minLinkWidth )
   rightLinkExtra    = linkExtraWidth // 2
   leftLinkExtra     = linkExtraWidth - rightLinkExtra

   # build value line taking into account left indent and link bar extension (on left side)
   valueIndent       = max(0, firstLeftWidth + leftLinkExtra + leftLinkBar - valueOffset)
   valueLine         = " " * max(0,valueIndent) + stringValue
   slash             = "\\" if inverted else  "/"
   backslash         = "/" if inverted else  "\\"
   uLine             = "¯" if inverted else  "_"

   # build left side of link line
   leftLink          = "" if not leftNode else ( " " * firstLeftWidth + uLine * leftLinkExtra + slash)

   # build right side of link line (includes blank spaces under top node value)
   rightLinkOffset   = linkSpacing + valueOffset * (1 - leftLinkBar)
   rightLink         = "" if not rightNode else ( " " * rightLinkOffset + backslash + uLine * rightLinkExtra )

   # full link line (will be empty if there are no sub nodes)
   linkLine          = leftLink + rightLink

   # will need to offset left side lines if right side sub nodes extend beyond left margin
   # can happen if left subtree is shorter (in height) than right side subtree
   leftIndentWidth   = max(0,firstRightIndent - rightNodePosition)
   leftIndent        = " " * leftIndentWidth
   indentedLeftLines = [ (leftIndent if line else "") + line for line in leftSubLines ]

   # compute distance between left and right sublines based on their value position
   # can be negative if leading spaces need to be removed from right side
   mergeOffsets      = [ len(line) for line in indentedLeftLines ]
   mergeOffsets      = [ leftIndentWidth + rightNodePosition - firstRightIndent - w for w in mergeOffsets ]
   mergeOffsets      = [ p if rightSubLines[i] else 0 for i,p in enumerate(mergeOffsets) ]

   # combine left and right lines using computed offsets
   #   * indented left sub lines
   #   * spaces between left and right lines
   #   * right sub line with extra leading blanks removed.
   mergedSubLines    = zip(range(len(mergeOffsets)), mergeOffsets, indentedLeftLines)
   mergedSubLines    = [ (i,p,line + (" " * max(0,p)) )       for i,p,line in mergedSubLines ]
   mergedSubLines    = [ line + rightSubLines[i][max(0,-p):]  for i,p,line in mergedSubLines ]

   # Assemble final result combining
   #  * node value string
   #  * link line (if any)
   #  * merged lines from left and right sub trees (if any)
   treeLines = [leftIndent + valueLine] + ( [] if not linkLine else [leftIndent + linkLine] ) + mergedSubLines

   # invert final result if requested
   treeLines = reversed(treeLines) if inverted and isTop else treeLines

   # return intermediate tree lines or print final result
   if isTop : print("\n".join(treeLines))
   else     : return treeLines


tree = SearchTree(10)
tree.insert(12)
tree.insert(2)
tree.insert(5)
tree.insert(15)
tree.insert(13)
tree.insert(11)
tree.insert(4)
tree.insert(3)
printBTree(tree)
tree.delete(2)
printBTree(tree)



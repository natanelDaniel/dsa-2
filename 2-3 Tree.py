
class Tree_2_3():
    def __init__(self, value, left=None, middle=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.middle = middle
        self.right = right
        self.parent = parent

    def member(self, x):
        if self is None:
            return False

        if type(self.value) is int:
            if x == self.value:
                return self
            else:
                return False
        if x < self.value[0]:
            return False
        if self.value[1] > x >= self.value[0]:
            if self.left is None:
                return False
            return self.left.member(x)
        if (self.value[2] !='-' and self.value[2] > x >= self.value[1]) or (self.value[2] =='-' and x >= self.value[1]):
            if self.middle is None:
                return False
            return self.middle.member(x)
        if self.right is None:
            return False
        return self.right.member(x)

    def min(self):
        return self.value[0]

    def max(self):
        if type(self.value) is int:
            return self.value
        if self.right:
            return self.right.max()
        if self.middle:
            return self.middle.max()
        return self.left.max()

    def member_parent(self, x):
        if type(self.left.value) is int:
            return self
        if x < self.value[1]:
            return self.left.member_parent(x)
        if (self.value[2] != "-" and self.value[2] > x >= self.value[1]) or (self.value[2] == "-" and x >= self.value[1]):
            return self.middle.member_parent(x)
        return self.right.member_parent(x)

    # function for plot
    def array_tree(self,root_val, rows=[], h=0, f=''):
        if self is None:
            return
        if self.value == root_val:
            rows.append([self.value])
        else:
            if len(rows) == h:
                rows.append([(self.value,f)])
            else:
                rows[h].append((self.value,f))
        if self.left:
            rows = self.left.array_tree(root_val, rows, h+1, 'L')
        if self.middle:
            rows = self.middle.array_tree(root_val, rows, h+1, "M")
        if self.right:
            rows = self.right.array_tree(root_val, rows, h+1, "R")

        return rows


def print_tree(tree):
    rows = []
    rows = tree.array_tree(root_val=tree.value, rows=[])
    last_row_len = len(rows[-1])
    if True:
        print(" "*(len(rows)*2+2), end="")
        if len(rows) > 2:
            print(" "*(len(rows)*5), end="")
        print(rows[0][0])

    for r in range(1, 2*len(rows) -1):
        if r%2==0:
            if r//2 != len(rows) - 1:
                for item in rows[r//2]:
                    if item[1] == "L":
                        print(" ", end="")
                    print(" "*(2*len(rows)-r)+str(item[0]), end=" ")
            else:
                for item in rows[r // 2]:
                    if item[1] == "L":
                        print("  ", end="")
                    print(" " * (2 * len(rows) - r +1) + str(item[0]), end=" ")

        else:
            link = []
            for i in rows[(r+1)//2]:
                if i[1] == 'L':
                    link.append('/')
                if i[1] == "M":
                    link.append('|')
                if i[1] == "R":
                    link.append("\\")
            if r//2 != len(rows) - 2:
                for l in link:
                    if l=="/":
                        print("  ", end="")
                    print("  "*(2*len(rows)-r)+ l, end=" ")
            else:
                for l in link:
                    if l=="/":
                        print("  ", end="")
                    print(" "*(2*len(rows)-r)+ l, end=" ")
        print()
    print()


def insert_up(tree, parent,  p1, p2):
    # we reach the root
    if parent is None:
        tree = Tree_2_3((p1.value[0], p2.value[0], "-"), left=p1, middle=p2)
        p1.parent = tree
        p2.parent = tree
        return tree
    # parent has open place at right
    if parent.right is None:
        if p1 is parent.middle:
            parent.right = p2
            p2.parent = parent
            parent.value = parent.value[0], parent.value[1], p2.value[0]
            return tree
        parent.right = parent.middle
        parent.middle = p2
        p2.parent = parent
        parent.value = p1.value[0], p2.value[0], parent.value[1]
        while parent.parent:
            parent = parent.parent
            parent.value = parent.left.value[0], parent.value[1],parent.value[2]
        return tree
    if p1 is parent.right:
        new_p2 = Tree_2_3((p1.value[0], p2.value[0], "-"), left=p1, middle=p2)
        p1.parent = new_p2
        p2.parent = new_p2
        parent.right = None
        parent.value = parent.value[0], parent.value[1], "-"
        return insert_up(tree, parent.parent, parent, new_p2)
    if p1 is parent.middle:
        new_p2 = Tree_2_3((p2.value[0], parent.right.value[0], "-"), left=p2, middle=parent.right)
        parent.right.parent = new_p2
        p2.parent = new_p2
        parent.right = None
        parent.value = parent.value[0], parent.value[1], "-"
        return insert_up(tree, parent.parent, parent, new_p2)
    new_p2 = Tree_2_3((parent.middle.value[0], parent.right.value[0], "-"), left=parent.middle, middle=parent.right)
    parent.right.parent = new_p2
    parent.middle.parent = new_p2
    parent.right = None
    parent.middle = p2
    p2.parent = parent
    parent.value = parent.value[0], p2.value[0], "-"
    return insert_up(tree, parent.parent, parent, new_p2)


def insert(tree, x):
    p = tree.member_parent(x)
    # only 2 child
    if p.right is None:
        if x > p.middle.value:
            p.right = Tree_2_3(x, parent=p)
            p.value = p.value[0], p.value[1], x
            return tree
        if p.left.value < x <= p.middle.value:
            p.right = p.middle
            p.middle = Tree_2_3(x, parent=p)
            p.value = p.value[0], x, p.value[1]
            return tree
        p.right, p.middle = p.middle, p.left
        p.left = Tree_2_3(x, parent=p)
        p.value = x, p.value[0], p.value[1]
        while p.parent is not None:
            p = p.parent
            p.value = p.left.value[0], p.middle.value[0], p.value[2]
        return tree
    # 3 child
    else:
        #
        if x > p.middle.value:
            if x > p.right.value:
                p_1 = Tree_2_3((p.right.value, x, "-"))
                p.right.parent = p_1
                p_1.left = p.right
                p_1.middle = Tree_2_3(x, parent=p_1)
            else:
                p_1 = Tree_2_3((x, p.right.value, "-"))
                p.right.parent = p_1
                p_1.left = Tree_2_3(x, parent=p_1)
                p_1.middle = p.right
            p.right = None
            p.value = p.value[0], p.value[1], "-"
        else:
            p_1 = Tree_2_3((p.middle.value, p.right.value, "-"), left=p.middle, middle=p.right)
            p.middle.parent = p_1
            p.right.parent = p_1
            p.right = None
            if x > p.left.value:
                p.middle = Tree_2_3(x, parent=p)
                p.value = p.value[0], x, "-"

            else:
                p.middle = p.left
                p.left = Tree_2_3(x, parent=p)
                p.value = x, p.value[0], "-"
        return insert_up(tree,p.parent,  p, p_1)


def delete(tree, x):
    p = tree.member_parent(x)
    if p.right:
        if x == p.right.value:
            p.right.parent = None
            p.right = None
            p.value = p.value[0], p.value[1], "-"
            return tree
        if x == p.middle.value:
            p.middle.parent = None
            p.middle = p.right
            p.right = None
            p.value = p.value[0], p.value[2], "-"
            return tree
        p.left.parent = None
        p.left = p.middle
        p.middle = p.right
        p.right = None
        p.value = p.value[1], p.value[2], "-"
        while p.parent and p.parent.value[0] == x:
            p = p.parent
            p.value = p.left.value[0], p.value[1], p.value[2]
        if p.parent:
            p = p.parent
            if p.value[1] == x:
                p.value = p.value[0], p.middle.value[0], p.value[2]
            else:
                p.value = p.value[0], p.value[1], p.right.value[0]
        return tree

    else:
        if p is tree:
            print("cant leave tree with 1 child")
            return tree
        else:
            if x == p.middle.value:
                p.middle.parent = None
                p.middle = None
                p.value = p.value[0], '-', '-'
            else:
                p.left.parent = None
                p.left = p.middle
                p.value = p.value[1], '-', '-'
                temp = p
                while temp.parent and temp.parent.value[0] == x:
                    temp = temp.parent
                    temp.value = temp.left.value[0], temp.value[1], temp.value[2]
                if temp.parent:
                    temp = temp.parent
                    if temp.value[1] == x:
                        temp.value = temp.value[0], temp.middle.value[0], temp.value[2]
                    else:
                        temp.value = temp.value[0], temp.value[1], temp.right.value[0]
            return delete_up(tree, p)


def delete_up(tree, p):
    parent = p.parent
    if parent:
        # come from right
        if p is parent.right:
            if parent.middle.right:
                p.middle = p.left
                parent.middle.right.parent = p
                p.left = parent.middle.right
                if type(p.left.value) is int:
                    p.value = p.left.value, p.value[0], p.value[2]
                else:
                    p.value = p.left.value[0], p.value[0], p.value[2]
                parent.middle.value = parent.middle.value[0], parent.middle.value[1], '-'
                parent.value = parent.value[0], parent.value[1], p.value[0]
                return tree
            parent.middle.right = p.left
            p.left.parent = parent.middle
            parent.right = None
            parent.value = parent.value[0], parent.value[1], '-'
            parent.middle.value = parent.middle.value[0], parent.middle.value[1], p.value[0]
            p = None
            return tree
        else:
            # there is 3 children for parent
            if parent.right:
                if p is parent.middle:
                    if parent.right.right:
                        p.middle = parent.right.left
                        p.middle.parent = p
                        parent.right.left = parent.right.middle
                        parent.right.middle = parent.right.right
                        if type(p.left.value) is int:
                            p.value = p.value[0], p.middle.value, p.value[2]
                        else:
                            p.value = p.value[0], p.middle.value[0], p.value[2]
                        parent.right.value = parent.right.value[1], parent.right.value[2], '-'
                        parent.value = parent.value[0], parent.value[1], parent.right.value[0]
                        return tree
                    else:
                        if parent.left.right:
                            p.middle = p.left
                            p.left = parent.left.right
                            p.left.parent = p
                            parent.left.right = None
                            if type(p.left.value) is int:
                                p.value = p.left.value, p.middle.value, p.value[2]
                            else:
                                p.value = p.left.value[0], p.middle.value[0], p.value[2]
                            parent.left.value = parent.left.value[0], parent.left.value[1], '-'
                            parent.value = parent.value[0], p.value[0], parent.value[2]
                            return tree
                        p.middle = parent.right.left
                        p.middle.parent = p
                        p.right = parent.right.middle
                        p.right.parent = p
                        parent.right = None
                        if type(p.left.value) is int:
                            p.value = p.value[0], p.middle.value, p.right.value
                        else:
                            p.value = p.value[0], p.middle.value[0], p.right.value[0]
                        parent.value = parent.value[0], parent.value[1], '-'
                        return tree
                if p is parent.left:
                    if parent.middle.right:
                        p.middle = parent.middle.left
                        p.middle.parent = p
                        parent.middle.left = parent.middle.middle
                        parent.middle.middle = parent.middle.right
                        parent.middle.right = None
                        if type(p.left.value) is int:
                            p.value = p.left.value, p.middle.value, p.value[2]
                        else:
                            p.value = p.left.value[0], p.middle.value[0], p.value[2]
                        parent.middle.value = parent.middle.value[1], parent.middle.value[2], '-'
                        parent.value = parent.value[0], parent.middle.value[1], parent.value[2]
                        return tree
                    else:
                        p.middle = parent.middle.left
                        p.middle.parent = p
                        p.right = parent.middle.middle
                        p.right.parent = p
                        parent.middle = parent.right
                        parent.right = None
                        if type(p.left.value) is int:
                            p.value = p.left.value, p.middle.value, p.right.value
                        else:
                            p.value = p.left.value[0], p.middle.value[0], p.right.value[0]
                        parent.value = parent.value[0], parent.value[2], '-'
                        return tree
            # only 2 child to parent
            else:
                if p is parent.middle:
                    if parent.left.right:
                        p.middle = p.left
                        p.left  = parent.left.right
                        p.left.parent = p
                        parent.left.right = None
                        if type(p.left.value) is int:
                            p.value = p.left.value, p.middle.value, '-'
                        else:
                            p.value = p.left.value[0], p.middle.value[0], '-'
                        parent.left.value = parent.left.value[0], parent.left.value[1], '-'
                        parent.value = parent.value[0], p.value[0], '-'
                        return tree
                    else:
                        parent.left.right = p.left
                        parent.left.right.parent = parent.left
                        parent.middle = None
                        if type(p.left.value) is int:
                            parent.left.value = parent.left.value[0], parent.left.value[1], parent.left.right.value
                        else:
                            parent.left.value = parent.left.value[0], parent.left.value[1], parent.left.right.value[0]
                        parent.value = parent.value[0], '-', '-'
                        if parent.parent:
                            return delete_up(tree, parent)
                        parent.left.parent = None
                        return parent.left

                else:
                    if parent.middle.right:
                        p.middle = parent.middle.left
                        parent.middle.left = parent.middle.middle
                        parent.middle.middle = parent.middle.right
                        p.middle.parent = p
                        parent.middle.right = None
                        if type(p.left.value) is int:
                            p.value = p.left.value, p.middle.value, '-'
                            parent.middle.value = parent.middle.left.value, parent.middle.middle.value, '-'
                        else:
                            p.value = p.left.value[0], p.middle.value[0], '-'
                            parent.middle.value = parent.middle.left.value[0], parent.middle.middle.value[0], '-'
                        parent.value = parent.value[0], parent.middle.value[0], '-'
                        return tree
                    else:
                        p.middle = parent.middle.left
                        p.middle.parent = p
                        p.right = parent.middle.middle
                        p.right.parent = p
                        parent.middle = None
                        if type(p.left.value) is int:
                            p.value = p.value[0], p.middle.value, p.right.value
                        else:
                            p.value = p.value[0], p.middle.value[0], p.right.value[0]
                        parent.value = parent.value[0], '-', '-'
                        if parent.parent:
                            return delete_up(tree, parent)
                        parent.left.parent = None
                        return parent.left


def manu():
    root = Tree_2_3((2, 7, "-"))
    root.left = Tree_2_3(2, parent=root)
    root.middle = Tree_2_3(7, parent=root)
    tree = root
    print_tree(tree)
    key = -1
    while key!=8:
        print("    manu:\n1)print tree\n2)member\n3)min\n4)max\n5)insert\n6)delete\n7)initialize new tree\n8)quit\nEnter nuber:")
        key = int(input())
        if key==1:
            print_tree(tree)
        if key==2:
            print("enter number to find:")
            x = int(input())
            f = tree.member(x)
            if f:
                print("{} in tree".format(x))
            else:
                print("{} not in tree".format(x))
        if key==3:
            print("min: ",tree.min())
        if key==4:
            print("max: ", tree.max())
        if key==5:
            print("enter number to insert:")
            x = int(input())
            f = tree.member(x)
            if f:
                print("{} already in tree".format(x))
            else:
                tree = insert(tree, x)
                print_tree(tree)
        if key==6:
            print("enter number to delete:")
            x = int(input())
            f = tree.member(x)
            if f:
                tree = delete(tree, x)
                print_tree(tree)
            else:
                print("{} not in tree".format(x))
        if key==7:
            print("enter value 1:")
            x = int(input())
            print("enter value 2:")
            y = int(input())
            root = Tree_2_3((min(x,y), max(x,y), "-"))
            root.left = Tree_2_3(min(x,y), parent=root)
            root.middle = Tree_2_3(max(x,y), parent=root)
            tree = root
            print_tree(tree)
        if key == 8:
            break


if __name__ == '__main__':
    manu()

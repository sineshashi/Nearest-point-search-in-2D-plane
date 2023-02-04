import random, math
from typing import Optional, Any
from sklearn.neighbors import KDTree


arr = []

for _ in range(10000):
    arr.append((random.randint(-1000, 1000), random.randint(-1000, 1000)))


def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def linear_search(point):
    '''Searches closest point using linear search.'''
    min_point, min_dis = (0, 0), float('inf')

    for p in arr:
        dis = distance(p, point)
        if dis < min_dis:
            min_point, min_dis = p, dis
    return min_point

class BinaryTree:
    def __init__(self, val:int, other: Any=None, left:Optional["BinaryTree"]=None, right: Optional["BinaryTree"]=None):
        self.val = val
        self.left = left
        self.right = right
        self.other = other

    def insert(self, val: int, other: Any=None):
        if val < self.val:
            if self.left is not None:
                self.left.insert(val, other)
            else:
                self.left = BinaryTree(val, other)
        else:
            if self.right is not None:
                self.right.insert(val, other)
            else:
                self.right = BinaryTree(val, other)

    def pre_order(self, node):
        if node is None:
            return
        self.pre_order(node.left)
        print(node.val)
        self.pre_order(node.right)
    

'''
    First I was thinking to search using the recatangle around the given point. If there is any point inside that rectangle
    I will use that point to form a new rectangle and repeat that but there was flaw in the approach, OUT SIDE RECTANGLE CLOSEST
    POINT MAY LIE.
    This lead me to the use of SQUARE which ensures that closest point must lie in the region and because of using square, I needed a
    single binary tree on x-coordinate.
'''
long_binary_tree = None

for (x, y) in arr:
    if long_binary_tree is None:
        long_binary_tree = BinaryTree(x, other=y)
    else:
        long_binary_tree.insert(x, y)

# long_binary_tree.pre_order(long_binary_tree)

visited = set()
def x_range_search(d: float, min_x: int, max_x: int, point, node:Optional[BinaryTree]=long_binary_tree):
    if node is None:
        return
    x = node.val
    y = node.other

    if (x, y) not in visited:
        visited.add((x, y)) #Making sure that we do not calculate those distances again and again.
        cnt_dis = distance((x,y), point)
        if cnt_dis < d:
            return (x, y)

    if x < min_x:
        #If x is below the range then solution will lie in right tree.
        return x_range_search(d, min_x, max_x, point, node.right)
    if x > max_x:
        #If x is above the range then solution will lie in left tree.
        return x_range_search(d, min_x, max_x, point, node.left)
    
    #In case of x is in the range, try both left and right to check whether there is any desired point in the square.
    ans = x_range_search(d, min_x, max_x, point, node.left)
    if ans is None:
        ans = x_range_search(d, min_x, max_x, point, node.right)
    return ans

def binary_search_closest_point(point):
    '''
    Should have O(log(n)*log(n)) runtime but binary search tree is not balanced. A Balanced binary search tree will provide this runtime.
    '''
    pre_dis = float('inf')
    pre_pt = None
    cnt_pt = (float('inf'), float('inf'))
    while True:
        if cnt_pt is None:
            break
        cnt_dis = distance(cnt_pt, point)
        if cnt_dis < pre_dis:
            pre_dis = cnt_dis
        #Now searching in the square around the given point if there is any point inside the squre with distance less than cnt_dis.
        pre_pt, cnt_pt = cnt_pt, x_range_search(cnt_dis, point[0]-cnt_dis, point[0]+cnt_dis, point)
    return pre_pt

'''
Since we are continuously searching if there is any point inside the square, we can use a 2d rtree(range tree)
instead of binary search tree to search in the square, which can make it more faster.

But the most efficient way to do this, is use of kd trees.
'''

kd_tree = KDTree(arr, leaf_size=30, metric='euclidean')

def kd_tree_search(point):
    _, idx = kd_tree.query([point],k=1)
    return arr[idx[0][0]]


for _ in range(10):
    print("...............................")
    point = (random.randint(-1000, 1000), random.randint(-1000, 1000))
    print("Input Point: ", point)
    ans_point = linear_search(point)
    print("Linear Search:")
    print("       Point: ", ans_point)
    print("       Distance: ", distance(point, ans_point))
    ans_point = binary_search_closest_point(point)
    print("Binary Search:")
    print("       Point: ", ans_point)
    print("       Distance: ", distance(point, ans_point))
    ans_point = kd_tree_search(point)
    print("KD tree Search:")
    print("       Point: ", ans_point)
    print("       Distance: ", distance(point, ans_point))
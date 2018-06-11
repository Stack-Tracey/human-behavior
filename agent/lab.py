import numpy as np


objects = [5, 5, 4, 4, 2, 2, 5, 5, 5, 5, 5]

def get_bounding_box(x):  # bbox = get_bounding_box() , shape = transform.rotate(bbox, z_angle_degree)#############
    mask = x == 0
    bbox = []
    all_axis = np.arange(x.ndim)
    print("all_axis", all_axis)
    for kdim in all_axis:
        nk_dim = np.delete(all_axis, kdim)
        print("nk_dim", nk_dim)
        mask_i = mask.all(axis=tuple(nk_dim))
        print("mask_i", mask_i)
        dmask_i = np.diff(mask_i)
        print("dmask", dmask_i)
        idx_i = np.nonzero(dmask_i)[0]
        print("idx_i", idx_i)
        if len(idx_i) != 2:
            raise ValueError('Algorithm failed, {} does not have 2 elements!'.format(idx_i))
        bbox.append(slice(idx_i[0] + 1, idx_i[1] + 1))
    return bbox

nodes = []

for obj in objects:
                #obs_transit = np.ndarray([self.field_x_size, self.field_y_size, self.field_z_size])
    x = y = z = x_size = y_size = z_size = radius = z_angle_deg = slowdown_fac = visibility = geometric_type = obj
    val = []
    field = np.zeros([20, 20])
    field2 = np.zeros([20, 20])

    print("here comes obs", obj)

    x_size = round(x_size / 2)
    y_size = round(y_size / 2)
    z_size = round(z_size / 2)
    print("here comes single values", x, y, z, x_size, y_size, z_size, z_angle_deg, slowdown_fac,
                          visibility, geometric_type)

    l = x - x_size
    if l == 0:
        l = l + 1
    r = x + x_size + 1
    if r == 0:
        r = l + 1
    u = y - y_size
    if u == 0:
        u = u + 1
    o = y + y_size + 1
    if o == 0:
        o = o + 1
    v = z - z_size
    h = z + z_size

    print("calculated values", l, r, u, o)

    field[l:r, u:o] = 1.
    print("field", field.astype(int))
    #print("feld mit obstacle", (field != 0).astype(int))
    idx_1 = np.nonzero(field)
    print("here comes idsx 1", idx_1)
    min_x_cent = []
    min_y_cent = []
    max_x_cent = []
    max_y_cent = []
    idx_min = []
    idx_max = []


    for i in idx_1[0]:
        i = i - x
        min_x_cent.append(i)
    print("here comes min x cent", min_x_cent)
    idx_min.append(min_x_cent)
    for i in idx_1[1]:
        i = i - y
        min_y_cent.append(i)
    print("here comes min y cent", min_y_cent)
    idx_min.append(min_y_cent)
    print("here comes idsx min", idx_min)
    A = np.matrix(idx_min)
    print("here comes A", A)

                    #creating a rotation matrix R
    theta = np.radians(139)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))

    print("shapes", A.shape, R.shape)
    M = np.round(R * A)
    print("here comes rounded M ", M)

    m_list = np.asarray(M)
    print("here comes  list", m_list)
    for i in m_list[0]:
        i = i + x
        max_x_cent.append(i)
    idx_max.append(max_x_cent)
    for i in m_list[1]:
        i = i + y
        max_y_cent.append(i)
    idx_max.append(max_y_cent)

    i = 0
    for x in idx_max[0]:
        y = idx_max[1][i]
        field2[x, y] = 1
        i = i + 1
    print("here comes field2", field2.astype(int))
    bbox = get_bounding_box(field2)
    print("here comes bbox", (field2[bbox] != 0).astype(int))
    nodes.append(bbox)
    #ndimage.rotate(field, 70, output=obs_transit, reshape=False, mode='constant')
    print("here is the node list: nodes", nodes)

#######################################################################################################################

# Enter your code here. Read input from STDIN. Print output to STDOUT
class Node:
    def __init__(self, value, point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other):
        return 0 if self.value == '.' else 1


def children(point, grid):
    x, y = point.point
    links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
    return [link for link in links if link.value != '%']


def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1] - point2.point[0])


def aStar(start, goal, grid):
    # The open and closed sets
    openset = set()
    closedset = set()
    # Current point is the starting point
    current = start
    # Add the starting point to the open set
    openset.add(current)
    # While the open set is not empty
    while openset:
        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o: o.G + o.H)
        # If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        # Remove the item from the open set
        openset.remove(current)
        # Add it to the closed set
        closedset.add(current)
        # Loop through the node's children/siblings
        for node in children(current, grid):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue
            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                # Set the parent to our current item
                node.parent = current
                # Add it to the set
                openset.add(node)
    # Throw an exception if there is no path
    raise ValueError('No Path Found')


def next_move(pacman, food, grid):
    # Convert all the points to instances of Node
    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            grid[x][y] = Node(grid[x][y], (x, y))
    # Get the path
    path = aStar(grid[pacman[0]][pacman[1]], grid[food[0]][food[1]], grid)
    # Output the path
    print
    len(path) - 1
    for node in path:
        x, y = node.point
        print
        x, y


pacman_x, pacman_y = [int(i) for i in raw_input().strip().split()]
food_x, food_y = [int(i) for i in raw_input().strip().split()]
x, y = [int(i) for i in raw_input().strip().split()]

grid = []
for i in xrange(0, x):
    grid.append(list(raw_input().strip()))

next_move((pacman_x, pacman_y), (food_x, food_y), grid)
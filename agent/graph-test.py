
import numpy as np
from scipy import ndimage


obstacles = [[5, 5, 0, 4, 4, 0, 45, 1, 1, 1], [10, 10, 0, 2, 2, 0, 120, 1, 1, 1]]
targets = [[8, 8, 0, 0, 4, 0], [3, 3, 0, 0, 4, 0]]
#ball = ball
field_x_size = 20
field_y_size = 20
field_z_size = 500
field2 = np.zeros([field_x_size, field_y_size])
tile_size = field_x_size / 4
#field = np.zeros([field_x_size, field_y_size, field_z_size])
obs_trans = []

print("1 her are the obstacles", obstacles)
###Calculates the bounding box of a ndarray
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

def get_nodes(objects):######################################################################################
    #field = np.empty([field_x_size, field_y_size, field_z_size])
    nodes = []
    print("reached objects", objects)
    j = 0
    for obj in objects:
        #obs_transit = np.ndarray([field_x_size, field_y_size, field_z_size])
        x = y = z = x_size = y_size = z_size = radius = z_angle_deg = slowdown_fac = visibility = geometric_type = 0
        val = []
        field = np.zeros([field_x_size, field_y_size])
        marker = 1.
        if len(obj) < 7:
            print("here comes tar", obj)
            x, y, z, z_size, radius, amount = obj
            radius = radius / 2

            x_size = round(radius / 2)
            y_size = round(radius / 2)
            z_size = round(z_size / 2)
            marker = 2.
        else:
            print("here comes obs", obj)
            x, y, z, x_size, y_size, z_size, z_angle_deg, slowdown_fac, visibility, geometric_type = obj
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
        field[l:r, u:o], field2[l:r, u:o]  = marker
        print("here comes field", field)
        if marker == 2.:
            bbox = get_bounding_box(field)
            print("here comes bbox", (field[bbox] != 0).astype(int))
            nodes.append(bbox)
        else:
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
                print("here comes idx[0]", idx_1[0])
                print("here comes i, x", i, x)
                i = i - x
                print("here comes i after calc", i)
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
            print("here comes z angle degree", z_angle_deg)

            theta = np.radians(z_angle_deg)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c, -s), (s, c)))

            print("shapes and zangl degree", A.shape, R. shape, z_angle_deg)
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
                field2[x, y] = marker
                i = i + 1

            print("transformation", m_list.astype(int))
            bbox = get_bounding_box(field2)
            print("here comes bbox", (field2[bbox] != 0).astype(int))
            nodes.append(bbox)
            j = j + 1
            #ndimage.rotate(field, 70, output=obs_transit, reshape=False, mode='constant')
    print("here is the node list: nodes", nodes)
    return nodes

obs_nodes = get_nodes(obstacles)
print("here is the node list obstacles", obs_nodes)
tar_nodes = get_nodes(targets)
print("here is the node list targets", tar_nodes)
#tar_nodes = get_nodes(targets)
#print("here is the node list targets", tar_nodes)
# print("obs", obs.astype(int))

# print((obs!=0).astype(int))

get_nodes(obstacles)
get_nodes(targets)
print("here is field2", field2)
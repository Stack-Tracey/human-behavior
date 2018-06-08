
import numpy as np
from scipy import ndimage


class Graph:
    def __init__(self, obstacles, targets, ball):
        self.obstacles = obstacles
        self.targets = targets
        self.ball = ball
        self.field_x_size = 1024
        self.field_y_size = 768
        self.field_z_size = 500
        self.tile_size = self.field_x_size / 4
        #self.field = np.zeros([self.field_x_size, self.field_y_size, self.field_z_size])
        self.obs_trans = []

        print("1 her are the obstacles", self.obstacles)
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

        def get_nodes(self, objects):######################################################################################
            #field = np.empty([self.field_x_size, self.field_y_size, self.field_z_size])
            nodes = []
            print("reached objects", objects)
            for obj in objects:
                #obs_transit = np.ndarray([self.field_x_size, self.field_y_size, self.field_z_size])
                x = y = z = x_size = y_size = z_size = radius = z_angle_deg = slowdown_fac = visibility = geometric_type = 0
                val = []
                field = np.zeros([self.field_x_size, self.field_y_size])
                if len(obj) < 7:
                    print("here comes tar", obj)
                    x, y, z, z_size, radius, amount = obj
                    radius = radius[0] / 2

                    x_size = round(radius / 2)
                    y_size = round(radius / 2)
                    z_size = round(z_size / 2)
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

                field[l:r, u:o] = 1.
                #print("feld mit obstacle", (field != 0).astype(int))
                bbox = get_bounding_box(field)
                print("here comes bbox", bbox)
                nodes.append(bbox)
                #ndimage.rotate(field, 70, output=obs_transit, reshape=False, mode='constant')
            print("here is the node list: nodes", nodes)
            return nodes

        self.obs_nodes = get_nodes(self, self.obstacles)
        print("here is the node list obstacles", self.obs_nodes)
        self.tar_nodes = get_nodes(self, self.targets)
        print("here is the node list targets", self.tar_nodes)
        # print("obs", obs.astype(int))

        # print((obs!=0).astype(int))


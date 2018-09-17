import numpy as np

np.set_printoptions(threshold=np.inf)

class Nodes:
    def __init__(self, obstacles, targets, ball):
        self.obstacles = obstacles
        self.targets = targets
        self.ball = ball
        self.field_x_size = 1025
        self.field_y_size = 770
        self.tile_size = self.field_x_size / 4
        self.field_filled = np.zeros([self.field_x_size, self.field_y_size], dtype=object)

        #calculates the bounding box of a ndarray
        def get_bounding_box(x):
            mask = x == 0
            bbox = []
            all_axis = np.arange(x.ndim)
            for kdim in all_axis:
                nk_dim = np.delete(all_axis, kdim)
                mask_i = mask.all(axis=tuple(nk_dim))
                dmask_i = np.diff(mask_i)
                idx_i = np.nonzero(dmask_i)[0]
                if len(idx_i) != 2:
                    raise ValueError('Algorithm failed, {} does not have 2 elements!'.format(idx_i))
                bbox.append(slice(idx_i[0] + 1, idx_i[1] + 1))
            return bbox

        def get_nodes(objects):
            nodes = []

            for obj in objects:
                x = y = z = x_size = y_size = z_size = radius = z_angle_deg = slowdown_fac = visibility = geometric_type = 0
                field = np.zeros([self.field_x_size, self.field_y_size])
                field2 = np.zeros([self.field_x_size, self.field_y_size])
                global marker

                #initialises values according to object type: obs or tar
                if len(obj) < 7:
                    x, y, z, z_size, radius, amount = obj

                    radius = radius[0] / 2
                    x_size = round(radius / 2)
                    y_size = round(radius / 2)
                    z_size = round(z_size / 2)
                    marker = 2
                    print("marker tar", marker)
                else:
                    print("reached loop for marker 1")
                    x, y, z, x_size, y_size, z_size, z_angle_deg, slowdown_fac, visibility, geometric_type = obj

                    x_size = round(x_size / 2)
                    y_size = round(y_size / 2)
                    z_size = round(z_size / 2)
                    marker = 1

                #calculates the size of given object
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

                #adds object to field
                field[l:r, u:o] = marker

                #substracts x_center / y_center from objects and stores them in matrix
                idx_1 = np.nonzero(field)
                min_x_cent = []
                min_y_cent = []
                max_x_cent = []
                max_y_cent = []
                idx_min = []
                idx_max = []

                for i in idx_1[0]:
                    i = i - x
                    min_x_cent.append(i)
                idx_min.append(min_x_cent)
                for i in idx_1[1]:
                    i = i - y
                    min_y_cent.append(i)
                idx_min.append(min_y_cent)

                A = np.matrix(idx_min)

                #creates a rotation matrix R to rotate objects in given degree
                theta = np.radians(z_angle_deg)
                c, s = np.cos(theta), np.sin(theta)
                R = np.array(((c, -s), (s, c)))

                #multiply rotation matrix with object_field and store in array
                M = np.round(R * A)
                m_list = np.asarray(M)

                #adds x_center / y_center to objects
                for i in m_list[0]:
                    i = i + x
                    max_x_cent.append(i)
                idx_max.append(max_x_cent)
                for i in m_list[1]:
                    i = i + y
                    max_y_cent.append(i)
                idx_max.append(max_y_cent)

                #stores rotated objects in empty field and filled_field.
                i = 0
                for x in idx_max[0]:
                    y = idx_max[1][i]
                    field2[int(x), int(y)] = marker
                    self.field_filled[int(x), int(y)] = marker
                    i = i + 1

                bbox = get_bounding_box(field2)
                print("fierld filled with obstacles", self.field_filled)
                nodes.append(bbox)
            return nodes

        self.tar_nodes = get_nodes(self.targets)








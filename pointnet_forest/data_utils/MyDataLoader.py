import os
import numpy as np
from torch.utils.data import Dataset


class MyDataset(Dataset):

    def __init__(self, split='train', data_root='trainval_fullarea', num_point=1024, block_size=1.0, sample_rate=1.0, num_class=8,transform=None):
        super().__init__()
        self.num_point = num_point
        self.block_size = block_size
        self.transform = transform

        if split == 'train':
            data_root  = os.path.join(data_root, 'Train/')
            rooms_split = sorted(os.listdir(data_root))
        else:
            data_root = os.path.join(data_root, 'Test/')
            rooms_split = sorted(os.listdir(data_root))

        self.room_points, self.room_labels = [], []
        self.room_coord_min, self.room_coord_max = [], []
        num_point_all = []
        labelweights = np.zeros(num_class)

        for room_name in rooms_split:
            room_path = os.path.join(data_root, room_name)
            room_data = np.loadtxt(room_path)  # xyzrgbl, N*7
            points, labels = room_data[:, 0:6], room_data[:, 6]  # xyzrgb, N*6; l, N
            tmp, _ = np.histogram(labels, range(num_class+1))
            labelweights += tmp
            coord_min, coord_max = np.amin(points, axis=0)[:3], np.amax(points, axis=0)[:3]
            self.room_points.append(points), self.room_labels.append(labels)
            self.room_coord_min.append(coord_min), self.room_coord_max.append(coord_max)
            num_point_all.append(labels.size)
        labelweights = labelweights.astype(np.float32)
        labelweights = labelweights / np.sum(labelweights)
        self.labelweights = np.power(np.amax(labelweights) / labelweights, 1 / 3.0)
        print(self.labelweights)
        sample_prob = num_point_all / np.sum(num_point_all)
        num_iter = int(np.sum(num_point_all) * sample_rate / num_point)
        room_idxs = []
        for index in range(len(rooms_split)):
            room_idxs.extend([index] * int(round(sample_prob[index] * num_iter)))
        self.room_idxs = np.array(room_idxs)
        print("Totally {} samples in {} set.".format(len(self.room_idxs), split))

    def __getitem__(self, idx):
        room_idx = self.room_idxs[idx]
        points = self.room_points[room_idx]   # N * 6
        labels = self.room_labels[room_idx]   # N
        N_points = points.shape[0]

        while (True):
            center = points[np.random.choice(N_points)][:3]
            block_min = center - [self.block_size / 2.0, self.block_size / 2.0, 0]
            block_max = center + [self.block_size / 2.0, self.block_size / 2.0, 0]
            point_idxs = np.where((points[:, 0] >= block_min[0]) & (points[:, 0] <= block_max[0]) & (points[:, 1] >= block_min[1]) & (points[:, 1] <= block_max[1]))[0]
            if point_idxs.size > 1024:
                break

        if point_idxs.size >= self.num_point:
            selected_point_idxs = np.random.choice(point_idxs, self.num_point, replace=False)
        else:
            selected_point_idxs = np.random.choice(point_idxs, self.num_point, replace=True)

        # normalize
        selected_points = points[selected_point_idxs, :]  # num_point * 6
        current_points = np.zeros((self.num_point, 9))  # num_point * 9
        current_points[:, 6] = selected_points[:, 0] / self.room_coord_max[room_idx][0]
        current_points[:, 7] = selected_points[:, 1] / self.room_coord_max[room_idx][1]
        current_points[:, 8] = selected_points[:, 2] / self.room_coord_max[room_idx][2]
        selected_points[:, 0] = selected_points[:, 0] - center[0]
        selected_points[:, 1] = selected_points[:, 1] - center[1]
        # selected_points[:, 3:6] /= 65536
        selected_points[:, 3:6] /= 255
        current_points[:, 0:6] = selected_points
        current_labels = labels[selected_point_idxs]
        if self.transform is not None:
            current_points, current_labels = self.transform(current_points, current_labels)
        return current_points, current_labels

    def __len__(self):
        return len(self.room_idxs)

class TestDataLoad():
        # prepare to give prediction on each points
        def __init__(self, root, block_points=2048,  stride=0.5, block_size=1.0,  num_class=8, padding=0.001):
            self.block_points = block_points
            self.block_size = block_size
            self.padding = padding
            self.root = root
            self.stride = stride
            self.scene_points_num = []
            data_root = os.path.join(root, 'New/')
            self.file_list = sorted(os.listdir(data_root))

            self.scene_points_list = []
            self.semantic_labels_list = []
            self.room_coord_min, self.room_coord_max = [], []
            for file in self.file_list:
                data = np.loadtxt(data_root + file)
                points = data[:, :3]
                self.scene_points_list.append(data[:, :6])
                self.semantic_labels_list.append(data[:, 6])
                coord_min, coord_max = np.amin(points, axis=0)[:3], np.amax(points, axis=0)[:3]
                self.room_coord_min.append(coord_min), self.room_coord_max.append(coord_max)
            assert len(self.scene_points_list) == len(self.semantic_labels_list)

            labelweights = np.zeros(num_class)
            for seg in self.semantic_labels_list:
                tmp, _ = np.histogram(seg, range(num_class+1))
                self.scene_points_num.append(seg.shape[0])
                labelweights += tmp
            labelweights = labelweights.astype(np.float32)
            labelweights = labelweights / np.sum(labelweights)
            self.labelweights = np.power(np.amax(labelweights) / labelweights, 1 / 3.0)

        def __getitem__(self, index):
            point_set_ini = self.scene_points_list[index]
            points = point_set_ini[:, :6]
            labels = self.semantic_labels_list[index]
            coord_min, coord_max = np.amin(points, axis=0)[:3], np.amax(points, axis=0)[:3]
            grid_x = int(np.ceil(float(coord_max[0] - coord_min[0] - self.block_size) / self.stride) + 1)
            grid_y = int(np.ceil(float(coord_max[1] - coord_min[1] - self.block_size) / self.stride) + 1)
            # 这里需要考虑怎么修改
            if (grid_x < 1):
                grid_x  = 1
            if (grid_y  < 1):
                grid_y = 1
            data_room, label_room, sample_weight, index_room = np.array([]), np.array([]), np.array([]), np.array([])
            for index_y in range(0, grid_y):
                for index_x in range(0, grid_x):
                    s_x = coord_min[0] + index_x * self.stride
                    e_x = min(s_x + self.block_size, coord_max[0])
                    s_x = e_x - self.block_size
                    s_y = coord_min[1] + index_y * self.stride
                    e_y = min(s_y + self.block_size, coord_max[1])
                    s_y = e_y - self.block_size
                    point_idxs = np.where(
                        (points[:, 0] >= s_x - self.padding) & (points[:, 0] <= e_x + self.padding) & (
                                    points[:, 1] >= s_y - self.padding) & (
                                points[:, 1] <= e_y + self.padding))[0]
                    if point_idxs.size == 0:
                        continue
                    num_batch = int(np.ceil(point_idxs.size / self.block_points))
                    point_size = int(num_batch * self.block_points)
                    replace = False if (point_size - point_idxs.size <= point_idxs.size) else True
                    point_idxs_repeat = np.random.choice(point_idxs, point_size - point_idxs.size, replace=replace)
                    point_idxs = np.concatenate((point_idxs, point_idxs_repeat))
                    np.random.shuffle(point_idxs)
                    data_batch = points[point_idxs, :]
                    normlized_xyz = np.zeros((point_size, 3))
                    normlized_xyz[:, 0] = data_batch[:, 0] / coord_max[0]
                    normlized_xyz[:, 1] = data_batch[:, 1] / coord_max[1]
                    normlized_xyz[:, 2] = data_batch[:, 2] / coord_max[2]
                    data_batch[:, 0] = data_batch[:, 0] - (s_x + self.block_size / 2.0)
                    data_batch[:, 1] = data_batch[:, 1] - (s_y + self.block_size / 2.0)
                    #data_batch[:, 3:6] /= 65536
                    data_batch[:, 3:6] /= 255
                    data_batch = np.concatenate((data_batch, normlized_xyz), axis=1)
                    label_batch = labels[point_idxs].astype(int)
                    batch_weight = self.labelweights[label_batch]

                    data_room = np.vstack([data_room, data_batch]) if data_room.size else data_batch
                    label_room = np.hstack([label_room, label_batch]) if label_room.size else label_batch
                    sample_weight = np.hstack([sample_weight, batch_weight]) if label_room.size else batch_weight
                    index_room = np.hstack([index_room, point_idxs]) if index_room.size else point_idxs
            data_room = data_room.reshape((-1, self.block_points, data_room.shape[1]))
            label_room = label_room.reshape((-1, self.block_points))
            sample_weight = sample_weight.reshape((-1, self.block_points))
            index_room = index_room.reshape((-1, self.block_points))
            return data_room, label_room, sample_weight, index_room

        def __len__(self):
            return len(self.scene_points_list)

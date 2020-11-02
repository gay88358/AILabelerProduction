

class SharedFolder:
    def __init__(self, root, dataset_name_list, mount_root):
        self.root = root
        self.dataset_name_list = dataset_name_list
        self.mount_root = mount_root

    def get_mount_directory(self, dataset_name):
        if dataset_name in self.dataset_name_list:
            return self.mount_root + '/' + dataset_name
        raise ValueError('Given dataset name is invlide: ' + dataset_name)
__all__ = ["SharedFolder"]
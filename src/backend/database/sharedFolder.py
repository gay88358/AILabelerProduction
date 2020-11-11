

class SharedFolder:
    def __init__(self, root, dataset_name_list, mount_root):
        self.root = root
        self.dataset_name_list = dataset_name_list
        self.mount_root = mount_root

    def get_mount_directory(self, dataset_name):
        if dataset_name in self.dataset_name_list:
            return self.mount_root + '/' + dataset_name
        err_msg = 'Given dataset name is not contained in dataset_name_list: {}'.format(dataset_name)
        raise ValueError(err_msg)
    
    def contains(self, dataset_name_list):
        for d in dataset_name_list:
            if d not in self.dataset_name_list:
                return False
        return True

__all__ = ["SharedFolder"]
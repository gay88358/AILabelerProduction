from usecase.util.result import Result
from .mountDirectory import format_mount_directory

class AddSharedFolderUsecase:

    def __init__(self, dataset_repository):
        if dataset_repository == None:
            raise ValueError("Dataset Repository must not null")
        self.dataset_repository = dataset_repository
        
    def execute(self, user, stripID, dataset_name_list, mount_directory = "/worksapce/sharedFolder/ATWEX"):
        return self.check_empty_stripID(stripID)\
            .flat_map(lambda _: self.check_dataset_name_list(dataset_name_list))\
            .flat_map(lambda _: self.check_mount_directory(stripID, dataset_name_list, mount_directory))\
            .flat_map(lambda _: self.add_shared_folder_to_user(user, stripID, dataset_name_list, mount_directory))

    def check_empty_stripID(self, stripID):
        if stripID == "":
            err_msg = 'stripID {} can not be an empty string'.format(stripID)
            return Result.failure([err_msg])
        return Result.success('')


    def check_dataset_name_list(self, dataset_name_list):
        return self.check_contains_empty_name(dataset_name_list)\
            .flat_map(lambda _: self.check_duplicate(dataset_name_list))

    def check_duplicate(self, dataset_name_list):
        original_length = len(dataset_name_list)
        deduplicate_length = len(list(set(dataset_name_list)))
        if original_length != deduplicate_length:
            err_msg = 'dataset {} can not contain duplicate names'.format(dataset_name_list)
            return Result.failure([err_msg])
        return Result.success('')
    
    def check_contains_empty_name(self, dataset_name_list):
        for dataset_name in dataset_name_list:
            if dataset_name == "":
                err_msg = 'dataset_name_list {} can not contains empty string'.format(dataset_name_list)
                return Result.failure([err_msg])
        return Result.success('')

    def check_mount_directory(self, stripID, dataset_name_list, mount_directory):
        for dataset_name in self.format_dataset_name_list(stripID, dataset_name_list):
            result = format_mount_directory(mount_directory, dataset_name)
            if result.is_success() == False:
                return result
        return Result.success(dataset_name_list)

    def add_shared_folder_to_user(self, user, stripID, dataset_name_list, mount_directory):        
        result = self.dataset_repository.delete_by_stripId(stripID)
        if result.is_success() == False:
            return result

        user.add_strip_folder(stripID, self.format_dataset_name_list(stripID, dataset_name_list), mount_directory)
        return Result.success(user)

    def format_dataset_name_list(self, stripID, dataset_name_list):
        return list(
                    map(
                        lambda d: '{}/{}'.format(stripID, d),
                        dataset_name_list
                    )
                )


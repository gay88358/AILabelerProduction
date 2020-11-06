from usecase.util.result import Result

class AddSharedFolderUsecase:

    def execute(self, user, stripID, dataset_name_list, mount_directory = "/worksapce/sharedFolder/ATWEX"):
        user.add_shared_folder("", self.format_dataset_name_list(stripID, dataset_name_list), mount_directory)
        return Result.success(user)

    def format_dataset_name_list(self, stripID, dataset_name_list):
        return list(
                    map(
                        lambda d: '{}/{}'.format(stripID, d),
                        dataset_name_list
                    )
                )


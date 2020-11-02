
from usecase.util.result import Result
from database import (
    DatasetModel
)

class CreateNewDatasetUsecase:
    def create_all_dataset(self, dataset_name_list):
        dataset_id_list = []
        for dataset_name in dataset_name_list:
            result = self.to_dataset_id(dataset_name)
            if result.is_success():
                dataset_id_list.append(result.value)
            else:
                return result
        
        return Result.success(dataset_id_list)

    def to_dataset_id(self, name):
        dataset = DatasetModel.find_by_name(name)
        if dataset: # exist
            return Result.success(dataset.id)
        else:
            return self.create_new_dataset(name)

    def create_new_dataset(self, dataset_name): 
        try:       
            dataset = self.create_dataset(dataset_name)
            dataset.save()
            return Result.success(dataset.id)
        except:
            return Result.failure(['Dataset name is duplicate: ' + dataset_name])
    # seam point to isolate dataset dependency
    def create_dataset(self, dataset_name):
        return DatasetModel(
            name=dataset_name,
            categories=[]
        )
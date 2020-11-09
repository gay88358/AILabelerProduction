from usecase.util.result import Result
import json

# todo check all shape
class LabelChecker:

    INVALID_TYPE =  'Shape must contain Type property'       
    INVALID_POINTS =  'Shape must contain points property'       
    INVALID_ATTRIBUTES =  'Shape must contain Attributes property'       
    
    @staticmethod
    def check_string(labelme_json_string):
        return LabelChecker.check(json.loads(labelme_json_string))

    @staticmethod
    def check(labelme_document):
        labels = labelme_document['Labels']
        if LabelChecker.is_empty(labels):
            return Result.success('')
        shapesAndLabel = labels[0]
        shapes = shapesAndLabel['Shapes']
        return LabelChecker.check_shape(shapes)
    
    @staticmethod
    def is_empty(labels):
        return len(labels) == 0

    @staticmethod
    def check_shape(shapes):
        errors = []
        for shape in shapes:
            if 'Type' not in shape:
                errors.append(LabelChecker.INVALID_TYPE)
            
            if 'points' not in shape:
                errors.append(LabelChecker.INVALID_POINTS)
            
            if 'Attributes' not in shape:
                errors.append(LabelChecker.INVALID_ATTRIBUTES)

        if len(errors) > 0:
            return Result.failure(LabelChecker.remove_duplicate_error_message(errors))
        return Result.success('success')
    
    @staticmethod
    def remove_duplicate_error_message(errors):
        return list(
            set(
                errors
            )
        )
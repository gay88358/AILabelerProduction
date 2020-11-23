from usecase.util.result import Result
import json

class LabelChecker:

    INVALID_TYPE =  'Shape must contain Type property'       
    INVALID_POINTS =  'Shape must contain points property'       
    INVALID_ATTRIBUTES =  'Shape must contain Attributes property'       
    EMPTY_POINT = 'The point of shape can not be empty'

    @staticmethod
    def check_string(labelme_json_string):
        d = json.loads(labelme_json_string)
        return LabelChecker.check(d)

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
            LabelChecker.check_type(shape, errors)
            LabelChecker.check_point(shape, errors)
            LabelChecker.check_attribute(shape, errors)
        
        if len(errors) > 0:
            return Result.failure(LabelChecker.remove_duplicate_error_message(errors))
        return Result.success('success')
    
    @staticmethod
    def check_type(shape, errors):
        if 'Type' not in shape:
            errors.append(LabelChecker.INVALID_TYPE)

    @staticmethod
    def check_attribute(shape, errors):
        if 'Attributes' not in shape:
            errors.append(LabelChecker.INVALID_ATTRIBUTES)

    @staticmethod
    def check_point(shape, errors):
        if 'points' not in shape:
            errors.append(LabelChecker.INVALID_POINTS)
            return
        
        if len(shape['points']) == 0:
            errors.append(LabelChecker.EMPTY_POINT)

    @staticmethod
    def remove_duplicate_error_message(errors):
        return list(
            set(
                errors
            )
        )
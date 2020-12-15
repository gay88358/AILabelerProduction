
import { CompoundPathBuilder, compoundPathRecord } from './compoundPathRecord';

class AnnotationMapper {
    static annotationIdCounter = 0;

    createAnnotation(path, store) {
        let compoundPath = this.createCompoundPath(path);
        return this.mapAnnotationFrom(compoundPath, store);
    }

    createCompoundPath(path) {
        let initialCompoundPath = new CompoundPathBuilder(
          null,
          null,        
          null, 
          null,
          new paper.Point(1202 / 2, 1208 / 2)
        )
        .withAnnotationIndex(-1)
        .withCategoryIndex(-1)
        .withFullySelected(true)
        .withOpacity(true)
        .build()
  
        let pathItem = compoundPathRecord.unitCompound(
          new paper.CompoundPath(path), 
          initialCompoundPath
        );
        let result = new paper.CompoundPath(pathItem);
        result.fillColor = "red";
        return result;
    }
    
    mapAnnotationFrom(compoundPath, store) {
        let result = {}
        AnnotationMapper.annotationIdCounter += 1;
        this.appendBoxArea(result); // ok
        this.appendIdentity(result, store);
        this.appendDataPoints(result, compoundPath); // ok
        this.appendImageSize(result); 
        this.appendOtherData(result); // ok
        return result;
    }

    appendBoxArea(result) {
        result['area'] = 0
        result['bbox'] = [0, 0, 0, 0] // polygon path four points
    }
    
    appendIdentity(result, store) {      
        result['category_id'] = store.getters.getCurrentCategoryId; // current category_id
        result['dataset_id'] = store.getters.getCurrentDatasetId;
        result['id'] = AnnotationMapper.annotationIdCounter // generate from database
        result['image_id'] = store.getters.getCurrentImageId;
    }

    appendDataPoints(result, compoundPath) {
        result['paper_object'] = ["CompoundPath", compoundPath];
        result['segmentation'] = [];
        result['keypoints'] = [];
    }

    appendImageSize(result) {
        result['height'] = 0;
        result['width'] = 0;
    }

    appendOtherData(result) {
        result['isbbox'] = false;
        result['iscrowd'] = false;
        result['color'] = "#03dc34"
        result['creator'] = "admin"
        result['deleted'] = false
        result['metadata'] = {};
        result['milliseconds'] = 0;
    }
}

export const annotationMapper = new AnnotationMapper();
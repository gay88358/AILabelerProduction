
import { CompoundPathBuilder, compoundPathRecord } from './compoundPathRecord';
import axios from "axios";


class AnnotationIdGateway {
    constructor() {
        this.currentId = -1;
        this.maxId = -1;
    }

    async nextId() {
        let currentIdInitialized = this.currentId != -1
        let currentIdLessThanCache = this.currentId < this.maxId;
        if (!currentIdInitialized || !currentIdLessThanCache) {
            await this.resolveId();
        }
        this.currentId += 1;
        return this.currentId;
    }

    async resolveId() {
        let response = await this.fetchIdRange();
        let range = response.data;
        this.currentId = range[0];
        this.maxId = range[1];
    }

    async fetchIdRange() {
        let url = "/api/labelme/annotationIdentity";
        return axios.get(url);
    }
}


class AnnotationMapper {
    constructor() {
        this.idGateway = new AnnotationIdGateway()
    }

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
    
    async mapAnnotationFrom(compoundPath, store) {
        let result = {}
        this.appendBoxArea(result); // ok
        await this.appendIdentity(result, store);
        this.appendDataPoints(result, compoundPath); // ok
        this.appendImageSize(result); 
        this.appendOtherData(result); // ok
        return result;
    }

    appendBoxArea(result) {
        result['area'] = 0
        result['bbox'] = [0, 0, 0, 0] // polygon path four points
    }
    
    async appendIdentity(result, store) {      
        result['category_id'] = store.getters.getCurrentCategoryId; // current category_id
        result['dataset_id'] = store.getters.getCurrentDatasetId;
        let annotationId = await this.idGateway.nextId();
        result['id'] = annotationId // generate from database
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
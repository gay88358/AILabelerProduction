import Vue from 'vue';

export default 
class Annotator {
    static of(annotatorDataString) {
        let annotatorData = JSON.parse(annotatorDataString);
        return new Annotator(annotatorData);
    }

    constructor(annotatorData) {
        this.annotatorData = annotatorData;
        this.currentAnnotationData = null;
        this.currentCategoryName = "";
        this.CLASS = "Class";
        this.TYPE = "Type";
        this.VIM_300_CODE = "Vim300_Code";
    }

    addAnnotation(annotation) {
        // only for experiment 
        this.annotatorData[0].annotations.push(annotation);
    }

    setSelectedAnnotationAndCategory(categoryId, annotationId) {
        this.currentAnnotationData = this.findAnnotation(categoryId, annotationId);
        this.currentCategoryName = this.getCategoryName(categoryId);
    }

    getCategoryName(categoryId) {
        let result = this.findCategory(categoryId);
        return result.length === 0 ? "" : result[0].name;
    }

    findAnnotation(categoryId, annotationId) {
        return this.findCategory(categoryId)[0]
            .annotations
            .filter(a => a.id === annotationId)[0];
    }
    
    findCategory(categoryId) {
        return this.annotatorData.filter(c => c.id === categoryId);
    }

    getAnnotatorData() {
        return this.annotatorData;
    }
    
    deepClone(annotatorData) {
        return JSON.parse(JSON.stringify(annotatorData))
    }

    cloneAnnotatorData() {
        return JSON.parse(JSON.stringify(this.annotatorData));
    }

    hasSelectedAnnotation() {
        return this.currentAnnotationData != null;
    }

    getSelectedAnnotation() {
        if (!this.hasSelectedAnnotation()) {
            return this.createAnnotationMetadata("", "");
        }
            
        return this.createAnnotationMetadata(
            this.currentAnnotationData.metadata[this.TYPE],
            this.currentAnnotationData.metadata[this.CLASS] || ''
        );
    }

    createAnnotationMetadata(annotationType, annotationClass) {
        return {
            Type: annotationType,
            Class: annotationClass
        }
    }

    updateSelectedAnnotationMetadata(classValue, defectCodeCatalog) {
        Vue.set(this.currentAnnotationData.metadata, this.CLASS, classValue)
        let vim300Code = defectCodeCatalog.getVIM300Code(this.getCurrentCategoryName(), classValue)
        Vue.set(this.currentAnnotationData.metadata, this.VIM_300_CODE, vim300Code)
    }

    getCurrentCategoryName() {
        return this.currentCategoryName;
    }

    deleteSelectedAnnotation() {
        let annotationId = this.currentAnnotationData.id;
        let categoryId = this.currentAnnotationData.category_id;
        this.deleteAnnotationById(categoryId, annotationId);
    }

    deleteAnnotationById(categoryId, annotationId) {
        let deleteIndex = this.findDeleteAnnotationIndex(categoryId, annotationId);
        let annotations = this.findAnnotations(categoryId);
        annotations.splice(deleteIndex, 1);
    }

    findDeleteAnnotationIndex(categoryId, annotationId) {
        let annotations = this.findAnnotations(categoryId);
        for (let i = 0; i < annotations.length; i++)
            if (annotations[i].id === annotationId)
                return i;
        throw new Error('Given categoryId and annotationId is invalid');
    }

    findAnnotations(categoryId) {
        return this.findCategory(categoryId)[0].annotations;
    }
}
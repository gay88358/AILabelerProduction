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

    setSelectedAnnotationAndCategory(categoryId, annotationId) {
        this.setSelectedAnnotation(categoryId, annotationId);
        this.currentCategoryName = this.getCategoryName(categoryId);
    }

    setSelectedAnnotation(categoryId, annotationId) {
        this.currentAnnotationData = this.findAnnotation(categoryId, annotationId);
        this.categoryId = categoryId;
    }

    findAnnotation(categoryId, annotationId) {
        return this.findCategory(categoryId)[0]
            .annotations
            .filter(a => a.id === annotationId)[0];
    }

    getCategoryName(categoryId) {
        let result = this.findCategory(categoryId);
        if (result.length === 0)
            return "";
        return result[0].name;
    }

    findCategory(categoryId) {
        return this.annotatorData.filter(c => c.id === categoryId);
    }

    getCurrentCategoryName() {
        return this.currentCategoryName;
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
}
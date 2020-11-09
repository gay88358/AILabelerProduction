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
    }

    setSelectedAnnotationAndCategory(categoryId, annotationId) {
        this.setSelectedAnnotation(categoryId, annotationId);
        this.currentCategoryName = this.getCategoryName(categoryId);
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

    annotation(categoryId, annotationId) {
        let category = this.annotatorData.filter(a => a.id === categoryId)[0];
        return category.annotations.filter(a => a.id === annotationId)[0];
    }


    cloneAnnotatorData() {
        return JSON.parse(JSON.stringify(this.annotatorData));
    }

    setSelectedAnnotation(categoryId, annotationId) {
        this.currentAnnotationData = this.annotation(categoryId, annotationId);
        this.categoryId = categoryId;
    }

    getCategoryName(categoryId) {
        let result = this.annotatorData.filter(c => c.id === categoryId);
        if (result.length === 0)
            return "";
        return result[0].name;
    }

    hasSelectedAnnotation() {
        return this.currentAnnotationData != null;
    }

    getSelectedAnnotation() {
        if (!this.hasSelectedAnnotation())
            return {
                Type: "",
                Class: ""
            }
        //let annotation = state.annotatorData.getSelectedAnnotation();
        return { 
                Type: this.currentAnnotationData.metadata['Type'],
                Class: this.currentAnnotationData.metadata['class'] || ''
        };
    }

    updateSelectedAnnotationMetadata(typeValue, classValue) {
        Vue.set(this.currentAnnotationData.metadata, 'class', classValue)
    }

    findAnnotationMetadataBy(categoryId, annotationId) {
        let defectCode = this.annotation(categoryId, annotationId).metadata['class'];
        let type = this.annotation(categoryId, annotationId).metadata['Type'];
        return {
            Type: type,
            Class: defectCode
        }
    }
}
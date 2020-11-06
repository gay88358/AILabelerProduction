export default 
class Annotator {
    static of(annotatorDataString) {
        let annotatorData = JSON.parse(annotatorDataString);
        return new Annotator(annotatorData);
    }

    constructor(annotatorData) {
        this.annotatorData = annotatorData;
        this.currentAnnotationData = null;
        this.currentCategoryId = null;
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

    getSelectedAnnotation() {
        return this.currentAnnotationData;
    }

    updateSelectedAnnotationMetadata(typeValue, classValue) {
        // this.currentAnnotationData.metadata['Type'] = typeValue;
        this.currentAnnotationData.metadata['class'] = classValue;
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
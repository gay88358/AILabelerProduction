let assert = require('assert');
const util = require('util')
let fs = require('fs');
// import Annotator from '../annotatorObject';

class FileHelper {
    static async getJsonFile() {
        const readFilePromise = util.promisify(fs.readFile);
        return await readFilePromise('myjsonfile.json', 'utf8');
    }
}

class Annotator {
    static of(annotatorDataString) {
        let annotatorData = JSON.parse(annotatorDataString);
        return new Annotator(annotatorData);
    }

    constructor(annotatorData) {
        this.annotatorData = this.deepClone(annotatorData);
        this.currentAnnotationData = null;
    }

    deepClone(annotatorData) {
        return JSON.parse(JSON.stringify(annotatorData))
    }

    annotation(categoryId, annotationId) {
        let category = this.annotatorData.filter(a => a.id === categoryId)[0];
        return category.annotations.filter(a => a.id === annotationId)[0];
    }


    findMetadataItem(categoryId, annotationId, key) {
        let result = this.annotation(categoryId, annotationId);
        return result.metadata[key]
    }

    getAnnotatorData() {
        return this.annotatorData;
    }

    setSelectedAnnotation(categoryId, annotationId) {
        this.currentAnnotationData = this.annotation(categoryId, annotationId);
    }

    getSelectedAnnotation() {
        return this.currentAnnotationData;
    }

    updateSelectedAnnotationMetadata(typeValue, classValue) {
        this.currentAnnotationData.metadata['Type'] = typeValue;
        this.currentAnnotationData.metadata['class'] = classValue;
    }
}

describe('Annotator', function() {
    beforeEach(function() {
        categoryId = 130;
        annotationId = 73282;
    });

    it('should find annotation given categoryId and annotationId', async function() {
        // Arrange
        let annotator = await createAnnotator()
        // Act
        let result = annotator.annotation(categoryId, annotationId);
        // Assert
        assert.strictEqual(64, result.dataset_id);
    });

    it('update selected annotation with type and class value', async function() {
        let annotator = await createAnnotator()
        annotator.setSelectedAnnotation(categoryId, annotationId);
        const typeValue = "a type";
        const classValue = "normal"

        annotator.updateSelectedAnnotationMetadata(typeValue, classValue);

        result = annotator.getSelectedAnnotation();
        assert.strictEqual(typeValue, result.metadata['Type']);
        assert.strictEqual(classValue, result.metadata['class']);
    });

    async function createAnnotator() {
        let data = await FileHelper.getJsonFile();
        return Annotator.of(data);
    }
});

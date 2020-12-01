
import { EventHandler } from './logHandler';

export const setSelectedAnnotation = (store, annotationId, categoryId) => {
    store.dispatch('setSelectedAnnotation', {
        annotationId: annotationId,
        categoryId: categoryId
    });
};

export const updateAnnotationMetadata = (store, annotationClass) => {
    store.dispatch(
        'updateAnnotationMetadata', 
        {
          annotationClass: annotationClass
        }
    );

    EventHandler.annotationMetadataChanged();
}

export const deleteSelectedAnnotation = (store) => {
    store.dispatch(
        'deleteSelectedAnnotation'
    );
}

export const updateCurrentStripID = (store, stripID) => {
    store.dispatch('updateCurrentStripID', stripID);
}

export const updateAnnotatorData = (store, annotatorData) => {
    store.dispatch('updateAnnotatorData', annotatorData);
}

export const recordModifiedDataset = (store, datasetName, datasetId) => {
    store.dispatch('addAffectedDataset', { name: datasetName, id: datasetId });
}

export const clearAnnotatorData = (store) => {
    store.dispatch('clearAnnotatorData');
}
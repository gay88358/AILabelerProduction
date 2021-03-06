import Annotator from './annotatorObject';
import axios from "axios";

class DefectCodeCatalog {
    constructor(defectCodeCatalogDocument) {
        this.defectCodeCatalogDocument = defectCodeCatalogDocument
    }

    getDefectCodeListBy(categoryName) {
        if (!this.hasDefectCode(categoryName))
            return []
        return  this.findDefectCodeTokenBy(categoryName)
                    .defect_code_list
                    .map(d => d.Defect_Code);
    }

    getVIM300Code(categoryName, defectCode) { 
        if (!this.hasDefectCode(categoryName))
            return ""
        let defect_set = this.findDefectCodeTokenBy(categoryName)
                             .defect_code_list.filter(d => d.Defect_Code === defectCode)[0]
        return defect_set.Vim300_Code
    }

    findDefectCodeTokenBy(categoryName) {
        if (this.defectCodeCatalogDocument.length == 0)
            return []

        let result = this.defectCodeCatalogDocument.defectcode_catalog.filter(
            defectCode => defectCode.category_name === categoryName
        )
        return result.length == 0 ? [] : result[0];
    }

    hasDefectCode(categoryName) {
        return this.findDefectCodeTokenBy(categoryName).length != 0;
    }
}

class NullAnnotator {
    hasSelectedAnnotation() {
        return false;
    }

    getCurrentCategoryName() {
        return "";
    }

    getAnnotatorData() {
        return [];
    }
}

const state = {
    annotatorData: new NullAnnotator(),
    selectedCategoryName: "",
    defectCodeCatalog: [],
    tempAnnotations: []
}

const mutations = {
    UPDATE_ANNOTATOR_DATA (state, payload) {
        state.annotatorData = new Annotator(payload);
    },
    SET_SELECTED_ANNOTATION (state, {categoryId, annotationId}) {
        state.annotatorData.setSelectedAnnotationAndCategory(categoryId, annotationId);
    },
    UPDATE_ANNOTATION_METADATA(state, { annotationClass }) {
        state.annotatorData.updateSelectedAnnotationMetadata(annotationClass, new DefectCodeCatalog(state.defectCodeCatalog));        
    },
    UPDATE_DEFECT_CODE_CATALOG (state, payload) {
        state.defectCodeCatalog = JSON.parse(payload)
    },
    DELETE_ANNOTATION_BY_ID (state, {categoryId, annotationId}) {
        state.annotatorData.deleteAnnotationById(categoryId, annotationId);
    },
    DELETE_SELECTED_ANNOTATION(state, payload) {
        state.annotatorData.deleteSelectedAnnotation();
    },
    CLEAR_ANNOTATOR_DATA(state) {
        state.annotatorData = new NullAnnotator();
    },
    ADD_TEMP_ANNOTATION(state, tempAnnotation) {
        state.tempAnnotations.push(tempAnnotation);
    },
    SAVE_TEMP_ANNOTATIONS(state, addedAnnotationIdList) {
        state.tempAnnotations
            .filter(ta => addedAnnotationIdList.includes(ta.id))
            .forEach(ta => state.annotatorData.addAnnotation(ta));

        state.tempAnnotations = [];
    }
}

const actions = {
    updateAnnotatorData({ commit }, annotatorData) {
        commit('UPDATE_ANNOTATOR_DATA', annotatorData);
    },
    setSelectedAnnotation({ commit }, payload) {
        commit('SET_SELECTED_ANNOTATION', payload);
    },
    updateAnnotationMetadata({ commit }, payload) {
        commit('UPDATE_ANNOTATION_METADATA', payload);
    },
    getDefectCodeCatalog({ commit, state }) {
        if (state.defectCodeCatalog.length > 0)
            return state.defectCodeCatalog
        axios.get('/api/labelme/defect_code')
            .then(
            res => {
                commit('UPDATE_DEFECT_CODE_CATALOG', res.data)
            }
        )
    },
    deleteAnnotationById({ commit }, payload) {
        commit('DELETE_ANNOTATION_BY_ID', payload);
    },
    deleteSelectedAnnotation({commit}, payload) {
        commit('DELETE_SELECTED_ANNOTATION', payload);
    },
    clearAnnotatorData({ commit }) {
        commit('CLEAR_ANNOTATOR_DATA');
    },
    addTempAnnotation({ commit }, tempAnnotation) {
        commit('ADD_TEMP_ANNOTATION', tempAnnotation);
    },
    saveTempAnnotations({ commit }, addedAnnotationIdList) {
        commit('SAVE_TEMP_ANNOTATIONS', addedAnnotationIdList);
    }
}

const getters = {
    getDefectCodeOfSelectedAnnotation: state => {
        if (!state.annotatorData.hasSelectedAnnotation())
            return [];
        return new DefectCodeCatalog(state.defectCodeCatalog)
        .getDefectCodeListBy(state.annotatorData.getCurrentCategoryName())
    },
    hasAnnotationSelected: state => {
        return state.annotatorData.hasSelectedAnnotation();
    },
    getSelectedAnnotation: state => {
        return state.annotatorData.getSelectedAnnotation();
    },
    getCategories: state => {
        return state.annotatorData.getAnnotatorData();
    },
    getDefectCodeList: (state) => (categoryName) => {
        return new DefectCodeCatalog(state.defectCodeCatalog)
        .getDefectCodeListBy(categoryName)
    },
    containsTempAnnotation: (state) => state.tempAnnotations.length > 0,
    getTempAnnotations:(state) => state.tempAnnotations
}

const annotatorDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default annotatorDataModule;
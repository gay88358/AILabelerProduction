
import Annotator from './annotatorObject';
import axios from "axios";

const state = {
    annotatorData: null,
    selectedAnnotation: null,
    selectedCategoryName: "",
    defectCodeCatalog: [],
    categoriesData: []
}

const mutations = {
    UPDATE_ANNOTATOR_DATA (state, payload) {
        state.annotatorData = new Annotator(payload);
        state.categoriesData = state.annotatorData.getAnnotatorData();
    },
    SET_SELECTED_ANNOTATION (state, {categoryId, annotationId}) {
        state.annotatorData.setSelectedAnnotation(categoryId, annotationId);
        state.selectedAnnotation = state.annotatorData.getSelectedAnnotation();
        state.selectedCategoryName = state.annotatorData.getCategoryName(categoryId);
    },
    UPDATE_ANNOTATION_METADATA(state, { annotationType, annotationClass }) {
        state.annotatorData.updateSelectedAnnotationMetadata(annotationType, annotationClass);        
        state.categoriesData = state.annotatorData.cloneAnnotatorData();

        state.selectedAnnotation = { ...state.annotatorData.getSelectedAnnotation() };
    },
    UPDATE_DEFECT_CODE_CATALOG (state, payload) {
        state.defectCodeCatalog = payload
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
                commit('UPDATE_DEFECT_CODE_CATALOG', res.data['defectcode_catalog'])
            }
        )
    }
}

class DefectCodeCatalog {
    constructor(defectCodeCatalogDocument) {
        this.defectCodeCatalogDocument = defectCodeCatalogDocument
    }

    getDefectCodeListBy(categoryName) {
        let result = this.defectCodeCatalogDocument.filter(
            defectCode => defectCode.category_name === categoryName
        )
        if (result.length == 0)
            return []
        return result[0].defect_code_list;
    }
}

const getters = {
    getDefectCodeOfSelectedAnnotation: state => {
        if (!state.selectedAnnotation == null)
            return [];
        return new DefectCodeCatalog(state.defectCodeCatalog)
        .getDefectCodeListBy(state.selectedCategoryName)
    },
    hasAnnotationSelected: state => {
        return state.selectedAnnotation !== null
    },
    getSelectedAnnotation: state => {
        return  { 
            Type: state.selectedAnnotation.metadata['Type'],
            Class: state.selectedAnnotation.metadata['class'] || ''
        }
    },
    getCategories: state => {
        return state.categoriesData;
    },
    getDefectCodeList: (state) => (categoryName) => {
        return new DefectCodeCatalog(state.defectCodeCatalog)
        .getDefectCodeListBy(categoryName)
    }
}

const annotatorDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default annotatorDataModule;
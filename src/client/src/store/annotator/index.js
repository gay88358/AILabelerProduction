import Annotator from './annotatorObject';
import axios from "axios";


class DefectCodeCatalog {
    constructor(defectCodeCatalogDocument) {
        this.defectCodeCatalogDocument = defectCodeCatalogDocument
    }

    getDefectCodeListBy(categoryName) {
        if (this.defectCodeCatalogDocument.length == 0)
            return []

        let result = this.defectCodeCatalogDocument.defectcode_catalog.filter(
            defectCode => defectCode.category_name === categoryName
        )
        if (result.length == 0)
            return []
        return result[0].defect_code_list.map(d => d.Defect_Code);
    }

    getVIM300Code(categoryName, defectCode) { 
        if (this.defectCodeCatalogDocument.length == 0)
            return []
        let result = this.defectCodeCatalogDocument.defectcode_catalog.filter(
            defectCode => defectCode.category_name === categoryName
        )
        if (result.length == 0)
            return []
        let defect_set = result[0].defect_code_list.filter(d => d.Defect_Code === defectCode)[0]
        return defect_set.Vim300_Code
    }
}

class NullAnnotator {
    hasSelectedAnnotation() {
        return false;
    }

    getCurrentCategoryName() {
        return "";
    }
}

const state = {
    annotatorData: new NullAnnotator(),
    selectedCategoryName: "",
    defectCodeCatalog: [],
}

const mutations = {
    UPDATE_ANNOTATOR_DATA (state, payload) {
        state.annotatorData = new Annotator(payload);
    },
    SET_SELECTED_ANNOTATION (state, {categoryId, annotationId}) {
        state.annotatorData.setSelectedAnnotationAndCategory(categoryId, annotationId);
    },
    UPDATE_ANNOTATION_METADATA(state, { annotationType, annotationClass }) {
        state.annotatorData.updateSelectedAnnotationMetadata(annotationType, annotationClass, new DefectCodeCatalog(state.defectCodeCatalog));        
    },
    UPDATE_DEFECT_CODE_CATALOG (state, payload) {
        state.defectCodeCatalog = JSON.parse(payload)
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
    }
}

const annotatorDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default annotatorDataModule;
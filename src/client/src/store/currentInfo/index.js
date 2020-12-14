const state = {
    current_dataset_id: -1,
    current_image_id: -1,
    current_category_id: -1    
}

const mutations = {
    UPDATE_CURRENT_DATASET_ID(state, dataset_id) {
        state.current_dataset_id = dataset_id;
    },
    UPDATE_CURRENT_IMAGE_ID(state, image_id) {
        state.current_image_id = image_id;
    },
    UPDATE_CURRENT_CATEGORY_ID(state, category_id) {
        state.current_category_id = category_id;
    }
}

const actions = {
    updateCurrentDatasetId({ commit }, datasetId) {
        commit('UPDATE_CURRENT_DATASET_ID', datasetId)
    },
    updateCurrentImageId({ commit }, imageId) {
        commit('UPDATE_CURRENT_IMAGE_ID', imageId)
    },
    updateCurrentCategoryId({ commit }, categoryId) {
        commit('UPDATE_CURRENT_CATEGORY_ID', categoryId)
    }
}

const getters = {
    getCurrentDatasetId: state => state.current_dataset_id,
    getCurrentImageId: state => state.current_image_id,
    getCurrentCategoryId: state => state.current_category_id,
}

const currentInfo = {
    state,
    mutations,
    actions,
    getters
}

export default currentInfo;
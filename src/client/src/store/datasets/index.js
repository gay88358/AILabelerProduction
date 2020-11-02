
const state = {
    datasetFolders: ""
}

const mutations = {
    UPDATE_DATASET_FOLDERS (state, payload) {
        state.datasetFolders = payload
    }
}

const actions = {
    updateDatasetFolders({ commit }, payload) {
        commit('UPDATE_DATASET_FOLDERS', payload)
    }
}

const getters = {
    getDatasetsUrl: state => '/datasets/' + state.datasetFolders,
}

const datasetDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default datasetDataModule;

const state = {
    current_stripID: ""
}

const mutations = {
    UPDATE_CURRENT_STRIP_ID (state, payload) {
        state.current_stripID = payload
    }
}

const actions = {
    updateCurrentStripID({ commit }, payload) {
        commit('UPDATE_CURRENT_STRIP_ID', payload)
    }
}

const getters = {
    getDatasetsUrl: state => '/datasets/' + state.current_stripID,
}

const datasetDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default datasetDataModule;
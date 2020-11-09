import AffectedDataset from './affectedDataset'

const state = {
    current_stripID: "",
    affectedDataset: new AffectedDataset()
}

const mutations = {
    UPDATE_CURRENT_STRIP_ID (state, payload) {
        let different_stripID = state.current_stripID !== payload
        if (different_stripID) {
            state.affectedDataset = state.affectedDataset.withEmptyDataset()
        }
        state.current_stripID = payload
    },
    ADD_AFFECTED_DATASET (state, payload) {
        state.affectedDataset.addAffectedDataset(payload)
    }
}

const actions = {
    updateCurrentStripID({ commit }, payload) {
        commit('UPDATE_CURRENT_STRIP_ID', payload)
    },
    addAffectedDataset({ commit }, affectedDataset) {
        commit('ADD_AFFECTED_DATASET', affectedDataset)
    }
}

const getters = {
    getDatasetsUrl: state => '/datasets/' + state.current_stripID,
    getAffectedDatasetMetadata: state => {
        return {
            id: state.current_stripID,
            dataset: state.affectedDataset.getAffectedDatasetNameList()
        }
    }
}

const datasetDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default datasetDataModule;
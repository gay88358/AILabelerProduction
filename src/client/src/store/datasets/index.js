import AffectedDataset from './affectedDataset'

const state = {
    current_stripID: "",
    affectedDataset: new AffectedDataset()
}

const mutations = {
    UPDATE_CURRENT_STRIP_ID (state, payload) {
        if (state.current_stripID !== payload) {
            state.affectedDataset = new AffectedDataset()
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
            id: state.affectedDataset.getStripId(),
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
import AffectedDataset from './affectedDataset'

const state = {
    affectedDataset: new AffectedDataset()
}

const mutations = {
    ADD_AFFECTED_DATASET (state, payload) {
        state.affectedDataset.addAffectedDataset(payload)
    }
}

const actions = {
    addAffectedDataset({ commit }, affectedDataset) {
        commit('ADD_AFFECTED_DATASET', affectedDataset)
    }
}

const getters = {
    getAffectedDatasetList: state => state.affectedDataset.getAffectedDatasetList(),
    getAffectedDatasetNameList: state => state.affectedDataset.getAffectedDatasetNameList()
}

const saveDataModule = {
    state,
    mutations,
    actions,
    getters
}

export default saveDataModule;
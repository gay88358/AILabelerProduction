import Vue from "vue";
import Vuex from "vuex";

import user from "./user";
import info from "./info";
import datasetsData from "./datasets";
import annotator from "./annotator";
import currentInfo from "./currentInfo";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    info,
    datasetsData,
    annotator,
    currentInfo
  },
  state: {
    process: [],
    undo: [],
    dataset: ""
  },
  mutations: {
    setDataset(state, dataset) {
      state.dataset = dataset;
    },
    addProcess(state, process) {
      state.process.push(process);
    },
    removeProcess(state, process) {
      let index = state.process.indexOf(process);
      if (index > -1) {
        state.process.splice(index, 1);
      }
    },
    resetUndo(state) {
      state.undo = [];
    },
    addUndo(state, action) {
      state.undo.push(action);
    },
    undo(state) {
      let action = state.undo.pop();
      if (action != null) {
        action.undo();
      }
    },
    removeUndos(state, action) {
      state.undo = state.undo.filter(undo => undo.action !== action);
    }
  },
  actions: {}
});

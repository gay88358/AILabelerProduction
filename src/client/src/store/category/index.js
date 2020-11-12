// import axios from "axios";
// import DefectCodeCatalog from "./defectCodeCatalog";

// const state = {
//     defectCodeCatalog: []
// }

// const mutations = {
//     UPDATE_DEFECT_CODE_CATALOG (state, payload) {
//         state.defectCodeCatalog = payload
//     }
// }

// const actions = {
//     getDefectCodeCatalog({ commit }) {
//         axios.get('/api/labelme/defect_code').then(
//             res => {
//                 let defectCodeCatalog = res.data['defectcode_catalog']
//                 commit('UPDATE_DEFECT_CODE_CATALOG', defectCodeCatalog)
//             }
//         )
//     }
// }

// const getters = {
//     defectCodeCatalog: state => state.defectCodeCatalog,
//     getDefectCodeList: (state) => (categoryName) => {
//         return new DefectCodeCatalog(state.defectCodeCatalog)
//         .getDefectCodeListBy(categoryName)
//     }
// }

// const defectCodeCatalogModule = {
//     state,
//     mutations,
//     actions,
//     getters
// }
  
// export default defectCodeCatalogModule;
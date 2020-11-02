export default class AffectedDataset {
    constructor() {
        this.affectedDatasetList = []
    }

    addAffectedDataset(dataset) {
        if (this.contains(dataset))
            return
        this.affectedDatasetList.push(dataset)
    }

    contains(dataset) {
        let result = this.affectedDatasetList.filter(
            d => d.name === dataset.name && d.id === dataset.id
        )
        return result.length != 0
    }

    getAffectedDatasetList() {
        return this.affectedDatasetList
    }

    getAffectedDatasetNameList() {
        return this.affectedDatasetList.map(dataset => dataset.name);
    }

    getAffectedDatasetSize() {
        return this.affectedDatasetList.length
    }
}


// let datasetData1 = {
//     name: "logcase1",
//     id: "1"
// }

// let datasetData2 = {
//     name: "logcase2",
//     id: "1"
// }

// let datasetData3 = {
//     name: "logcase3",
//     id: "1"
// }

// let assert = require('assert');  

// let dataset = new AffectedDataset()
// dataset.addAffectedDataset(datasetData1)
// dataset.addAffectedDataset(datasetData2)
// dataset.addAffectedDataset(datasetData3)

// assert.notStrictEqual(dataset.getAffectedDatasetNameList(), [ 'logcase1', 'logcase2', 'logcase3' ])

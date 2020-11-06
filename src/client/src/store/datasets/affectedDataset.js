class AffectedDataset {
    constructor() {
        this.affectedDatasetList = []
    }

    addAffectedDataset(dataset) {
        if (this.contains(dataset))
            return
        this.affectedDatasetList.push(dataset)
    }

    getStripId() {
        if (this.getAffectedDatasetNameList().length == 0)
            return "No StripID";

        let dataset = this.getAffectedDatasetNameList()[0]  
        return dataset.split('/')[0]
    }

    contains(dataset) {
        let result = this.affectedDatasetList.filter(
            d => d.name === dataset.name && d.id === dataset.id
        )
        return result.length != 0
    }

    getAffectedDatasetNameList() {
        return this.affectedDatasetList.map(dataset => dataset.name);
    }

    getAffectedDatasetSize() {
        return this.affectedDatasetList.length
    }

}


let datasetData1 = {
    name: "stripID1/logcase1",
    id: "1"
}

let datasetData2 = {
    name: "stripID1/logcase2",
    id: "1"
}

let datasetData3 = {
    name: "stripID2/logcase3",
    id: "1"
}

let assert = require('assert');  

let dataset = new AffectedDataset()
dataset.addAffectedDataset(datasetData1)
dataset.addAffectedDataset(datasetData2)

assert.notStrictEqual(dataset.getAffectedDatasetNameList(), [ 'logcase1', 'logcase2', 'logcase3' ])

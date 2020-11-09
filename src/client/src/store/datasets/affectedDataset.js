export default class AffectedDataset {
    constructor() {
        this.affectedDatasetList = []
    }

    withEmptyDataset() {
        return new AffectedDataset()
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
        return this.affectedDatasetList.map(dataset => this.removeStripId(dataset.name));
    }

    removeStripId(datasetName) {
        let tokens = datasetName.split('/')
        let dataset_name_index = tokens.length - 1
        return tokens[dataset_name_index]
    }

    getAffectedDatasetSize() {
        return this.affectedDatasetList.length
    }
}
import paper from "paper";


export class CompoundPathFactory {
    static create(onDoucleClickCallback, onClickCallback) {
        let result = new paper.CompoundPath();
        result.onDoubleClick = onDoucleClickCallback;
        result.onClick = onClickCallback;
        return result;  
    }
}

class CompoundPathRecord {
    constructor() {
        this.compoundPath = null;
    }

    setCompoundPath(compoundPath) {
        this.compoundPath = compoundPath;
    }

    getCompoundPath() {
        return this.compoundPath;
    }
}

export const compoundPathRecord = new CompoundPathRecord();
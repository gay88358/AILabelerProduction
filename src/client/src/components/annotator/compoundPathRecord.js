import paper from "paper";

import simplifyjs from "simplify-js";

export class CompoundPathBuilder {
    constructor(onDoucleClickCallback, onClickCallback, paperObjectJson, segments, center) {
        this.onDoucleClickCallback = onDoucleClickCallback;
        this.onClickCallback = onClickCallback;
        this.paperObjectJson = paperObjectJson;
        this.segments = segments;
        this.center = center;
        this.annotationIndex = null;
        this.categoryIndex = null;
        this.isFullySelected = null;
        this.opacity = null;
    }

    withAnnotationIndex(annotationIndex) {
        this.annotationIndex = annotationIndex;
        return this;
    }   

    withCategoryIndex(categoryIndex) {
        this.categoryIndex = categoryIndex;
        return this;
    }

    withFullySelected(isFullySelected) {
        this.isFullySelected = isFullySelected;
        return this;
    }

    withOpacity(opacity) {
        this.opacity = opacity;
        return this;
    }

    build() {
        let compoundPath = CompoundPathFactory.create(
            this.onDoucleClickCallback, 
            this.onClickCallback, 
            this.paperObjectJson, 
            this.segments, 
            this.center
        );
        compoundPath.data.annotationId = this.annotationIndex;
        compoundPath.data.categoryId = this.categoryIndex;
        compoundPath.fullySelected = this.isFullySelected;
        compoundPath.opacity = this.opacity;
        return compoundPath;
    }

}

export class CompoundPathFactory {
    static create(onDoucleClickCallback, onClickCallback, paperObjectJson, segments, center) {
        let result = new paper.CompoundPath();
        result.onDoubleClick = onDoucleClickCallback;
        result.onClick = onClickCallback;
        compoundPathRecord.loadJsonOrSegmentIntoCompoundPath(
            paperObjectJson, 
            segments,
            result,
            center
        );
        return result;  
    }
}


class CompoundPathRecord {
    constructor() {
        this.compoundPath = null;
    }

    setCompoundPathAnnotationAndCategoryIndex(compoundPath, annotationIndex, categoryIndex) {
        compoundPath.data.annotationId = annotationIndex;
        compoundPath.data.categoryId = categoryIndex;
    }  

    setCompoundPathFullySelected(compoundPath, isFullySelected) {
        compoundPath.fullySelected = isFullySelected;
    }
    
    setCompoundPathOpacity(compoundPath, newOpacity) {
        compoundPath.opacity = newOpacity;
    }
  
    copyCompoundPath(compoundPath) {
        let result = compoundPath.clone();
        result.fullySelected = false;
        result.visible = false;
        return result;
    }
  
    updateCompoundPathChildren(compoundPath, simplifyNumber) {
        let newChildren = this.calculateCompoundPathChildren(compoundPath, simplifyNumber);
        compoundPath.removeChildren();
        compoundPath.addChildren(newChildren);
    }
  
    calculateCompoundPathChildren(compoundPath, simplifyNumber) {
        return compoundPath
            .children
            .map(
                path => this._toPaperPath(path, simplifyNumber)
            )
    }

    _toPaperPath(path, simplifyNumber) {
        let points = [];
        path.segments.forEach(seg => {
          points.push({ x: seg.point.x, y: seg.point.y });
        });
        points = simplifyjs(points, simplifyNumber, true);

        let result = new paper.Path(points);
        result.closePath();
        return result;
    }
  

    unitCompound(newCompound, originalCompound) {
        let result = originalCompound.unite(newCompound);
        result.strokeColor = null;
        result.strokeWidth = 0;
        result.onDoubleClick = originalCompound.onDoubleClick;
        result.onClick = originalCompound.onClick;
        return result;
    }
  

    removeCompoundPath(compoundPath) {
        if (compoundPath == null) {
          return;
        }
        compoundPath.remove();
      }
  
    setCompoundPath(compoundPath) {
        this.compoundPath = compoundPath;
    }

    getCompoundPath() {
        return this.compoundPath;
    }

    loadSegmentsIntoCompoundpath(segments, compoundPath, center) {
        segments
          .map(s => this.calculatePath(s, center))
          .forEach(path =>  compoundPath.addChild(path));
    }
  
    calculatePath(segment, center) {
        let result = new paper.Path();
        for (let j = 0; j < segment.length; j += 2) {
          let x = segment[j];
          let y = segment[j + 1]
          let point = new paper.Point(x, y);
          result.add(point.subtract(center));
        }
        result.closePath();
        return result;
    }

    loadJsonOrSegmentIntoCompoundPath(paperObjectJson, segments, compoundPath, center) {
        paperObjectJson = this.checkJson(paperObjectJson);
        if (paperObjectJson != null) {
          compoundPath.importJSON(paperObjectJson);
          return;
        }
        segments = this.checkSegments(segments);
        if (segments != null) {
          this.loadSegmentsIntoCompoundpath(segments, compoundPath, center);
        }
    }
  
  
    checkJson(paperObjectJson) {
        // consolidate expression to simplify nested condition checking
        if (paperObjectJson == null || this.noCompoundPathOrMatrix(paperObjectJson)) {
          return null;
        }
        return paperObjectJson;
    }
  
    noCompoundPathOrMatrix(paperObjectJson) {
        return paperObjectJson.length !== 2
    }

    checkSegments(segments) {
        if (segments == null || segments.length === 0)
            return null;
        return segments;
    }

    highlightColor(compoundPath, opacity, annotationColor) {
        if (compoundPath == null) return;
        this.setCompoundPathOpacity(compoundPath, opacity);
        this.setCompoundPathFillColor(compoundPath, annotationColor);
    }

    setCompoundPathFillColor(compoundPath, newFillColor) {
        compoundPath.fillColor = newFillColor;
    }

}

export const compoundPathRecord = new CompoundPathRecord();
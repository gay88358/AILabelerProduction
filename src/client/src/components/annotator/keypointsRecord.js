
export default class KeypointsRecord {
    getKeypoints() {
        return this.keypoints;
    }

    setKeypoints(keypoints) {
        this.keypoints = keypoints;
    }

    setKeypointsColor(newColor) {
        this.getKeypoints().color = newColor;
    }
  
    setKeypointsVisible(newVisible) {
        this.getKeypoints().visible = newVisible;
    }

    setKeypointsRadius(newRadius) {
        this.getKeypoints().radius = newRadius;
    }

    setKeypointsLineWidth(newLineWidth) {
        this.getKeypoints().lineWidth = newLineWidth;
    }

    isEmptyKeypoints() {
        return this.getKeypoints().isEmpty();
    } 
    
    getKeypointsLabel(index) {
        return this.getKeypoints()._labelled[index];
    }
    
    containsKeypointsLabel() {
        return this.getKeypoints()._labelled;
    }

    exportKeypointsJson(keypointLabels, width, height) {
        return this.getKeypoints().exportJSON(
            keypointLabels,
            width,
            height
        );
    }
  
    bringKeypointsToFront() {
        this.getKeypoints().bringToFront();
    }

    deleteKeypoint(keypoint) {
        this.getKeypoints().deleteKeypoint(keypoint);
    }

    contains(point) {
        return this.getKeypoints().contains(point); 
    }

    exportJSONKeypoints(keypointLabels, annotationWidth, annotationHeight) {
        return this.getKeypoints().exportJSON(
            keypointLabels,
            annotationWidth,
            annotationHeight
        );
    }
  
    addKeypoints(keypoint) {
        this.getKeypoints().addKeypoint(keypoint);
    }

    moveKeypoint(newPoint, keypoint) {
        this.getKeypoints().moveKeypoint(newPoint, keypoint);
    }

    addAllEdges(newEdges) {
        newEdges.forEach(e => this.getKeypoints().addEdge(e));
    }

    removeKeypoints() {
        this.getKeypoints().remove();
    }

    getLine(edge) {
        return this.getKeypoints().getLine(edge);
    }

    getKeypointVisibility(index) {
        let visibility = 0;
        if (this.getKeypoints() && this.containsKeypointsLabel()) {
          let labelled = this.getKeypointsLabel(index + 1);
          if (labelled) {
            visibility = labelled.visibility;
          }
        }
        return visibility;
    }
}



export const keypointsRecord = new KeypointsRecord();;
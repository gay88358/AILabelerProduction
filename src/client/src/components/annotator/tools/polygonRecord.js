
class PolygonRecord {
    constructor() {
        this.record = {
            path: null,
            guidance: true,
            pathOptions: {
              strokeColor: "black",
              strokeWidth: 1
            }
        }
    }

    removeAllSegments() {
        this.getPolygonPath().removeSegments();
    }

    removeSegments(points) {
        let length = this.polygonSegmentLength();
        this.getPolygonPath().removeSegments(length - points, length);  
    }

    getPolygonPath() {
        return this.record.path;
    }

    getCompleteDistance() {
        return this.record.completeDistance;
    }

    getMinDistance() {
        return this.record.minDistance;
    }

    setPolygonPath(newPath) {
        this.record.path = newPath;
    }

    getPolygonPathOptions() {
        return this.record.pathOptions;
    }

    getPolygonPathStrokeColor() {
        return this.record.pathOptions.strokeColor;
    }

    setPolygonPathFillColor(color) {
        this.getPolygonPath().fillColor = color;
    }

    removePolygonPath() {
        this.setPolygonPathFillColor("black");
        this.getPolygonPath().closePath();
        this.getPolygonPath().remove();
        this.setPolygonPath(null);
    }

    setPolygonPathOptionsStrokeWidth(newStrokeWidth) {
        this.getPolygonPathOptions().strokeWidth = newStrokeWidth;
    }

    polygonSegmentLength() {
        return this.getPolygonPath().segments.length;
    }

    setPolygonPathStrokeWidth(newStrokeWidth) {
        this.getPolygonPath().strokeWidth = newStrokeWidth;
    }

    setPolygonPathStrokeColor(newColor) {
        this.getPolygonPath().strokeColor = newColor;
    }
}

export const polygonRecord = new PolygonRecord();

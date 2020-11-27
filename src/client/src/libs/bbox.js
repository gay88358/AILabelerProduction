class Point{
    constructor(point) {
        this.x = point.x;
        this.y = point.y;
    }
}

export class BBox {
    constructor(point) {
        this.startPoint = new Point(point);
        this.endPoint = null;
    }

    addPointsTo(path) {
        this.getPoints()
            .forEach(
                point => path.add(point)
            );
    }
    
    modifyPoint(point){
        this.endPoint = new Point(point);
        this.startXEndYPoint = new Point({x: this.getStartPoint().x, y: this.getEndPoint().y});
        this.startYEndXPoint = new Point({x: this.getEndPoint().x, y: this.getStartPoint().y});
    }

    getPoints(){
        if(!this.isComplete()) {
            return [this.getStartPoint()];
        }
        let points = [];
        points[0] = this.getStartPoint();
        points[1] = this.startXEndYPoint;
        points[2] = this.getEndPoint();
        points[3] = this.startYEndXPoint;
        points[4] = this.getStartPoint();
        return points;
    }

    isComplete() {
        return this.getEndPoint() != null;
    }

    getStartPoint() {
        return this.startPoint;
    }

    getEndPoint() {
        return this.endPoint;
    }

    removePoint() {
        this.endPoint = null;
        this.startXEndYPoint = null;
        this.startYEndXPoint = null;
    }
}
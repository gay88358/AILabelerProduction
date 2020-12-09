
// singleAnnotationRecord encapsulates the structure of the annotation
// and prevent annotation vue component couples to that structure
// Advantage: For the change to thestructure of the annotation, only modify one place(SingleAnnotationRecord) 


class SingleAnnotationRecord {
    getAnnotationCreator(annotation) {
        return annotation.creator;
    }

    getAnnotationId(annotation) {
        return annotation.id;
    }
  
    getAnnotationWidth(annotation) {
        return annotation.width;
    }
    
    getAnnotationHeight(annotation) {
        return annotation.height;
    }

    setAnnotationIsBBox(annotation, isBBox) {
        annotation.isbbox = isBBox;
    }

    getAnnotationIsBBox(annotation) {
        return annotation.isbbox;
    }
  
    getAnnotationPaperObject(annotation) {
        return annotation.paper_object;
    }
    
    setAnnotationPaperObject(annotation, paper_object) {
        // given annotation's point & segments data
        // so that the annotation can be displayed on the canvas
        annotation.paper_objec = paper_object;
    }

    getAnnotationKeypoints(annotation) {
        return annotation.keypoints;
    }

    getAnnotationSegmentation(annotation) {
        return annotation.segmentation;
    }

    getAnnotationColor(annotation) {
        return annotation.color;
    }
}


export const singleAnnotationRecord = new SingleAnnotationRecord();
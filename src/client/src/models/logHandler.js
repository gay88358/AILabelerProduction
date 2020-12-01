import axios from "axios";

const logToService = (message) => {
    axios.post(
        '/api/labelme/log', 
        {
            message: message
        }
    );
}

class LogHandler {
    annotationDeleted() {
        logToService('Annotation Deleted')
    }
    
    annotationMetadataChanged() {
        logToService('Annotation Metadata Changed')
    }
    
    annotationAdded() {
        logToService('Annotation Added')
    }

    annotationShapeModified() {
        logToService('Annotation Shape Modified')
    }
}

export const EventHandler = new LogHandler;

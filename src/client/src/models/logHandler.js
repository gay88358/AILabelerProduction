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
    
    annotationMetadataChanged(annotationClass) {
        logToService(`Change the metadata of the annotation to ${annotationClass}`)
    }
    
    annotationAdded() {
        logToService('Annotation Added')
    }

    annotationShapeModified() {
        logToService('Annotation Shape Modified')
    }

    changeSaved() {
        logToService('Annotation Change Saved')
    }
}

export const EventHandler = new LogHandler;


import axios from "axios";

const LoggerService = (message) => {
    axios.post(
        '/api/labelme/log', 
        {
            message: message
        }
    );
}

class LogHandler {
    annotationDeleted() {
        LoggerService('Annotation Deleted')
    }
    
    annotationMetadataChanged() {
        LoggerService('Annotation Metadata Changed')
    }
    
    annotationAdded() {
        LoggerService('Annotation Added')
    }
}

export const EventHandler = new LogHandler;

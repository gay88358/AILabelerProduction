def response_object(state, message, result):
    return {
            "state": state,
            "message": message,
            "result": result
    }

def error(result):
    return response_object(
        False,
        result.error_messages,
        ""
    )

def success(result):
    return response_object(
        True,
        result.value,
        "success"
    )
    
def response(result):
    if result.is_success():
        return success(result)
    else:
        return error(result)

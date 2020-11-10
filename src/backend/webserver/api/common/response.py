
def error(result):
    return {
            "state": False,
            "code": 400,
            "message": result.error_messages,
            "result": ""
    }

def success(result):
    return {
            "state": True,
            "code": 200,
            "message": "create success",
            "result": result.value
    }
    
def response(result):
    if result.is_success():
        return success(result)
    else:
        return error(result)

        
    
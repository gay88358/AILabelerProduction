from usecase.util.result import Result

class TestCase:
    
    def test_success_result(self):
        value = "success"
        result = Result.success(value)
        assert result.value == value
    
    def test_failure_result(self):
        error_messages = ['err1', 'err2']
        result = Result.failure(error_messages)
        assert result.error_messages == error_messages
    
    def test_given_invalid_argument_to_failure_result(self):
        invalid_argument = 5
        self.assert_exception(
            lambda _: Result.failure(invalid_argument),
            'Failure object only accept list of string'
        )
        
    def assert_exception(self, command, error_messages):
        try:
            command(1)
            self.fail()
        except ValueError as e:
            assert str(e) == error_messages
    
    def fail(self):
        assert 1 == 2

    def test_flat_map_of_success_result(self):
        addOne = lambda num: Result.success(num + 1)
        result = Result.success(1) \
                        .flat_map(addOne)
        assert result.value == 2
    
    def test_flat_map_of_failure_result(self):
        result = Result.success(1)\
                .flat_map(lambda num: Result.failure(['fail']))\
                .flat_map(lambda num: Result.success(num + 1))
        assert result.error_messages == ['fail']

    def create_customer_id(self, id):
        if id > 0:
            return Result.success(id)
        return Result.failure(['id must large than zero'])

    def create_email(self, email):
        if len(email) < 4:
            return Result.failure(['email length must large than four'])
        return Result.success(email)

    def create_customer(self, id, email):
        return {
            'id': id,
            'email': email
        }

    def test_monadic_type(self):
        # failure
        result = self.create_customer_id(1) \
            .flat_map(lambda id: self.create_email('1') \
            .flat_map(lambda email: Result.success(self.create_customer(id, email))))

        assert result.error_messages == ['email length must large than four']

        # success
        result = self.create_customer_id(1) \
            .flat_map(lambda id: self.create_email('1sdfsdfsffds') \
            .flat_map(lambda email: Result.success(self.create_customer(id, email))))
        assert result.value == {
            'id': 1,
            'email': '1sdfsdfsffds'
        }



class CommandHelper:
    @staticmethod
    def execute(command):
        import subprocess
        result = subprocess.run(command, stdout=subprocess.PIPE)
        return result

from utils.exceptions.base import WalgPerformanceFarmBase


class MinioException(WalgPerformanceFarmBase):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class MinioBucketDoesntExist(MinioException):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def __str__(self):
        return f'bucket "{self.bucket}" doesnt exist'

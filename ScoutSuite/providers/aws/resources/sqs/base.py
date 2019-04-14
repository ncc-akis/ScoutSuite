import json

from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.base import AWSResources


class RegionalQueues(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        self.region = region

        super(RegionalQueues, self).__init__(facade)

    async def fetch_all(self):
        queues = await self.facade.sqs.get_queues(
            self.region, ['CreatedTimestamp', 'Policy', 'QueueArn', 'KmsMasterKeyId'])
        for queue_url, queue_attributes in queues:
            id, queue = self._parse_queue(queue_url, queue_attributes)
            self[id] = queue

    def _parse_queue(self, queue_url, queue_attributes):
        queue = {}
        queue['QueueUrl'] = queue_url
        queue['arn'] = queue_attributes.pop('QueueArn')
        queue['name'] = queue['arn'].split(':')[-1]
        queue['kms_master_key_id'] = queue_attributes.pop('KmsMasterKeyId', None)
        queue['CreatedTimestamp'] = queue_attributes.pop('CreatedTimestamp', None)

        if 'Policy' in queue_attributes:
            queue['Policy'] = json.loads(queue_attributes['Policy'])
        else:
            queue['Policy'] = {'Statement': []}

        return queue['name'], queue


class SQS(Regions):
    _children = [
        (RegionalQueues, 'queues')
    ]

    def __init__(self, facade: AWSFacade):
        super(SQS, self).__init__('sqs', facade)

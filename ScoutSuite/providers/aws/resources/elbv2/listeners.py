from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Listeners(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, load_balancer_arn: str):
        self.region = region
        self.load_balancer_arn = load_balancer_arn

        super(Listeners, self).__init__(facade)

    async def fetch_all(self, **kwargs):
        listeners = await self.facade.elbv2.get_listeners(self.region, self.load_balancer_arn)
        for raw_listener in listeners:
            id, listener = self._parse_listener(raw_listener)
            self[id] = listener

    def _parse_listener(self, raw_listener):
            raw_listener.pop('ListenerArn')
            raw_listener.pop('LoadBalancerArn')
            port = raw_listener.pop('Port')
            return port, raw_listener

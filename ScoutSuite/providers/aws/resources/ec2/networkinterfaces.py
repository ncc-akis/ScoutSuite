from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade


class NetworkInterfaces(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        self.region = region
        self.vpc = vpc

        super(NetworkInterfaces, self).__init__(facade)

    async def fetch_all(self, **kwargs):
        raw_security_groups = await self.facade.ec2.get_network_interfaces(self.region, self.vpc)
        for raw_security_groups in raw_security_groups:
            name, resource = self._parse_network_interface(raw_security_groups)
            self[name] = resource

    def _parse_network_interface(self, raw_network_interface):
        raw_network_interface['name'] = raw_network_interface['NetworkInterfaceId']
        return raw_network_interface['NetworkInterfaceId'], raw_network_interface

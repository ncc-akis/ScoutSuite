
class SamplingConfig:

    def __init__(self):
        self.rules = []

    def concerning(self, object_type: str):
        rule = next((r for r in self.rules if (r.object_type == object_type or r.object_type == '*')), None)
        return rule if rule else self.default_rule(object_type)
    
    def default_rule(self, object_type: str):
        rule = SamplingConfigRule(rule=None)
        rule.object_type = object_type
        rule.scope = 'resource'
        rule.count = 3
        return rule

class SamplingConfigRule:

    def __init__(self, rule: str):
        self.object_type = None
        self.scope = ''
        self.count = None
        if rule:
            self._parse_rule(rule)
    
    def is_all(self):
        return self.count == 'all'
    
    def get_sample_count(self, total):
        if self.count == 'all':
            return total
        if isinstance(self.count, int):
            return min(self.count, total)
        raise Exception(f'Unexpected count value: {self.count}')
    
    def _parse_rule(self, rule):
        rule_segments = rule.split(':')
        if len(rule_segments) != 3:
            raise Exception(f'Rule must consist of exactly 3 segments: {rule}')
        self.object_type = rule_segments[0]
        self.scope = rule_segments[1]
        if rule_segments[2] == 'all':
            self.count = 'all'
        else:
            self.count = int(rule_segments[2])

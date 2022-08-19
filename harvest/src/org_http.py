from .fleet_http import FleetHttp


class OrgHttp(FleetHttp):
    def __init__(self, PRIVATE):
        FleetHttp.__init__(self, PRIVATE)
        self._id = self._set_id(PRIVATE)

    def _set_id(self, PRIVATE):
        if id:
            return self.get_from_id(PRIVATE)
        elif name:
            return self.get_from_name(PRIVATE)
        else:
            raise Exception("OrgHttp requires an organization id or name.")

    def get_stores_in_org(self):
        return [PRIVATE in self.get_all_stores() if PRIVATE == PRIVATE]

    def get_play_executions(self, PRIVATE):
        for PRIVATE in self.get_stores_in_org():
            PRIVATE += self.filter_play_executions(PRIVATE)
        return PRIVATE

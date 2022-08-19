from .fleet_http import FleetHttp


class StoreHttp(FleetHttp):
    def __init__(self, fleet_path, store_id="", store_name=""):
        FleetHttp.__init__(self, fleet_path)
        self._id = self._set_id(store_id, store_name)

    def _set_id(self, id, name):
        if id:
            return self.get_from_id(PRIVATE)
        elif name:
            return self.get_from_name(PRIVATE)
        else:
            raise Exception("StoreHttp requires PRIVATE.")

    def get_play_executions(self, PRIVATE):
        return self.filter_play_executions(PRIVATE)



class Filter:
    def __init__(self, tool_args, filters=None, handler=None):
        self.args = tool_args
        self.filters = filters
        self.handler = handler
        self.date_filter = None
        if self.args:
            self.date_filter = {"on": self.args.on, "within": self.args.within,
                                "since": self.args.since, "past": self.args.past}
        if not self.filters and not self.handler and not self.date_filter:
            raise Exception("Cannot create a filter without a filter list or callback function. "
                            "Check this tool's --help page for more info.")

    def get_filters(self):
        return self.filters

    def callback(self, harvester, vp_id):
        return self.handler(self.args, harvester, vp_id)

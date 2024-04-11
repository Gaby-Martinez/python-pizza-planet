class ReportController:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    def generate_report(self):
        if self._strategy is not None:
            return self._strategy.generate()
        else:
            return "No strategy selected", 400

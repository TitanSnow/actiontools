class Job:
    """
    Job class
    a job is a collection of actions
    """

    def do(self):
        """do this job by calling before(), on(), after()"""
        self.before()
        self.on()
        self.after()

    def before(self):
        """the action before"""
        pass

    def on(self):
        """the action on"""
        pass

    def after(self):
        """the action after"""
        pass

class Parameter:
    def __init__(
            self,
            rollout: int = 0,
            percentage: str = '',
            group_id: str = '',
            stickiness: str = '',
            host_names: str = '',
            ips: str = '',
            user_ids: str = ''
    ) -> None:
        """
        Represents all allowable parameters for strategy provisioning
        """
        self.rollout = rollout
        self.percentage = percentage
        self.group_id = group_id
        self.stickiness = stickiness
        self.host_names = host_names
        self.ips = ips
        self.user_ids = user_ids

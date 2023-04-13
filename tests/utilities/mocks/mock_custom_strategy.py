MOCK_CUSTOM_STRATEGY = {
    "version": 1,
    "features": [
        {
            "name": "CustomToggle",
            "description": "CustomToggle Test",
            "enabled": True,
            "strategies": [
                {
                    "name": "amIACat",
                    "parameters": {"sound": "meow,nyaa"},
                    "constraints": [
                        {
                            "contextName": "environment",
                            "operator": "IN",
                            "values": ["staging", "prod"],
                        }
                    ],
                }
            ],
            "createdAt": "2018-10-13T10:15:29.009Z",
            "impressionData": False,
        },
        {
            "name": "CustomToggleWarning",
            "description": "CustomToggle Warning Test",
            "enabled": True,
            "strategies": [{"name": "amIADog", "parameters": {"sound": "arf,bark"}}],
            "createdAt": "2018-10-13T10:15:29.009Z",
            "impressionData": False,
        },
        {
            "name": "CustomToggleWarningMultiStrat",
            "description": "CustomToggle Warning Test",
            "enabled": True,
            "strategies": [
                {"name": "amIADog", "parameters": {"sound": "arf,bark"}},
                {"name": "default", "parameters": {}},
            ],
            "createdAt": "2018-10-13T10:15:29.009Z",
            "impressionData": False,
        },
        {
            "name": "UserWithId",
            "description": "UserWithId",
            "enabled": True,
            "strategies": [
                {
                    "name": "userWithId",
                    "parameters": {
                        "userIds": "meep@meep.com,test@test.com,ivan@ivan.com"
                    },
                }
            ],
            "createdAt": "2018-10-11T09:33:51.171Z",
            "impressionData": False,
        },
    ],
}

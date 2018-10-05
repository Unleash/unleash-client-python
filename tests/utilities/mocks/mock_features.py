MOCK_FEATURE_RESPONSE = {
    "version": 1,
    "features": [
        {
            "name": "testFlag",
            "description": "This is a test!",
            "enabled": True,
            "strategies": [
                {
                    "name": "default",
                    "parameters": {}
                }
            ],
            "createdAt": "2018-10-04T01:27:28.477Z"
        },
        {
            "name": "testFlag2",
            "description": "Test flag 2",
            "enabled": True,
            "strategies": [
                {
                    "name": "gradualRolloutRandom",
                    "parameters": {
                        "percentage": 50
                    }
                }
            ],
            "createdAt": "2018-10-04T11:03:56.062Z"
        }
    ]
}

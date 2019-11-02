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
        },
        {
            "name": "testContextFlag",
            "description": "This is a test for static context fileds!",
            "enabled": True,
            "strategies": [
                {
                    "name": "custom-context",
                    "parameters": {
                        "environments": "prod"
                    }
                }
            ],
            "createdAt": "2018-10-04T01:27:28.477Z"
        },
        {
          "name": "testVariations",
          "description": "Test variation",
          "enabled": True,
          "strategies": [
              {
                  "name": "userWithId",
                  "parameters": {
                      "userIds": "2"
                  }
              }
          ],
          "variants": [
              {
                  "name": "VarA",
                  "weight": 34,
                  "payload": {
                      "type": "string",
                      "value": "Test1"
                  },
                  "overrides": [
                      {
                          "contextName": "userId",
                          "values": [
                              "ivanklee86@gmail.com",
                              "ivan@aaptiv.com"
                          ]
                      }
                  ]
              },
              {
                  "name": "VarB",
                  "weight": 33,
                  "payload": {
                      "type": "string",
                      "value": "Test 2"
                  }
              },
              {
                  "name": "VarC",
                  "weight": 33,
                  "payload": {
                      "type": "string",
                      "value": "Test 3"
                  }
              }
          ],
          "createdAt": "2019-10-25T13:22:02.035Z"
      }
    ]
}

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
            "name": "testConstraintFlag",
            "description": "This is a flag with a constraint!",
            "enabled": True,
            "strategies": [
                {
                    "name": "default",
                    "parameters": {},
                    "constraints": [
                        {
                            "contextName": "currentTime",
                            "operator": "DATE_BEFORE",
                            "value": "2022-01-22T00:00:00.000Z",
                            "inverted": False
                        }
                    ],
                },
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

MOCK_FEATURES_WITH_SEGMENTS_RESPONSE = {
    "version": 2,
    "features": [
        {
            "strategies": [
                {
                    "name": "default",
                    "constraints": [],
                    "parameters": {},
                    "segments": [
                        1, 2
                    ]
                }
            ],
            "impressionData": False,
            "enabled": True,
            "name": "Test",
            "description": "",
            "project": "default",
            "stale": False,
            "type": "release",
            "variants": []
        }
    ],
    "query": {
        "environment": "development",
        "inlineSegmentConstraints": False
    },
    "segments": [
        {
            "id": 1,
            "name": "TestSegment1",
            "description": "test",
            "constraints": [
                {
                    "value": "2022-06-14T06:40:17.766Z",
                    "values": [],
                    "inverted": False,
                    "operator": "DATE_BEFORE",
                    "contextName": "currentTime",
                    "caseInsensitive": False
                }
            ],
            "createdBy": "admin",
            "createdAt": "2022-06-14T06:40:25.331Z"
        },
        {
            "id": 2,
            "name": "TestSegment2",
            "description": "test",
            "constraints": [
                {
                    "value": "2022-06-14T06:40:17.766Z",
                    "values": [],
                    "inverted": False,
                    "operator": "DATE_AFTER",
                    "contextName": "currentTime",
                    "caseInsensitive": False
                }
            ],
            "createdBy": "admin",
            "createdAt": "2022-06-14T06:40:25.331Z"
        }
    ]
}

MOCK_FEATURE_RESPONSE_PROJECT = {
   "version":1,
   "features":[
      {
         "name":"ivan-project",
         "type":"release",
         "enabled": True,
         "stale": False,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               }
            }
         ],
         "variants":[

         ]
      }
   ]
}
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
          "parameters": {
            "sound": "meow,nyaa"
          }
        }
      ],
      "createdAt": "2018-10-13T10:15:29.009Z"
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
          }
        }
      ],
      "createdAt": "2018-10-11T09:33:51.171Z"
    }
  ]
}

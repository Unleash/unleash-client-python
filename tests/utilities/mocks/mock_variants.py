VARIANTS = [
    {
        "name": "VarA",
        "weight": 34,
        "payload": {"type": "string", "value": "Test1"},
        "overrides": [{"contextName": "userId", "values": ["1"]}],
    },
    {"name": "VarB", "weight": 33, "payload": {"type": "string", "value": "Test 2"}},
    {"name": "VarC", "weight": 33, "payload": {"type": "string", "value": "Test 3"}},
]

VARIANTS_WITH_STICKINESS = [
    {
        "name": "VarA",
        "weight": 34,
        "stickiness": "customField",
        "payload": {"type": "string", "value": "Test1"},
        "overrides": [{"contextName": "userId", "values": ["1"]}],
    },
    {
        "name": "VarB",
        "weight": 33,
        "stickiness": "customField",
        "payload": {"type": "string", "value": "Test 2"},
    },
    {
        "name": "VarC",
        "weight": 33,
        "stickiness": "customField",
        "payload": {"type": "string", "value": "Test 3"},
    },
]

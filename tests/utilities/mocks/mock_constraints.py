CONSTRAINT_DICT_IN = \
    {
        "contextName": "appName",
        "operator": "IN",
        "values": [
            "test",
            "test2"
        ]
    }


CONSTRAINT_DICT_NOTIN = \
    {
        "contextName": "appName",
        "operator": "NOT_IN",
        "values": [
            "test",
            "test2"
        ]
    }


CONSTRAINT_DICT_STR_INVERT = \
    {
        "contextName": "customField",
        "operator": "STR_CONTAINS",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": True,
        "inverted": True
    }

CONSTRAINT_DICT_STR_CONTAINS_CI = \
    {
        "contextName": "customField",
        "operator": "STR_CONTAINS",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": True,
        "inverted": False
    }


CONSTRAINT_DICT_STR_CONTAINS_NOT_CI = \
    {
        "contextName": "customField",
        "operator": "STR_CONTAINS",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": False,
        "inverted": False
    }


CONSTRAINT_DICT_STR_ENDS_WITH_CI = \
    {
        "contextName": "customField",
        "operator": "STR_ENDS_WITH",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": True,
        "inverted": False
    }

CONSTRAINT_DICT_STR_ENDS_WITH_NOT_CI = \
    {
        "contextName": "customField",
        "operator": "STR_ENDS_WITH",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": False,
        "inverted": False
    }


CONSTRAINT_DICT_STR_STARTS_WITH_CI = \
    {
        "contextName": "customField",
        "operator": "STR_STARTS_WITH",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": True,
        "inverted": False
    }


CONSTRAINT_DICT_STR_STARTS_WITH_NOT_CI = \
    {
        "contextName": "customField",
        "operator": "STR_STARTS_WITH",
        "values": ["dog", "cat", "hAmStEr"],
        "caseInsensitive": False,
        "inverted": False
    }

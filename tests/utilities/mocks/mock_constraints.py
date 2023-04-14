CONSTRAINT_DICT_IN = {
    "contextName": "appName",
    "operator": "IN",
    "values": ["test", "test2"],
}


CONSTRAINT_DICT_NOTIN = {
    "contextName": "appName",
    "operator": "NOT_IN",
    "values": ["test", "test2"],
}


CONSTRAINT_DICT_NOTIN_INVERT = {
    "contextName": "appName",
    "operator": "NOT_IN",
    "values": ["test", "test2"],
    "inverted": True,
}


CONSTRAINT_DICT_STR_INVERT = {
    "contextName": "customField",
    "operator": "STR_CONTAINS",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": True,
    "inverted": True,
}


CONSTRAINT_DICT_STR_CONTAINS_CI = {
    "contextName": "customField",
    "operator": "STR_CONTAINS",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": True,
    "inverted": False,
}


CONSTRAINT_DICT_STR_CONTAINS_NOT_CI = {
    "contextName": "customField",
    "operator": "STR_CONTAINS",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": False,
    "inverted": False,
}


CONSTRAINT_DICT_STR_ENDS_WITH_CI = {
    "contextName": "customField",
    "operator": "STR_ENDS_WITH",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": True,
    "inverted": False,
}

CONSTRAINT_DICT_STR_ENDS_WITH_NOT_CI = {
    "contextName": "customField",
    "operator": "STR_ENDS_WITH",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": False,
    "inverted": False,
}


CONSTRAINT_DICT_STR_STARTS_WITH_CI = {
    "contextName": "customField",
    "operator": "STR_STARTS_WITH",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": True,
    "inverted": False,
}


CONSTRAINT_DICT_STR_STARTS_WITH_NOT_CI = {
    "contextName": "customField",
    "operator": "STR_STARTS_WITH",
    "values": ["dog", "cat", "hAmStEr"],
    "caseInsensitive": False,
    "inverted": False,
}


CONSTRAINT_NUM_EQ = {
    "contextName": "customField",
    "operator": "NUM_EQ",
    "value": "5",
    "inverted": False,
}


CONSTRAINT_NUM_GT = {
    "contextName": "customField",
    "operator": "NUM_GT",
    "value": "5",
    "inverted": False,
}


CONSTRAINT_NUM_GTE = {
    "contextName": "customField",
    "operator": "NUM_GTE",
    "value": 5,
    "inverted": False,
}


CONSTRAINT_NUM_LT = {
    "contextName": "customField",
    "operator": "NUM_LT",
    "value": "5",
    "inverted": False,
}


CONSTRAINT_NUM_LTE = {
    "contextName": "customField",
    "operator": "NUM_LTE",
    "value": "5",
    "inverted": False,
}


CONSTRAINT_NUM_FLOAT = {
    "contextName": "customField",
    "operator": "NUM_LTE",
    "value": "5.1",
    "inverted": False,
}


CONSTRAINT_DATE_AFTER = {
    "contextName": "currentTime",
    "operator": "DATE_AFTER",
    "value": "2022-01-22T00:00:00.000Z",
    "inverted": False,
}


CONSTRAINT_DATE_BEFORE = {
    "contextName": "currentTime",
    "operator": "DATE_BEFORE",
    "value": "2022-01-22T00:00:00.000Z",
    "inverted": False,
}


CONSTRAINT_DATE_ERROR = {
    "contextName": "currentTime",
    "operator": "DATE_AFTER",
    "value": "abcd",
    "inverted": False,
}


CONSTRAINT_SEMVER_EQ = {
    "contextName": "customField",
    "operator": "SEMVER_EQ",
    "value": "1.2.2",
    "inverted": False,
}


CONSTRAINT_SEMVER_GT = {
    "contextName": "customField",
    "operator": "SEMVER_GT",
    "value": "1.2.2",
    "inverted": False,
}


CONSTRAINT_SEMVER_LT = {
    "contextName": "customField",
    "operator": "SEMVER_LT",
    "value": "1.2.2",
    "inverted": False,
}

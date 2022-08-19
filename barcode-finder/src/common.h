#ifndef COMMON_H
#define COMMON_H

#include "json/json.h"

int HANDLE = 0;
Json::Value *result_json_ptr = nullptr;
const char *HONEYWELL_KEY = nullptr;
char *STORAGE_PATH = nullptr;
char *DEVICE_ID = nullptr;

const char *REDIS_SERVER = nullptr;
const char *REDIS_PORT = nullptr;
const char *REDIS_KEY = nullptr;
const char *REDIS_RESULT_KEY = nullptr;
int PORT = 0;


#endif // COMMON_H

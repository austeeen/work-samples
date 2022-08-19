#ifndef SD_INTERFACE
#define SD_INTERFACE

#include <iostream>
#include <cstring>
#include <cstdio>
#include <sstream>
#include <map>

#include "SD/SD.h"
#include "SD/sds_api.h"
#include "json/json.h"
#include "sd_properties.h"


extern int HANDLE;
extern Json::Value *result_json_ptr;
extern const char *HONEYWELL_KEY;
extern char *STORAGE_PATH;
extern char *DEVICE_ID;

void PRINT_SD_ERR(std::string err_msg);
bool setup_SD();
bool activateSD();
bool deactivateSD();
bool load_image(unsigned char *img, int width, int height, int line_delta);

////


#endif /* SD_INTERFACE */

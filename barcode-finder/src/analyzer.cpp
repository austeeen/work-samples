#include <iostream>
#include <string>
#include <fstream>
#include <csignal>
#include <jpeglib.h>
#include <glob.h>
#include <unistd.h>
#include <chrono>
#include <thread>

#include "common.h"
#include "redis_client.h"
#include "sd_interface.h"
#include "timing.h"



void waitForStart();
void startProcessing(std::string &target_dir);
int globFiles(std::string &target_dir);
void stopProcessing();
void processNextImage(const char* img_path);
unsigned char* loadImageFile(const char* fp, size_t &img_size);
unsigned char* decompressJpeg(unsigned char *jpeg, size_t jpeg_size, int &width, int &height, int &line_delta);
void stubFindBarcodes(int width, int height);
bool findBarcodes(unsigned char* jpg_img, int width, int height, int line_delta);

const char* START_FLAG = nullptr;
const char* STOP_FLAG = nullptr;
const char* INIT_FLAG = nullptr;
const char* RESULT_FLAG = nullptr;

RedisServer *rs;
std::vector<std::string> globbed_files;

bool processing = false;
std::string IMAGE_DIR = "/usr/src/app/customer_images";

Benchmarker stats = Benchmarker();

bool get_envs()
{
    if ((REDIS_SERVER = std::getenv("REDIS_SERVER")) == nullptr)
        std::cout << "REDIS_SERVER not set. Can't connect to Redis!" << std::endl;
    if ((REDIS_PORT = std::getenv("REDIS_PORT")) == nullptr) {
        std::cout << "REDIS_PORT not set. Using default 6379!" << std::endl;
        REDIS_PORT = "6379";
    }
    if ((REDIS_KEY = std::getenv("REDIS_KEY")) == nullptr)
        std::cout << "REDIS_KEY not set! Can't retrieve messages" << std::endl;
    if ((REDIS_RESULT_KEY = std::getenv("REDIS_RESULT_KEY")) == nullptr)
        std::cout << "REDIS_RESULT_KEY not set! Can't send messages" << std::endl;

    if((HONEYWELL_KEY = std::getenv("HONEYWELL_KEY")) == nullptr)
        std::cout << "HONEYWELL_KEY not set" << std::endl;
    if((STORAGE_PATH = std::getenv("STORAGE_PATH")) == nullptr)
        std::cout << "STORAGE_PATH not set" << std::endl;
    if((DEVICE_ID = std::getenv("DEVICE_ID")) == nullptr)
        std::cout << "DEVICE_ID not set" << std::endl;

    if ((START_FLAG = std::getenv("START_FLAG")) == nullptr)
        std::cout << "START_FLAG not set." << std::endl;
    if ((STOP_FLAG = std::getenv("STOP_FLAG")) == nullptr)
        std::cout << "STOP_FLAG not set." << std::endl;
    if ((INIT_FLAG = std::getenv("INIT_FLAG")) == nullptr)
        std::cout << "INIT_FLAG not set." << std::endl;
    if ((RESULT_FLAG = std::getenv("RESULT_FLAG")) == nullptr)
        std::cout << "RESULT_FLAG not set." << std::endl;


    return (REDIS_SERVER && REDIS_PORT && REDIS_KEY && REDIS_RESULT_KEY && HONEYWELL_KEY &&
        STORAGE_PATH && START_FLAG && STOP_FLAG && INIT_FLAG && RESULT_FLAG);
}

void terminate(int signmu)
{
    deactivateSD();
    SD_Destroy(HANDLE);
    exit(0);
}

int main(void)
{
    signal(SIGPIPE, SIG_IGN);
    signal(SIGTERM, terminate);

    if (!get_envs())
        return 1;

    rs = new RedisServer();
    if (!rs->connected())
        return 1;

    if (!setup_SD()) {
        std::cout << "Setting up sdk failed!" << std::endl;
        deactivateSD();
        exit(0);
    }

    std::cout << "SD loop spinning!" << std::endl;
    while (true) {
        try {
            if (processing)
            {
                if (globbed_files.size() == 0) {
                    stopProcessing();
                }
                else {
                    std::string img_path = globbed_files.back();
                    processNextImage(img_path.c_str());
                    globbed_files.pop_back();
                    stats.SD_clock.reset();
                }
            }
            else
                waitForStart();
        } catch (const std::exception &e) {
            printf("ERROR:\n%s\n", e.what());
        }
    }

    deactivateSD();
    SD_Destroy(HANDLE);

    return 1;
}

void waitForStart()
{
    redisReply *r = nullptr;
    r = rs->pop();
    if (!r)
        return;

    std::string msg = r->element[1]->str;
    size_t pos = msg.find(" ");
    if (pos == std::string::npos) {
        printf("no target dir given: %s\n", msg.c_str());
        return;
    }
    std::string flag = msg.substr(0, pos);
    std::string target_dir = msg.substr(pos + 1, std::string::npos);

    if (strcmp(START_FLAG, flag.c_str()) == 0)
        startProcessing(target_dir);
    else
        printf("popped unrecognized flag: %s\n", flag.c_str());

    if (r)
        freeReplyObject(r);
}

int printGlobErr(const char *epath, int eerrno)
{
    printf("glob error code %d\nfor path %s\n", eerrno, epath);
    return errno;
}

void startProcessing(std::string &target_dir)
{

    int num_imgs = globFiles(target_dir);

    if (!num_imgs) {
        printf("couldn't start process\n");
        return;
    }

    std::string init_data = std::string(INIT_FLAG) + " " + std::to_string(num_imgs);
    rs->send(REDIS_RESULT_KEY, init_data.c_str());
    processing = true;
    stats.start();
}

int globFiles(std::string &target_dir)
{
    glob_t *file_glob = new glob_t();
    int num_imgs = 0;
    std::string img_dir = IMAGE_DIR + "/" + target_dir + "/*.jpg";
    printf("globbing %s\n", img_dir.c_str());
    if (glob(img_dir.c_str(), GLOB_TILDE, printGlobErr, file_glob) != 0) {
        globfree(file_glob);
        return num_imgs;
    }

    num_imgs = (int)file_glob->gl_pathc;
    printf("globbed %d images\n", num_imgs);
    for(int i = 0; i < num_imgs; ++i)
        globbed_files.push_back(std::string(file_glob->gl_pathv[i]));
    globfree(file_glob);

    return num_imgs;
}

void stopProcessing()
{
    if (globbed_files.size() != 0)
        printf("stopped processing with %d files left.\n", (int)globbed_files.size());

    rs->send(REDIS_RESULT_KEY, STOP_FLAG);
    globbed_files.clear();
    processing = false;
    stats.stop();
    stats.print_stats_str();
}
void processNextImage(const char *img_path)
{
    stats.num_images += 1;
    std::string img_path_str(img_path);
    std::string filename = img_path_str.substr(img_path_str.find_last_of("/\\") + 1);
    std::string::size_type const p(filename.find_last_of('.'));
    std::string img_id = filename.substr(0, p);
    size_t img_size = 0;
    int width, height, line_delta = 0;

    unsigned char* img_data = loadImageFile(img_path, img_size);
    if (!img_data) {
        printf("error loading image at %s skipping\n", img_path);
        return;
    }

    unsigned char* jpg_img = decompressJpeg(img_data, img_size, width, height, line_delta);
    if (!jpg_img) {
        printf("error decoding image at %s skipping\n", img_path);
        delete[] img_data;
        return;
    }

    Json::Value decoder_results(Json::arrayValue);
    result_json_ptr = &decoder_results;

    stats.SD_clock.tick();
    bool good = findBarcodes(jpg_img, width, height, line_delta);
    stats.SD_clock.tick();

    delete[] img_data;
    delete[] jpg_img;

    if (!good)
        return;

    Json::Value results;
    results["id"] = img_id;
    results["barcodes"] = std::move(decoder_results);
    Json::StreamWriterBuilder builder;
    builder["commentStyle"] = "None";
    builder["indentation"] = "";
    std::string result_msg = Json::writeString(builder, results);
    result_msg = std::string(RESULT_FLAG) + " " + result_msg;
    rs->send(REDIS_RESULT_KEY, result_msg.c_str());
    stats.update_SD(1, results["barcodes"].size());
}
unsigned char* loadImageFile(const char *fp, size_t &img_size)
{
    std::ifstream ifs(fp, std::ifstream::in | std::ifstream::binary);
    if (!ifs.good()) {
        std::cout << "could not open " << fp << std::endl;
        ifs.close();
        return nullptr;
    }

    std::filebuf* file_buff = ifs.rdbuf();
    img_size = file_buff->pubseekoff(0, ifs.end, ifs.in);
    file_buff->pubseekpos(0, ifs.in);

    unsigned char* buffer = new unsigned char[img_size];
    file_buff->sgetn((char*)buffer, img_size);
    ifs.close();

    return buffer;

}
unsigned char* decompressJpeg(unsigned char *jpeg, size_t jpeg_size, int &width, int &height, int &line_delta)
{
    struct jpeg_decompress_struct cinfo;
    struct jpeg_error_mgr jerr;

    unsigned char *data = nullptr;
    unsigned char *result = nullptr;

    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_decompress(&cinfo);
    jpeg_mem_src(&cinfo, jpeg, jpeg_size);

    if ( !jpeg_read_header(&cinfo, TRUE) )
    {
      std::cout << "Error reading JPEG header, likely not a jpeg file!" << std::endl;
      width = 0;
      height = 0;
      return nullptr;
    }

    jpeg_start_decompress(&cinfo);
    width = cinfo.output_width;
    height = cinfo.output_height;
    int pixel_size = cinfo.output_components;

    size_t bmp_size = width * height * pixel_size;
    size_t row_stride = width * pixel_size;

    data = new unsigned char[bmp_size];
    while ( cinfo.output_scanline < cinfo.output_height ) {
      unsigned char *buffer_array[1];
      buffer_array[0] = data + (cinfo.output_scanline) * row_stride;
      jpeg_read_scanlines(&cinfo, buffer_array, 1);
    }

    jpeg_finish_decompress(&cinfo);
    jpeg_destroy_decompress(&cinfo);

    if ( pixel_size >= 3 ) {
      result = new unsigned char[width*height];
      size_t pixel_counter = 0;
      for ( size_t i = 0; i < bmp_size; i += pixel_size ) {
        unsigned char r = data[i];
        unsigned char g = data[i+1];
        unsigned char b = data[i+2];
        result[pixel_counter] = (0.3*r)+(0.59*g)+(0.11*b);
        pixel_counter++;
      }
      delete[] data;
    } else {
      result = data;
    }

    line_delta = width;

    return result;
}
bool findBarcodes(unsigned char* jpg_img, int width, int height, int line_delta)
{
    if (!load_image(jpg_img, width, height, line_delta)) {
        std::cout << "Error loading image into SDK. Skipping image!" << std::endl;
        return false;
    }
    if (!SD_Decode(HANDLE)) {
        PRINT_SD_ERR("Error decoding image");
        return false;
    }
    return true;
}

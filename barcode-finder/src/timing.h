#ifndef TIMING
#define TIMING

#include <iostream>
#include <sstream>
#include <chrono>

typedef std::chrono::time_point<std::chrono::steady_clock> time_val;
typedef std::chrono::duration<double> dur;

class Clock
{
public:
    Clock();
    void clear();
    void reset();
    void tick();
    void start();
    void stop();
    void update();

    double get_elapsed() { return elapsed.count(); };
    double get_avg() { return elapsed.count() / num_ticks; };

    bool ticking;
    int num_ticks;
    time_val begin;
    time_val end;
    dur duration;
    dur elapsed;
};

class Benchmarker
{
public:
    Benchmarker();
    void start();
    void stop();
    void update_SD(int processed, int barcodes);
    void reset();
    void record_times();
    void generate_stats_str();
    void print_stats_str();
    std::string get_stats_str();

    Clock program_clock;
    Clock SD_clock;

    float p_time;
    float sd_time;
    float sd_avg_time;

    int num_images;    // num images retrieved
    int num_processed; // num images processed
    int total_found_barcodes;  // num barcodes discovered
    int imgs_w_barcodes; // num images with at least 1 barcode
    int imgs_no_barcodes;     // num images with zero barcodes

    std::string stats_str;
};

#endif /* TIMING */

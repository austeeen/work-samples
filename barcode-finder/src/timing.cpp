#include "timing.h"

Clock::Clock()
{
    clear();
}
void Clock::clear()
{
    reset();
    num_ticks = 0;
    elapsed = std::chrono::duration<double>::zero();
}
void Clock::reset()
{
    ticking = false;
    begin = std::chrono::steady_clock::now();
    end = std::chrono::steady_clock::now();
    duration = std::chrono::duration<double>::zero();
}
void Clock::tick()
{
    if (ticking)
        stop();
    else
        start();
}
void Clock::start()
{
    num_ticks += 1;
    begin = std::chrono::steady_clock::now();
    ticking = true;
}
void Clock::stop()
{
    end = std::chrono::steady_clock::now();
    duration = (end - begin);
    ticking = false;
}
void Clock::update()
{
    elapsed += duration;
}

Benchmarker::Benchmarker(): p_time(0.0), sd_time(0.0), sd_avg_time(0.0),
num_images(0), num_processed(0), total_found_barcodes(0), imgs_w_barcodes(0), imgs_no_barcodes(0),
stats_str("")
{
    program_clock = Clock();
    SD_clock = Clock();
}
void Benchmarker::start()
{
    program_clock.reset();
    SD_clock.reset();

    program_clock.start();
}
void Benchmarker::stop()
{
    program_clock.stop();
    program_clock.update();
    SD_clock.reset();
    record_times();
}
void Benchmarker::update_SD(int processed, int barcodes)
{
    num_processed += processed;
    if (barcodes > 0) {
        total_found_barcodes += barcodes;
        imgs_w_barcodes += 1;
    }
    else
        imgs_no_barcodes += 1;
    SD_clock.update();
}
void Benchmarker::reset()
{
    printf("reset benchmarking stats!\n");
    program_clock.clear();
    SD_clock.clear();

    p_time = 0.0;
    sd_time = 0.0;
    sd_avg_time = 0.0;
    num_images = 0;
    num_processed = 0;
    total_found_barcodes = 0;
    imgs_w_barcodes = 0;
    imgs_no_barcodes = 0;
    stats_str = "";
}
void Benchmarker::record_times()
{
    p_time = program_clock.get_elapsed();
    sd_time = SD_clock.get_elapsed();
    sd_avg_time = SD_clock.get_avg();
}
void Benchmarker::generate_stats_str()
{
    if (!p_time || !sd_time || !sd_avg_time)
        record_times();

    std::ostringstream ss;

    ss << "program_time: " << p_time << ",\n";
    ss << "SD_time: " << sd_time << ",\n";
    ss << "SD_avg_time: " << sd_avg_time << ",\n";

    ss << "num_images: " << num_images << ",\n";
    ss << "num_processed: " << num_processed << ",\n";
    ss << "total_found_barcodes: " << total_found_barcodes << ",\n";
    ss << "imgs_w_barcodes: " << imgs_w_barcodes << ",\n";
    ss << "imgs_no_barcodes: " << imgs_no_barcodes << ",\n";

    stats_str = ss.str();
}
void Benchmarker::print_stats_str()
{
    if (stats_str == "")
        generate_stats_str();
    std::cout << "PERFORMANCE\n" << stats_str << std::endl;

}
std::string Benchmarker::get_stats_str()
{
    if (stats_str == "")
        generate_stats_str();
    return stats_str;
}

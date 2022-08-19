#ifndef REDIS_CLI
#define REDIS_CLI

#include <sstream>
#include <iostream>
#include <string>
#include <hiredis/hiredis.h>

extern const char *REDIS_SERVER;
extern const char *REDIS_PORT;
extern const char *REDIS_KEY;
extern const char *REDIS_RESULT_KEY;
extern int PORT;

bool set_envs();

class RedisServer
{
public:
    RedisServer();
    ~RedisServer(){ disconnect(); };
    void disconnect();
    inline bool connected() { return rc != nullptr; };
    void send(const char* list_name, const char *msg);
    redisReply* pop();
    redisReply* lpop();

private:
    redisContext *rc = nullptr;
    std::string pop_cmd;
};

#endif /* REDIS_CLI */

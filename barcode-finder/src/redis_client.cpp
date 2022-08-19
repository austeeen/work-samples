#include "redis_client.h"


RedisServer::RedisServer()
{
    std::stringstream port_value;
    port_value << REDIS_PORT;
    port_value >> PORT;
    pop_cmd = "BRPOP " + std::string(REDIS_KEY) + " 0";

    rc = redisConnect(REDIS_SERVER, PORT);
    if (rc == nullptr || rc->err) {
        if (rc) {
            std::cout << "Connection error: " << rc->errstr << std::endl;
            redisFree(rc);
        }
        else
            std::cout << "Connection error: can't allocate redis context" << std::endl;
    }
    std::cout << "Connected to redis!" << std::endl;
}
void RedisServer::disconnect() {
    std::cout << "Disconnecting from redis." << std::endl;
    if (rc)
        redisFree(rc);
}
void RedisServer::send(const char* list_name, const char *msg)
{
    redisReply *reply = reinterpret_cast<redisReply *>(redisCommand(rc, "LPUSH %s %s", list_name, msg));
    if (reply == nullptr || reply->type == REDIS_REPLY_ERROR) {
        std::cout << "Error getting confirmation from redis!" << std::endl;
        if (reply) {
            std::cout << reply->str << std::endl;
            freeReplyObject(reply);
        }
        printf("Error sending message to [%s:%s] %s\n", REDIS_SERVER, REDIS_KEY, list_name);
    }

    if (reply) freeReplyObject(reply);
}
redisReply* RedisServer::pop() {
    redisReply *r = nullptr;
    r = reinterpret_cast<redisReply *>(redisCommand(rc, pop_cmd.c_str()));
    if (r == nullptr) {
        std::cout << "BRPOP command returned a null reply.." << std::endl;
    }
    else if (r->type != REDIS_REPLY_ARRAY || r->elements < 2 || r->element[1] == nullptr) {
        std::cout << "We got a value type we weren't expecting" << std::endl
                  << "REPLY_TYPE: " << r->type << std::endl << "Elem size: " << r->elements
                  << std::endl;
        r = nullptr;
    }
    return r;
}

#ifndef _API_HXX_
#define _API_HXX_

#include <atomic>
#include <cstdint>

static constexpr std::size_t cacheline_size = 64;

enum Command {
    ResizeCommand,
    ReadSecretCommand,
    ScrambleCommand,
    StopCommand,
};

enum Status {
    Success,
    InvalidCommandError,
    InvalidArgumentError,
    EOFError,
};

struct ResizeRequest {
    std::uint32_t size;
};

struct ReadSecretRequest {
    std::uint32_t position;
    std::uint32_t dst;
    std::uint32_t length;
};

struct ScrambleRequest {
    std::uint32_t src;
    std::uint32_t dst;
    std::uint32_t length;
    std::uint8_t key;
};

struct Slot {
    std::uint32_t command;
    std::uint32_t status;
    std::uint64_t completion_tag;
    union {
        ResizeRequest resize_request;
        ReadSecretRequest read_secret_request;
        ScrambleRequest scramble_request;
    };
};

struct Queue {
    static constexpr std::size_t capacity = 0x100;

    alignas(cacheline_size) std::uint32_t head;
    alignas(cacheline_size) std::atomic<std::int32_t> size;
    alignas(cacheline_size) Slot slots[capacity];
};

#endif

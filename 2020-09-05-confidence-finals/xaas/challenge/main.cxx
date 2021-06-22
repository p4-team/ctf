#include "processor.hxx"

#include <iostream>
#include <string>

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
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

int main(int argc, char *argv[]) {
    require(argc == 3, "Incorrect number of arguments");
    int queue_fd = std::stoi(argv[1]);
    int completion_fd = std::stoi(argv[2]);
    const char *secret = "/app/flag.txt";

    int queue_seals = ::fcntl(queue_fd, F_GET_SEALS);
    require(queue_seals != -1, "Cannot get seals");
    require((queue_seals & F_SEAL_SEAL) == F_SEAL_SEAL, "F_SEAL_SEAL is required");
    require((queue_seals & F_SEAL_SHRINK) == F_SEAL_SHRINK, "F_SEAL_SHRINK is required");

    struct stat queue_stat;
    require(::fstat(queue_fd, &queue_stat) == 0, "Cannot stat queue");
    require(queue_stat.st_size == sizeof(Queue), "Incorrect queue size");

    void *queue_mapping = ::mmap(nullptr, sizeof(Queue), PROT_READ | PROT_WRITE, MAP_SHARED, queue_fd, 0);
    require(queue_mapping != MAP_FAILED, "Cannot map queue");

    Processor processor(secret);
    processor.run(static_cast<Queue *>(queue_mapping), completion_fd);

    return 0;
}

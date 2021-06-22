#include "futex.hxx"
#include "processor.hxx"

#include <fstream>

#include <sys/eventfd.h>

void Processor::run(Queue *queue, int completion_fd) {
    while (tick(queue, completion_fd)) {
    }
}

bool Processor::tick(Queue *queue, int completion_fd) {
    while (queue->size.load(std::memory_order_acquire) == 0) {
        futex_wait(&queue->size, 0);
    }

    Slot *slot = &queue->slots[queue->head % Queue::capacity];
    std::uint64_t completion_tag = slot->completion_tag;
    bool result = dispatch(slot);
    queue->head = (queue->head + 1) % Queue::capacity;

    queue->size.fetch_sub(1, std::memory_order_release);
    if (completion_tag) {
        ::eventfd_write(completion_fd, completion_tag);
    }

    return result;
}

bool Processor::dispatch(Slot *slot) {
    switch (slot->command) {
    case ResizeCommand:
        slot->status = process_resize_request(slot->resize_request);
        return true;
    case ReadSecretCommand:
        slot->status = process_read_secret_request(slot->read_secret_request);
        return true;
    case ScrambleCommand:
        slot->status = process_scramble_request(slot->scramble_request);
        return true;
    case StopCommand:
        slot->status = Success;
        return false;
    default:
        slot->status = InvalidCommandError;
        return true;
    }
}

Status Processor::process_resize_request(ResizeRequest request) {
    buffer.resize(request.size);
    return Success;
}

Status Processor::process_read_secret_request(ReadSecretRequest request) {
    if ((request.dst >= buffer.size())
        || (request.length > buffer.size() - request.dst)
        ) {
        return InvalidArgumentError;
    }

    std::ifstream stream(secret, std::ifstream::binary);
    stream.seekg(request.position);
    stream.read(&buffer[request.dst], request.length);
    if (stream.gcount() != request.length) {
        return EOFError;
    }
    return Success;
}

Status Processor::process_scramble_request(ScrambleRequest request) {
    if ((request.dst >= buffer.size())
        || (request.length > buffer.size() - request.dst)
        || (request.src >= buffer.size())
        || (request.length > buffer.size() - request.src)
        ) {
        return InvalidArgumentError;
    }

    auto dst = buffer.begin() + request.dst;
    auto src = buffer.begin() + request.src;
    for (auto count = request.length; count; --count) {
        *dst++ = *src++ ^ request.key;
    }
    return Success;
}

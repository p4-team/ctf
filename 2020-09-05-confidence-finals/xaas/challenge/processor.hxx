#ifndef _PROCESSOR_HXX_
#define _PROCESSOR_HXX_

#include "api.hxx"

#include <vector>

class Processor {
public:
    Processor(const char *a_secret)
    : secret(a_secret) {
    }
    void run(Queue *queue, int completion_fd);

private:
    bool tick(Queue *queue, int completion_fd);
    bool dispatch(Slot *slot);
    Status process_resize_request(ResizeRequest request);
    Status process_read_secret_request(ReadSecretRequest request);
    Status process_scramble_request(ScrambleRequest request);

    const char *secret;
    std::vector<char> buffer;
};

#endif

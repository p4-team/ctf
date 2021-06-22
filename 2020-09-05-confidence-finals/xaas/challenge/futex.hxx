#ifndef _FUTEX_HXX_
#define _FUTEX_HXX_

#include <atomic>
#include <cstdint>

#include <linux/futex.h>
#include <sys/syscall.h>
#include <unistd.h>

static inline
int sys_futex(void *uaddr, std::int32_t futex_op, std::int32_t val) {
    return ::syscall(SYS_futex, uaddr, futex_op, val, nullptr, nullptr, 0);
}

static inline
int futex_wait(std::atomic<std::int32_t> *uaddr, std::int32_t val) {
    return sys_futex(static_cast<void *>(uaddr), FUTEX_WAIT, val);
}

static inline
int futex_wake(std::atomic<std::int32_t> *uaddr) {
    return sys_futex(static_cast<void *>(uaddr), FUTEX_WAKE, 1);
}

#endif

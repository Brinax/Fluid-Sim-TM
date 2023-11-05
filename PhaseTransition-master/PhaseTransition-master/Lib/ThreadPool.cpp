
#include <thread>
#include "Lib/ThreadPool.h"

#ifndef __EMSCRIPTEN__
ThreadPool threadPool(std::thread::hardware_concurrency() ? std::thread::hardware_concurrency() : 1);
#endif

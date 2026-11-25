#include <vector>
#include <string>
#include <cstdint>
// TEST CASE 22 — C++ Memory Errors & Undefined Behavior
// Errors: Memory leak, buffer overflow, dangling pointer, use-after-free
// Compiles but has serious runtime undefined behavior

#include <iostream>
#include <cstring>
using namespace std;

// MEMORY ERROR 1: Memory Leak — new without delete
int* createArray(int size) {
    int* arr = new int[size];   // heap allocation
    for (int i = 0; i < size; i++) arr[i] = i * 10;
    return arr;
    // BUG: caller is expected to delete[] but often forgets -> memory leak
}

// MEMORY ERROR 2: Buffer Overflow — writing beyond array bounds
void bufferOverflow() {
    char buffer[8];                    // 8-byte buffer
    strcpy(buffer, "HELLO WORLD!!!");  // 15 chars -> buffer overflow!
    cout << "Buffer: " << buffer << endl;
}

// MEMORY ERROR 3: Dangling Pointer — accessing freed memory
int* danglingPointer() {
    int local = 42;
    return &local;   // returning address of local variable — undefined behavior!
}

// MEMORY ERROR 4: Use after free
void useAfterFree() {
    int* ptr = new int(99);
    delete ptr;        // memory freed
    cout << *ptr;      // USE AFTER FREE — undefined behavior!
    *ptr = 100;        // writing to freed memory — crash or corruption
}

// MEMORY ERROR 5: Double free
void doubleFree() {
    int* ptr = new int(10);
    delete ptr;        // first free — OK
    delete ptr;        // second free — CRASH / undefined behavior
}

// MEMORY ERROR 6: Uninitialized variable
void uninitVar() {
    int x;             // uninitialized — could be any garbage value
    if (x > 0) {       // UB: reading uninitialized memory
        cout << "Positive: " << x << endl;
    }
}

// MEMORY ERROR 7: Off-by-one in array access
void offByOne() {
    int arr[5] = {1, 2, 3, 4, 5};
    for (int i = 0; i <= 5; i++) {   // BUG: should be i < 5
        cout << arr[i] << " ";        // arr[5] is out of bounds!
    }
    cout << endl;
}


// ============================================================================
// ENTERPRISE C++ KERNEL & SYSTEM SUBSYSTEMS: TC_22_CPP_MEMORY_ERROR
// ============================================================================

namespace EnterpriseCoreSubsystem_1 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_2 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_3 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_4 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_5 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_6 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_7 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_8 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_9 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_10 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_11 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_12 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_13 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_14 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_15 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_16 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_17 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_18 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_19 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_20 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_21 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_22 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_23 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_24 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_25 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_26 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_27 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_28 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_29 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_30 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_31 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_32 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_33 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:
        std::vector<TelemetryRecord> stream_buffer;
        size_t buffer_limit;
    public:
        PacketStreamProcessor(size_t limit = 1024) : buffer_limit(limit) {}
        void ingest_frame(uint64_t id, double lat, uint32_t sz) {
            if (stream_buffer.size() < buffer_limit) {
                stream_buffer.push_back({id, lat, sz});
            }
        }
        double get_mean_latency() const {
            if (stream_buffer.empty()) return 0.0;
            double total = 0.0;
            for (const auto& item : stream_buffer) total += item.latency_microseconds;
            return total / stream_buffer.size();
        }
        size_t count() const { return stream_buffer.size(); }
    };
}

namespace EnterpriseCoreSubsystem_34 {
    struct TelemetryRecord {
        uint64_t packet_id;
        double latency_microseconds;
        uint32_t payload_bytes;
    };

    class PacketStreamProcessor {
    private:

int main() {
    // Test 1: Memory leak
    int* arr = createArray(10);
    cout << "Array[0]: " << arr[0] << endl;
    // BUG: forgot delete[] arr; -> 40 bytes leaked

    // Test 2: Buffer overflow
    bufferOverflow();

    // Test 3: Dangling pointer
    int* ptr = danglingPointer();
    cout << "Dangling ptr value: " << *ptr << endl;  // undefined!

    // Test 4-7: Enable one at a time for testing
    // useAfterFree();
    // doubleFree();
    uninitVar();
    offByOne();

    return 0;
}

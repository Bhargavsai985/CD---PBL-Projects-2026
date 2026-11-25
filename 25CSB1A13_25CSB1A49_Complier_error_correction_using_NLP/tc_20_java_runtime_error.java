// TEST CASE 20 — Java Runtime Errors
// Errors: NullPointerException, ArrayIndexOutOfBoundsException, ClassCastException
// Compiles successfully but throws exceptions at runtime

import java.util.*;

public class tc_20_java_runtime_error {

    // RUNTIME ERROR 1: NullPointerException
    static String processName(String name) {
        // name could be null — calling .length() on null throws NPE
        return name.toUpperCase() + " (" + name.length() + " chars)";
    }

    // RUNTIME ERROR 2: ArrayIndexOutOfBoundsException
    static int getElement(int[] arr, int index) {
        return arr[index];   // no bounds check — throws if index >= arr.length
    }

    // RUNTIME ERROR 3: ClassCastException
    @SuppressWarnings("unchecked")
    static void castDemo() {
        Object obj = "Hello World";
        Integer num = (Integer) obj;   // String cannot be cast to Integer
        System.out.println(num);
    }

    // RUNTIME ERROR 4: StackOverflowError
    static int factorial(int n) {
        return n * factorial(n - 1);   // No base case — infinite recursion
    }

    // RUNTIME ERROR 5: NumberFormatException
    static int parseInput(String s) {
        return Integer.parseInt(s);    // throws if s is not a valid integer
    }

    public static void main(String[] args) {
        // Test 1: NullPointerException
        System.out.println(processName("Alice"));   // OK
        System.out.println(processName(null));      // NullPointerException!

        // Test 2: ArrayIndexOutOfBoundsException
        int[] scores = {85, 92, 78};
        System.out.println(getElement(scores, 1));   // OK: returns 92
        System.out.println(getElement(scores, 10));  // throws ArrayIndexOutOfBoundsException!

        // Test 3: ClassCastException
        castDemo();

        // Test 4: NumberFormatException
        System.out.println(parseInput("42"));        // OK
        System.out.println(parseInput("not_a_num")); // throws NumberFormatException!
    }


    // ==========================================================================
    // ENTERPRISE SERVICE SUBSYSTEM ARCHITECTURE: TC_20_JAVA_RUNTIME_ERROR
    // ==========================================================================

    public static class SubsystemEngine_1 {
        private String engineId = "tc_20_java_runtime_error_engine_1";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_1() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_2 {
        private String engineId = "tc_20_java_runtime_error_engine_2";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_2() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_3 {
        private String engineId = "tc_20_java_runtime_error_engine_3";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_3() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_4 {
        private String engineId = "tc_20_java_runtime_error_engine_4";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_4() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_5 {
        private String engineId = "tc_20_java_runtime_error_engine_5";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_5() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_6 {
        private String engineId = "tc_20_java_runtime_error_engine_6";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_6() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_7 {
        private String engineId = "tc_20_java_runtime_error_engine_7";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_7() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_8 {
        private String engineId = "tc_20_java_runtime_error_engine_8";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_8() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_9 {
        private String engineId = "tc_20_java_runtime_error_engine_9";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_9() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_10 {
        private String engineId = "tc_20_java_runtime_error_engine_10";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_10() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_11 {
        private String engineId = "tc_20_java_runtime_error_engine_11";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_11() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_12 {
        private String engineId = "tc_20_java_runtime_error_engine_12";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_12() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_13 {
        private String engineId = "tc_20_java_runtime_error_engine_13";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_13() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_14 {
        private String engineId = "tc_20_java_runtime_error_engine_14";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_14() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_15 {
        private String engineId = "tc_20_java_runtime_error_engine_15";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_15() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_16 {
        private String engineId = "tc_20_java_runtime_error_engine_16";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_16() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_17 {
        private String engineId = "tc_20_java_runtime_error_engine_17";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_17() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_18 {
        private String engineId = "tc_20_java_runtime_error_engine_18";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_18() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_19 {
        private String engineId = "tc_20_java_runtime_error_engine_19";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_19() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_20 {
        private String engineId = "tc_20_java_runtime_error_engine_20";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_20() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_21 {
        private String engineId = "tc_20_java_runtime_error_engine_21";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_21() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_22 {
        private String engineId = "tc_20_java_runtime_error_engine_22";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_22() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_23 {
        private String engineId = "tc_20_java_runtime_error_engine_23";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_23() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_24 {
        private String engineId = "tc_20_java_runtime_error_engine_24";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_24() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_25 {
        private String engineId = "tc_20_java_runtime_error_engine_25";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_25() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_26 {
        private String engineId = "tc_20_java_runtime_error_engine_26";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_26() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_27 {
        private String engineId = "tc_20_java_runtime_error_engine_27";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_27() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_28 {
        private String engineId = "tc_20_java_runtime_error_engine_28";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_28() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_29 {
        private String engineId = "tc_20_java_runtime_error_engine_29";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_29() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_30 {
        private String engineId = "tc_20_java_runtime_error_engine_30";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_30() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_31 {
        private String engineId = "tc_20_java_runtime_error_engine_31";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_31() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_32 {
        private String engineId = "tc_20_java_runtime_error_engine_32";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_32() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_33 {
        private String engineId = "tc_20_java_runtime_error_engine_33";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_33() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
            }
        }

        public int getRegistryCount() {
            return registry.size();
        }

        public double computeMetricChecksum() {
            double sum = 0.0;
            for (String k : registry.keySet()) {
                sum += k.length() * 1.5;
            }
            return sum;
        }
    }

    public static class SubsystemEngine_34 {
        private String engineId = "tc_20_java_runtime_error_engine_34";
        private int maxPoolSize = 64;
}

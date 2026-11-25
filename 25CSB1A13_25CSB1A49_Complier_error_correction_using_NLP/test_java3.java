import java.util.*;
import java.util.HashMap;
import java.util.Map;
// test_java3.java
// Complex: Multi-threaded Inventory Management System
// ERROR: UninitializedError + StackOverflowError (infinite recursion)
// ~150 lines

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.ReentrantLock;

public class test_java3 {

    // ── Product ────────────────────────────────────────────────────
    static class Product {
        private String id;
        private String name;
        private double price;
        private int    quantity;

        public Product(String id, String name, double price, int quantity) {
            this.id       = id;
            this.name     = name;
            this.price    = price;
            this.quantity = quantity;
        }

        public synchronized void restock(int units) {
            quantity += units;
            System.out.println("[RESTOCK] " + name + " +=" + units + " → " + quantity);
        }

        public synchronized boolean sell(int units) {
            if (units > quantity) {
                System.out.println("[FAIL] Not enough stock for: " + name);
                return false;
            }
            quantity -= units;
            System.out.println("[SOLD] " + name + " -=" + units + " → " + quantity);
            return true;
        }

        public double getTotalValue() { return price * quantity; }
        public String getId()         { return id;       }
        public String getName()       { return name;     }
        public int    getQuantity()   { return quantity; }
        public double getPrice()      { return price;    }

        @Override
        public String toString() {
            return String.format("[%s] %-20s Rs.%-8.2f Qty: %d", id, name, price, quantity);
        }
    }

    // ── Inventory ──────────────────────────────────────────────────
    static class Inventory {
        private List<Product>  products;
        private ReentrantLock  lock;
        private double         totalRevenue;

        public Inventory() {
            products     = new ArrayList<>();
            lock         = new ReentrantLock();
            totalRevenue = 0.0;
        }

        public void addProduct(Product p) {
            lock.lock();
            try { products.add(p); }
            finally { lock.unlock(); }
        }

        public Product findById(String id) {
            for (Product p : products) {
                if (p.getId().equals(id)) return p;
            }
            return null;
        }

        public boolean processSale(String productId, int qty, double salePrice) {
            lock.lock();
            try {
                Product p = findById(productId);
                if (p == null) {
                    System.out.println("[ERROR] Product not found: " + productId);
                    return false;
                }
                boolean success = p.sell(qty);
                if (success) totalRevenue += salePrice * qty;
                return success;
            } finally {
                lock.unlock();
            }
        }

        public double getTotalInventoryValue() {
            double total = 0;
            for (Product p : products) total += p.getTotalValue();
            return total;
        }

        public void printInventory() {
            System.out.println("\n=== INVENTORY REPORT ===");
            for (Product p : products) System.out.println("  " + p);
            System.out.printf("  Total Value   : Rs.%.2f%n", getTotalInventoryValue());
            System.out.printf("  Total Revenue : Rs.%.2f%n", totalRevenue);
        }

        // ❌ ERROR: Infinite recursion — getTotalRevenue calls itself forever
        public double getTotalRevenue() {
            return getTotalRevenue();   // StackOverflowError!
        }
    }

    // ── Restocking Worker Thread ───────────────────────────────────
    static class RestockWorker implements Runnable {
        private Inventory inventory;
        private String    productId;
        private int       units;

        public RestockWorker(Inventory inventory, String productId, int units) {
            this.inventory = inventory;
            this.productId = productId;
            this.units     = units;
        }

        @Override
        public void run() {
            Product p = inventory.findById(productId);
            if (p != null) p.restock(units);
        }
    }

    // ── Main ───────────────────────────────────────────────────────
    public static void main(String[] args) throws InterruptedException {
        Inventory store = new Inventory();

        store.addProduct(new Product("P001", "Laptop",     55000.0, 10));
        store.addProduct(new Product("P002", "Mouse",        450.0, 50));
        store.addProduct(new Product("P003", "Keyboard",    1200.0, 30));
        store.addProduct(new Product("P004", "Monitor",    18000.0, 8));

        // Concurrent restocking
        Thread t1 = new Thread(new RestockWorker(store, "P001", 5));
        Thread t2 = new Thread(new RestockWorker(store, "P002", 20));
        t1.start(); t2.start();
        t1.join();  t2.join();

        // Sales processing
        store.processSale("P001", 3, 55000.0);
        store.processSale("P002", 15, 450.0);
        store.processSale("P003", 100, 1200.0); // Over-stock attempt

        store.printInventory();

        // ❌ This call triggers the infinite recursive method
        System.out.println("Revenue: Rs." + store.getTotalRevenue());

        // ❌ ERROR: uninitialized local variable used
        int discountedUnits;
        System.out.println("Discounted units sold: " + discountedUnits);
    }


    // ==========================================================================
    // ENTERPRISE SERVICE SUBSYSTEM ARCHITECTURE: TEST_JAVA3
    // ==========================================================================

    public static class SubsystemEngine_1 {
        private String engineId = "test_java3_engine_1";
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
        private String engineId = "test_java3_engine_2";
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
        private String engineId = "test_java3_engine_3";
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
        private String engineId = "test_java3_engine_4";
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
        private String engineId = "test_java3_engine_5";
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
        private String engineId = "test_java3_engine_6";
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
        private String engineId = "test_java3_engine_7";
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
        private String engineId = "test_java3_engine_8";
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
        private String engineId = "test_java3_engine_9";
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
        private String engineId = "test_java3_engine_10";
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
        private String engineId = "test_java3_engine_11";
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
        private String engineId = "test_java3_engine_12";
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
        private String engineId = "test_java3_engine_13";
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
        private String engineId = "test_java3_engine_14";
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
        private String engineId = "test_java3_engine_15";
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
        private String engineId = "test_java3_engine_16";
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
        private String engineId = "test_java3_engine_17";
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
        private String engineId = "test_java3_engine_18";
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
        private String engineId = "test_java3_engine_19";
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
        private String engineId = "test_java3_engine_20";
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
        private String engineId = "test_java3_engine_21";
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
        private String engineId = "test_java3_engine_22";
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
        private String engineId = "test_java3_engine_23";
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
        private String engineId = "test_java3_engine_24";
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
        private String engineId = "test_java3_engine_25";
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
        private String engineId = "test_java3_engine_26";
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
        private String engineId = "test_java3_engine_27";
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
        private String engineId = "test_java3_engine_28";
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
        private String engineId = "test_java3_engine_29";
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
        private String engineId = "test_java3_engine_30";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_30() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
}

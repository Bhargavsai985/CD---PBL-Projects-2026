import java.util.*;
import java.util.HashMap;
import java.util.Map;
// test_java4.java
// Complex: Hospital Patient Record System with Inheritance & Interfaces
// ERROR: NullPointerException — calling method on uninitialized object
//        ClassCastException  — wrong polymorphic cast
// ~160 lines

import java.util.ArrayList;
import java.util.List;

public class test_java4 {

    // ── Interface ──────────────────────────────────────────────────
    interface Billable {
        double calculateBill();
        void   printBill();
    }

    // ── Base: Patient ──────────────────────────────────────────────
    static abstract class Patient implements Billable {
        protected String patientId;
        protected String name;
        protected int    age;
        protected String diagnosis;
        protected List<String> medications;

        public Patient(String patientId, String name, int age) {
            this.patientId   = patientId;
            this.name        = name;
            this.age         = age;
            this.medications = new ArrayList<>();
        }

        public void addMedication(String med) { medications.add(med); }
        public String getName()               { return name;      }
        public String getPatientId()          { return patientId; }
        public void   setDiagnosis(String d)  { this.diagnosis = d; }

        public void printProfile() {
            System.out.println("\n--- Patient Profile ---");
            System.out.println("ID        : " + patientId);
            System.out.println("Name      : " + name + "  |  Age: " + age);
            System.out.println("Diagnosis : " + diagnosis);
            System.out.println("Medications: " + medications);
        }
    }

    // ── InPatient ─────────────────────────────────────────────────
    static class InPatient extends Patient {
        private int    daysAdmitted;
        private double dailyRoomCharge;
        private double surgeryCharge;

        public InPatient(String id, String name, int age,
                         int days, double roomCharge, double surgeryCharge) {
            super(id, name, age);
            this.daysAdmitted   = days;
            this.dailyRoomCharge = roomCharge;
            this.surgeryCharge   = surgeryCharge;
        }

        @Override
        public double calculateBill() {
            return (daysAdmitted * dailyRoomCharge) + surgeryCharge + (medications.size() * 250.0);
        }

        @Override
        public void printBill() {
            System.out.printf("%-20s Room: Rs.%-8.2f Surgery: Rs.%-8.2f TOTAL: Rs.%.2f%n",
                name,
                daysAdmitted * dailyRoomCharge,
                surgeryCharge,
                calculateBill());
        }
    }

    // ── OutPatient ────────────────────────────────────────────────
    static class OutPatient extends Patient {
        private double consultationFee;
        private int    labTests;

        public OutPatient(String id, String name, int age,
                          double fee, int tests) {
            super(id, name, age);
            this.consultationFee = fee;
            this.labTests        = tests;
        }

        @Override
        public double calculateBill() {
            return consultationFee + (labTests * 500.0) + (medications.size() * 150.0);
        }

        @Override
        public void printBill() {
            System.out.printf("%-20s Consult: Rs.%-6.2f Labs: %d  TOTAL: Rs.%.2f%n",
                name, consultationFee, labTests, calculateBill());
        }
    }

    // ── Hospital ──────────────────────────────────────────────────
    static class Hospital {
        private String        name;
        private List<Patient> patients;

        public Hospital(String name) {
            this.name     = name;
            this.patients = new ArrayList<>();
        }

        public void admit(Patient p)   { patients.add(p); }

        public double getTotalRevenue() {
            double total = 0;
            for (Patient p : patients) total += p.calculateBill();
            return total;
        }

        public void printAllBills() {
            System.out.println("\n=== " + name + " — Billing Summary ===");
            for (Patient p : patients) p.printBill();
            System.out.printf("TOTAL REVENUE: Rs.%.2f%n", getTotalRevenue());
        }
    }

    // ── Main ───────────────────────────────────────────────────────
    public static void main(String[] args) {
        Hospital aiims = new Hospital("AIIMS City Hospital");

        InPatient  p1 = new InPatient ("P001","Priya Sharma",  34, 7, 3500, 45000);
        OutPatient p2 = new OutPatient("P002","Ravi Kumar",    52, 800, 4);
        InPatient  p3 = new InPatient ("P003","Meena Devi",    28, 3, 2500, 0);

        p1.setDiagnosis("Appendectomy");
        p1.addMedication("Amoxicillin");
        p1.addMedication("Pantoprazole");

        p2.setDiagnosis("Hypertension follow-up");
        p2.addMedication("Amlodipine");

        p3.setDiagnosis("Fracture — right arm");
        p3.addMedication("Ibuprofen");
        p3.addMedication("Calcium Carbonate");

        aiims.admit(p1);
        aiims.admit(p2);
        aiims.admit(p3);

        p1.printProfile();
        p2.printProfile();
        aiims.printAllBills();

        // ❌ ERROR 1: NullPointerException — patient4 never initialized
        Patient patient4 = null;
        patient4.setDiagnosis("Diabetes");     // NullPointerException!

        // ❌ ERROR 2: ClassCastException — OutPatient cast to InPatient
        Patient generic = aiims.patients.get(1);    // this is OutPatient
        InPatient wrongCast = (InPatient) generic;  // ClassCastException!
        System.out.println(wrongCast.calculateBill());
    }


    // ==========================================================================
    // ENTERPRISE SERVICE SUBSYSTEM ARCHITECTURE: TEST_JAVA4
    // ==========================================================================

    public static class SubsystemEngine_1 {
        private String engineId = "test_java4_engine_1";
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
        private String engineId = "test_java4_engine_2";
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
        private String engineId = "test_java4_engine_3";
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
        private String engineId = "test_java4_engine_4";
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
        private String engineId = "test_java4_engine_5";
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
        private String engineId = "test_java4_engine_6";
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
        private String engineId = "test_java4_engine_7";
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
        private String engineId = "test_java4_engine_8";
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
        private String engineId = "test_java4_engine_9";
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
        private String engineId = "test_java4_engine_10";
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
        private String engineId = "test_java4_engine_11";
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
        private String engineId = "test_java4_engine_12";
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
        private String engineId = "test_java4_engine_13";
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
        private String engineId = "test_java4_engine_14";
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
        private String engineId = "test_java4_engine_15";
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
        private String engineId = "test_java4_engine_16";
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
        private String engineId = "test_java4_engine_17";
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
        private String engineId = "test_java4_engine_18";
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
        private String engineId = "test_java4_engine_19";
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
        private String engineId = "test_java4_engine_20";
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
        private String engineId = "test_java4_engine_21";
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
        private String engineId = "test_java4_engine_22";
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
        private String engineId = "test_java4_engine_23";
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
        private String engineId = "test_java4_engine_24";
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
        private String engineId = "test_java4_engine_25";
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
        private String engineId = "test_java4_engine_26";
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
        private String engineId = "test_java4_engine_27";
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
        private String engineId = "test_java4_engine_28";
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
        private String engineId = "test_java4_engine_29";
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
        private String engineId = "test_java4_engine_30";
        private int maxPoolSize = 64;
        private Map<String, Object> registry = new HashMap<>();

        public SubsystemEngine_30() {}

        public String getEngineId() { return this.engineId; }
        public int getMaxPoolSize() { return this.maxPoolSize; }

        public void recordEntry(String key, Object val) {
            if (key != null && registry.size() < maxPoolSize) {
                registry.put(key, val);
}

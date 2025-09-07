package com.hse.li.swarm.ioh;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Analyzer logger - corresponds to ioh.logger.Analyzer in Python
 * Strictly follows Python implementation:
 * logger = ioh.logger.Analyzer(root=f"{DATA_FOLDER}/Baselines/", folder_name=f"{algname}_F{fid}_I{iid}_{dim}D", algorithm_name=f"{algname}")
 * func.attach_logger(logger)
 * logger.close()
 * 
 * Implements IOH standard logging format
 */
public class AnalyzerLogger implements IOHLogger {
    private static final Logger logger = LoggerFactory.getLogger(AnalyzerLogger.class);
    
    private final String rootPath;
    private final String folderName;
    private final String algorithmName;
    private final List<EvaluationRecord> records;
    private final Path outputDir;
    
    public AnalyzerLogger(String rootPath, String folderName, String algorithmName) {
        this.rootPath = rootPath;
        this.folderName = folderName;
        this.algorithmName = algorithmName;
        this.records = new ArrayList<>();
        
        // Create output directory - corresponds to Python implementation
        this.outputDir = Paths.get(rootPath, folderName);
        try {
            Files.createDirectories(outputDir);
            logger.info("Created output directory: {}", outputDir);
        } catch (IOException e) {
            logger.error("Failed to create output directory: {}", e.getMessage());
        }
    }
    
    @Override
    public void logEvaluation(int evaluation, double fitness, double[] solution) {
        EvaluationRecord record = new EvaluationRecord(
            evaluation, fitness, solution.clone(), algorithmName, 
            getFunctionId(), getInstance(), getDimension()
        );
        records.add(record);
        logger.debug("Logged evaluation: Eval={}, Fitness={}", evaluation, fitness);
    }
    
    @Override
    public void close() {
        try {
            saveToCSV();
            saveToJSON();
            logger.info("Results saved to: {}/{}", outputDir.getParent().getFileName(), folderName);
        } catch (IOException e) {
            logger.error("Failed to save results: {}", e.getMessage(), e);
        }
    }
    
    @Override
    public void reset() {
        records.clear();
        logger.debug("Reset logger");
    }
    
    /**
     * Save to CSV format - corresponds to IOH standard format
     */
    private void saveToCSV() throws IOException {
        String csvFileName = outputDir.resolve(
            String.format("IOHprofiler_f%d_%s.csv", getFunctionId(), getFunctionName())
        ).toString();
        
        try (FileWriter fileWriter = new FileWriter(csvFileName);
             org.apache.commons.csv.CSVPrinter csvPrinter = new org.apache.commons.csv.CSVPrinter(
                 fileWriter, org.apache.commons.csv.CSVFormat.DEFAULT)) {
            
            csvPrinter.printRecord("evaluation", "fitness", "solution");
            for (EvaluationRecord record : records) {
                csvPrinter.printRecord(
                    record.getEvaluation(),
                    record.getFitness(),
                    arrayToString(record.getSolution())
                );
            }
            csvPrinter.flush();
        }
    }
    
    /**
     * Save to JSON format - corresponds to IOH standard format
     */
    private void saveToJSON() throws IOException {
        String jsonFileName = outputDir.resolve(
            String.format("IOHprofiler_f%d_%s.json", getFunctionId(), getFunctionName())
        ).toString();
        
        Files.writeString(Paths.get(jsonFileName), generateJSONConfig());
    }
    
    /**
     * Generate JSON configuration - corresponds to IOH standard format
     */
    private String generateJSONConfig() {
        return String.format("{%n" +
            "    \"problem\": {%n" +
            "        \"function\": %d,%n" +
            "        \"name\": \"%s\",%n" +
            "        \"dimension\": %d,%n" +
            "        \"instance\": %d%n" +
            "    },%n" +
            "    \"algorithm\": {%n" +
            "        \"name\": \"%s\"%n" +
            "    },%n" +
            "    \"data\": {%n" +
            "        \"evaluations\": %d,%n" +
            "        \"best_fitness\": %.15e%n" +
            "    }%n" +
            "}",
            getFunctionId(), getFunctionName(), getDimension(), getInstance(),
            algorithmName, records.size(), getBestFitness()
        );
    }
    
    /**
     * Convert array to string
     */
    private String arrayToString(double[] array) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < array.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(array[i]);
        }
        sb.append("]");
        return sb.toString();
    }
    
    /**
     * Parse function ID from folder name - corresponds to Python implementation
     */
    private int getFunctionId() {
        String[] parts = folderName.split("_");
        for (String part : parts) {
            if (part.startsWith("F")) {
                return Integer.parseInt(part.substring(1));
            }
        }
        return 0;
    }
    
    /**
     * Get function name - corresponds to BBOB function names
     */
    private String getFunctionName() {
        int fid = getFunctionId();
        switch (fid) {
            case 20: return "Schwefel";
            case 21: return "Gallagher101";
            case 22: return "Gallagher21";
            case 23: return "Katsuura";
            case 24: return "LunacekBiRastrigin";
            default: return "Unknown";
        }
    }
    
    /**
     * Parse instance ID from folder name - corresponds to Python implementation
     */
    private int getInstance() {
        String[] parts = folderName.split("_");
        for (String part : parts) {
            if (part.startsWith("I")) {
                return Integer.parseInt(part.substring(1));
            }
        }
        return 0;
    }
    
    /**
     * Parse dimension from folder name - corresponds to Python implementation
     */
    private int getDimension() {
        String[] parts = folderName.split("_");
        for (String part : parts) {
            if (part.endsWith("D")) {
                return Integer.parseInt(part.substring(0, part.length() - 1));
            }
        }
        return 0;
    }
    
    /**
     * Get best fitness
     */
    private double getBestFitness() {
        return records.stream()
            .mapToDouble(EvaluationRecord::getFitness)
            .min()
            .orElse(Double.MAX_VALUE);
    }
    
    /**
     * Monitor algorithm attributes - corresponds to watch() method in Python
     */
    @Override
    public void watch(Object algorithm, String... attributes) {
        logger.debug("Monitoring algorithm attributes: {}", java.util.Arrays.toString(attributes));
        // Attribute monitoring logic can be implemented here
    }
    
    /**
     * Add run attributes - corresponds to addRunAttributes() method in Python
     */
    @Override
    public void addRunAttributes(Object algorithm, String... attributes) {
        logger.debug("Adding run attributes: {}", java.util.Arrays.toString(attributes));
        // Run attribute addition logic can be implemented here
    }
    
    /**
     * Set experiment attributes - corresponds to setExperimentAttributes() method in Python
     */
    @Override
    public void setExperimentAttributes(java.util.Map<String, String> attributes) {
        logger.debug("Setting experiment attributes: {}", attributes);
        // Experiment attribute setting logic can be implemented here
    }
    
    /**
     * Evaluation record inner class - corresponds to IOH evaluation records
     */
    private static class EvaluationRecord {
        private final int evaluation;
        private final double fitness;
        private final double[] solution;
        private final String algorithmName;
        private final int functionId;
        private final int instanceId;
        private final int dimension;
        
        public EvaluationRecord(int evaluation, double fitness, double[] solution, 
                              String algorithmName, int functionId, int instanceId, int dimension) {
            this.evaluation = evaluation;
            this.fitness = fitness;
            this.solution = solution;
            this.algorithmName = algorithmName;
            this.functionId = functionId;
            this.instanceId = instanceId;
            this.dimension = dimension;
        }
        
        public int getEvaluation() { return evaluation; }
        public double getFitness() { return fitness; }
        public double[] getSolution() { return solution; }
        public String getAlgorithmName() { return algorithmName; }
        public int getFunctionId() { return functionId; }
        public int getInstanceId() { return instanceId; }
        public int getDimension() { return dimension; }
    }
}
package com.swarm.benchmark;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Logger for recording optimization progress.
 * This corresponds to the IOH logger.Analyzer class.
 */
public class IOHLogger {
    private static final Logger logger = LogManager.getLogger(IOHLogger.class);
    
    private final String rootFolder;
    private final String folderName;
    private final String algorithmName;
    private final List<LogEntry> entries;
    private final Path logDir;
    private final Path datFile;
    
    public IOHLogger(String rootFolder, String folderName, String algorithmName) {
        this.rootFolder = rootFolder;
        this.folderName = folderName;
        this.algorithmName = algorithmName;
        this.entries = new ArrayList<>();
        
        // Create directory structure
        this.logDir = Paths.get(rootFolder, folderName);
        try {
            Files.createDirectories(logDir);
        } catch (IOException e) {
            logger.error("Failed to create log directory: " + logDir, e);
        }
        
        this.datFile = logDir.resolve("IOHprofiler_f1_i1.dat");
    }
    
    /**
     * Logs a function evaluation.
     * 
     * @param solution the solution vector
     * @param fitness the fitness value
     * @param evaluations the number of evaluations so far
     */
    public void logEvaluation(double[] solution, double fitness, int evaluations) {
        entries.add(new LogEntry(solution, fitness, evaluations));
    }
    
    /**
     * Closes the logger and writes the data file.
     */
    public void close() {
        try (BufferedWriter writer = Files.newBufferedWriter(datFile)) {
            // Write header
            writer.write("function evaluation functionvalue\n");
            
            // Write data entries
            for (LogEntry entry : entries) {
                writer.write(String.format("%d %d %.15e\n", 
                    entry.evaluations, entry.evaluations, entry.fitness));
            }
            
            logger.info("Log file written to: " + datFile);
        } catch (IOException e) {
            logger.error("Failed to write log file: " + datFile, e);
        }
    }
    
    /**
     * Gets the log directory path.
     */
    public String getLogDir() {
        return logDir.toString();
    }
    
    /**
     * Log entry containing evaluation data.
     */
    private static class LogEntry {
        final double[] solution;
        final double fitness;
        final int evaluations;
        
        LogEntry(double[] solution, double fitness, int evaluations) {
            this.solution = solution.clone();
            this.fitness = fitness;
            this.evaluations = evaluations;
        }
    }
}

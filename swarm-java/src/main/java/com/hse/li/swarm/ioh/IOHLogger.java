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
 * IOH日志接口 - 对应env_win11环境中的ioh.logger.Analyzer
 * 严格按照env_win11环境中的Analyzer类实现
 */
public interface IOHLogger {
    void logEvaluation(int evaluation, double fitness, double[] solution);
    void close();
    void reset();
    void watch(Object algorithm, String... attributes);
    void addRunAttributes(Object algorithm, String... attributes);
    void setExperimentAttributes(java.util.Map<String, String> attributes);
}




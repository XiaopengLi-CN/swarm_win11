package com.swarm.benchmark;

/**
 * Metadata about an objective function.
 * This corresponds to the IOH problem metadata.
 */
public class FunctionMetadata {
    private final int nVariables;
    private final int functionId;
    private final int instanceId;
    private final String name;
    
    public FunctionMetadata(int nVariables, int functionId, int instanceId, String name) {
        this.nVariables = nVariables;
        this.functionId = functionId;
        this.instanceId = instanceId;
        this.name = name;
    }
    
    public int getNVariables() {
        return nVariables;
    }
    
    public int getFunctionId() {
        return functionId;
    }
    
    public int getInstanceId() {
        return instanceId;
    }
    
    public String getName() {
        return name;
    }
}

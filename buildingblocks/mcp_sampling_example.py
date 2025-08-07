"""
MCP Sampling Example

This example demonstrates how to work with MCP sampling including different
sampling strategies, parameters, validation, and management.

Requirements:
- pip install mcp
"""

import asyncio
import json
import random
import numpy as np
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    SamplingParameters,
    SamplingStrategy,
    SamplingResult,
    SamplingValidation
)


# ============================================================================
# Sampling Management
# ============================================================================

class SamplingManager:
    """Manages different types of sampling strategies and techniques."""
    
    def __init__(self):
        self.sampling_strategies = {}
        self.sampling_parameters = {}
        self.sampling_results = {}
        self.setup_sample_strategies()
        
    def setup_sample_strategies(self):
        """Set up sample sampling strategies for demonstration."""
        # Random sampling
        self.sampling_strategies["random"] = {
            "type": "random",
            "description": "Simple random sampling",
            "parameters": ["sample_size", "population_size"],
            "validation": {
                "required": ["sample_size", "population_size"],
                "constraints": {
                    "sample_size": "positive_integer",
                    "population_size": "positive_integer"
                }
            }
        }
        
        # Stratified sampling
        self.sampling_strategies["stratified"] = {
            "type": "stratified",
            "description": "Stratified sampling with proportional allocation",
            "parameters": ["strata", "sample_size", "population_size"],
            "validation": {
                "required": ["strata", "sample_size", "population_size"],
                "constraints": {
                    "sample_size": "positive_integer",
                    "population_size": "positive_integer",
                    "strata": "dict_with_positive_values"
                }
            }
        }
        
        # Systematic sampling
        self.sampling_strategies["systematic"] = {
            "type": "systematic",
            "description": "Systematic sampling with fixed interval",
            "parameters": ["interval", "population_size", "start_index"],
            "validation": {
                "required": ["interval", "population_size"],
                "constraints": {
                    "interval": "positive_integer",
                    "population_size": "positive_integer",
                    "start_index": "non_negative_integer"
                }
            }
        }
        
        # Cluster sampling
        self.sampling_strategies["cluster"] = {
            "type": "cluster",
            "description": "Cluster sampling with random cluster selection",
            "parameters": ["clusters", "clusters_to_select", "population_size"],
            "validation": {
                "required": ["clusters", "clusters_to_select", "population_size"],
                "constraints": {
                    "clusters": "list_of_positive_integers",
                    "clusters_to_select": "positive_integer",
                    "population_size": "positive_integer"
                }
            }
        }
        
        # Adaptive sampling
        self.sampling_strategies["adaptive"] = {
            "type": "adaptive",
            "description": "Adaptive sampling based on criteria",
            "parameters": ["criteria", "max_samples", "threshold"],
            "validation": {
                "required": ["criteria", "max_samples"],
                "constraints": {
                    "max_samples": "positive_integer",
                    "threshold": "float_between_0_and_1"
                }
            }
        }
        
        # Monte Carlo sampling
        self.sampling_strategies["monte_carlo"] = {
            "type": "monte_carlo",
            "description": "Monte Carlo simulation sampling",
            "parameters": ["iterations", "distribution", "parameters"],
            "validation": {
                "required": ["iterations", "distribution"],
                "constraints": {
                    "iterations": "positive_integer",
                    "distribution": "valid_distribution"
                }
            }
        }
        
        # Bootstrap sampling
        self.sampling_strategies["bootstrap"] = {
            "type": "bootstrap",
            "description": "Bootstrap resampling technique",
            "parameters": ["data", "bootstrap_samples", "sample_size"],
            "validation": {
                "required": ["data", "bootstrap_samples"],
                "constraints": {
                    "bootstrap_samples": "positive_integer",
                    "sample_size": "positive_integer"
                }
            }
        }
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get a sampling strategy by ID."""
        return self.sampling_strategies.get(strategy_id)
    
    def list_strategies(self, strategy_type: str = None) -> List[Dict[str, Any]]:
        """List available sampling strategies."""
        results = []
        
        for strategy_id, strategy in self.sampling_strategies.items():
            if strategy_type and strategy.get("type") != strategy_type:
                continue
            
            results.append({
                "id": strategy_id,
                "type": strategy["type"],
                "description": strategy["description"],
                "parameters": strategy["parameters"],
                "validation": strategy.get("validation", {})
            })
        
        return results
    
    def validate_parameters(self, strategy_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate sampling parameters for a strategy."""
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            return {"valid": False, "error": "Strategy not found"}
        
        validation_rules = strategy.get("validation", {})
        required_params = validation_rules.get("required", [])
        constraints = validation_rules.get("constraints", {})
        
        # Check required parameters
        missing_params = [param for param in required_params if param not in parameters]
        if missing_params:
            return {
                "valid": False,
                "error": f"Missing required parameters: {missing_params}",
                "missing_parameters": missing_params
            }
        
        # Check parameter constraints
        for param_name, constraint in constraints.items():
            if param_name in parameters:
                param_value = parameters[param_name]
                
                if constraint == "positive_integer":
                    if not isinstance(param_value, int) or param_value <= 0:
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a positive integer",
                            "invalid_parameter": param_name,
                            "expected": "positive_integer"
                        }
                
                elif constraint == "non_negative_integer":
                    if not isinstance(param_value, int) or param_value < 0:
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a non-negative integer",
                            "invalid_parameter": param_name,
                            "expected": "non_negative_integer"
                        }
                
                elif constraint == "float_between_0_and_1":
                    if not isinstance(param_value, (int, float)) or param_value < 0 or param_value > 1:
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a float between 0 and 1",
                            "invalid_parameter": param_name,
                            "expected": "float_between_0_and_1"
                        }
                
                elif constraint == "dict_with_positive_values":
                    if not isinstance(param_value, dict):
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a dictionary",
                            "invalid_parameter": param_name,
                            "expected": "dict_with_positive_values"
                        }
                    for key, value in param_value.items():
                        if not isinstance(value, (int, float)) or value <= 0:
                            return {
                                "valid": False,
                                "error": f"Parameter {param_name} must have positive values",
                                "invalid_parameter": param_name,
                                "expected": "dict_with_positive_values"
                            }
                
                elif constraint == "list_of_positive_integers":
                    if not isinstance(param_value, list):
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a list",
                            "invalid_parameter": param_name,
                            "expected": "list_of_positive_integers"
                        }
                    for value in param_value:
                        if not isinstance(value, int) or value <= 0:
                            return {
                                "valid": False,
                                "error": f"Parameter {param_name} must contain positive integers",
                                "invalid_parameter": param_name,
                                "expected": "list_of_positive_integers"
                            }
        
        return {"valid": True}
    
    def execute_sampling(self, strategy_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sampling with the specified strategy and parameters."""
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            return {"status": "error", "message": "Strategy not found"}
        
        # Validate parameters
        validation = self.validate_parameters(strategy_id, parameters)
        if not validation["valid"]:
            return {"status": "error", "validation": validation}
        
        try:
            if strategy_id == "random":
                return self._execute_random_sampling(parameters)
            elif strategy_id == "stratified":
                return self._execute_stratified_sampling(parameters)
            elif strategy_id == "systematic":
                return self._execute_systematic_sampling(parameters)
            elif strategy_id == "cluster":
                return self._execute_cluster_sampling(parameters)
            elif strategy_id == "adaptive":
                return self._execute_adaptive_sampling(parameters)
            elif strategy_id == "monte_carlo":
                return self._execute_monte_carlo_sampling(parameters)
            elif strategy_id == "bootstrap":
                return self._execute_bootstrap_sampling(parameters)
            else:
                return {"status": "error", "message": "Unknown strategy"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _execute_random_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute random sampling."""
        sample_size = parameters["sample_size"]
        population_size = parameters["population_size"]
        
        # Generate random sample indices
        sample_indices = random.sample(range(population_size), min(sample_size, population_size))
        sample_indices.sort()
        
        return {
            "status": "success",
            "strategy": "random",
            "sample_size": len(sample_indices),
            "population_size": population_size,
            "sample_indices": sample_indices,
            "sampling_fraction": len(sample_indices) / population_size
        }
    
    def _execute_stratified_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute stratified sampling."""
        strata = parameters["strata"]
        sample_size = parameters["sample_size"]
        population_size = parameters["population_size"]
        
        # Calculate proportional allocation
        total_strata_size = sum(strata.values())
        sample_allocation = {}
        sample_indices = []
        
        for stratum_name, stratum_size in strata.items():
            stratum_proportion = stratum_size / total_strata_size
            stratum_sample_size = int(sample_size * stratum_proportion)
            
            # Generate random sample for this stratum
            stratum_indices = random.sample(range(stratum_size), min(stratum_sample_size, stratum_size))
            sample_allocation[stratum_name] = stratum_indices
            sample_indices.extend(stratum_indices)
        
        return {
            "status": "success",
            "strategy": "stratified",
            "sample_size": len(sample_indices),
            "population_size": population_size,
            "strata_allocation": sample_allocation,
            "sample_indices": sample_indices,
            "sampling_fraction": len(sample_indices) / population_size
        }
    
    def _execute_systematic_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute systematic sampling."""
        interval = parameters["interval"]
        population_size = parameters["population_size"]
        start_index = parameters.get("start_index", 0)
        
        # Generate systematic sample indices
        sample_indices = []
        current_index = start_index
        
        while current_index < population_size:
            sample_indices.append(current_index)
            current_index += interval
        
        return {
            "status": "success",
            "strategy": "systematic",
            "sample_size": len(sample_indices),
            "population_size": population_size,
            "interval": interval,
            "start_index": start_index,
            "sample_indices": sample_indices,
            "sampling_fraction": len(sample_indices) / population_size
        }
    
    def _execute_cluster_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute cluster sampling."""
        clusters = parameters["clusters"]
        clusters_to_select = parameters["clusters_to_select"]
        population_size = parameters["population_size"]
        
        # Randomly select clusters
        selected_clusters = random.sample(range(len(clusters)), min(clusters_to_select, len(clusters)))
        
        # Get all elements from selected clusters
        sample_indices = []
        for cluster_idx in selected_clusters:
            cluster_size = clusters[cluster_idx]
            sample_indices.extend(range(cluster_size))
        
        return {
            "status": "success",
            "strategy": "cluster",
            "sample_size": len(sample_indices),
            "population_size": population_size,
            "selected_clusters": selected_clusters,
            "sample_indices": sample_indices,
            "sampling_fraction": len(sample_indices) / population_size
        }
    
    def _execute_adaptive_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adaptive sampling."""
        criteria = parameters["criteria"]
        max_samples = parameters["max_samples"]
        threshold = parameters.get("threshold", 0.5)
        
        # Simulate adaptive sampling based on criteria
        sample_indices = []
        current_sample = 0
        
        while current_sample < max_samples:
            # Simulate some condition based on criteria
            if random.random() > threshold:
                sample_indices.append(current_sample)
            current_sample += 1
        
        return {
            "status": "success",
            "strategy": "adaptive",
            "sample_size": len(sample_indices),
            "max_samples": max_samples,
            "criteria": criteria,
            "threshold": threshold,
            "sample_indices": sample_indices,
            "sampling_fraction": len(sample_indices) / max_samples
        }
    
    def _execute_monte_carlo_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Monte Carlo sampling."""
        iterations = parameters["iterations"]
        distribution = parameters["distribution"]
        dist_params = parameters.get("parameters", {})
        
        # Generate Monte Carlo samples
        if distribution == "normal":
            mean = dist_params.get("mean", 0)
            std = dist_params.get("std", 1)
            samples = np.random.normal(mean, std, iterations)
        elif distribution == "uniform":
            low = dist_params.get("low", 0)
            high = dist_params.get("high", 1)
            samples = np.random.uniform(low, high, iterations)
        elif distribution == "exponential":
            scale = dist_params.get("scale", 1)
            samples = np.random.exponential(scale, iterations)
        else:
            # Default to uniform distribution
            samples = np.random.uniform(0, 1, iterations)
        
        return {
            "status": "success",
            "strategy": "monte_carlo",
            "iterations": iterations,
            "distribution": distribution,
            "parameters": dist_params,
            "samples": samples.tolist(),
            "sample_mean": float(np.mean(samples)),
            "sample_std": float(np.std(samples))
        }
    
    def _execute_bootstrap_sampling(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute bootstrap sampling."""
        data = parameters["data"]
        bootstrap_samples = parameters["bootstrap_samples"]
        sample_size = parameters.get("sample_size", len(data))
        
        # Generate bootstrap samples
        bootstrap_results = []
        for i in range(bootstrap_samples):
            # Resample with replacement
            bootstrap_sample = random.choices(data, k=sample_size)
            bootstrap_results.append(bootstrap_sample)
        
        return {
            "status": "success",
            "strategy": "bootstrap",
            "bootstrap_samples": bootstrap_samples,
            "sample_size": sample_size,
            "original_data_size": len(data),
            "bootstrap_results": bootstrap_results,
            "bootstrap_means": [float(np.mean(sample)) for sample in bootstrap_results]
        }
    
    def create_strategy(self, strategy_id: str, strategy_type: str, description: str,
                       parameters: List[str], validation: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new sampling strategy."""
        self.sampling_strategies[strategy_id] = {
            "type": strategy_type,
            "description": description,
            "parameters": parameters,
            "validation": validation or {}
        }
        
        return {"status": "success", "strategy_id": strategy_id}
    
    def update_strategy(self, strategy_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing sampling strategy."""
        if strategy_id not in self.sampling_strategies:
            return {"status": "error", "message": "Strategy not found"}
        
        self.sampling_strategies[strategy_id].update(updates)
        return {"status": "success", "strategy_id": strategy_id}
    
    def delete_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Delete a sampling strategy."""
        if strategy_id not in self.sampling_strategies:
            return {"status": "error", "message": "Strategy not found"}
        
        del self.sampling_strategies[strategy_id]
        return {"status": "success", "strategy_id": strategy_id}


# ============================================================================
# MCP Sampling Tools
# ============================================================================

sampling_manager = SamplingManager()


@tool("list_sampling_strategies")
async def list_sampling_strategies_tool(strategy_type: str = None) -> Dict[str, Any]:
    """
    List available sampling strategies.
    
    Args:
        strategy_type: Optional strategy type filter
        
    Returns:
        Dictionary containing list of sampling strategies
    """
    try:
        strategies = sampling_manager.list_strategies(strategy_type)
        return {
            "status": "success",
            "strategies": strategies,
            "count": len(strategies),
            "strategy_type": strategy_type
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_sampling_strategy")
async def get_sampling_strategy_tool(strategy_id: str) -> Dict[str, Any]:
    """
    Get a specific sampling strategy by ID.
    
    Args:
        strategy_id: ID of the strategy to retrieve
        
    Returns:
        Dictionary containing strategy details
    """
    try:
        strategy = sampling_manager.get_strategy(strategy_id)
        if strategy:
            return {
                "status": "success",
                "strategy": strategy
            }
        else:
            return {"status": "error", "message": "Strategy not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("validate_sampling_parameters")
async def validate_sampling_parameters_tool(strategy_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate sampling parameters for a strategy.
    
    Args:
        strategy_id: ID of the strategy to validate for
        parameters: Dictionary of parameters to validate
        
    Returns:
        Dictionary containing validation result
    """
    try:
        validation_result = sampling_manager.validate_parameters(strategy_id, parameters)
        return {
            "status": "success",
            "strategy_id": strategy_id,
            "validation": validation_result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("execute_sampling")
async def execute_sampling_tool(strategy_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute sampling with the specified strategy and parameters.
    
    Args:
        strategy_id: ID of the strategy to use
        parameters: Dictionary of parameters for the strategy
        
    Returns:
        Dictionary containing sampling results
    """
    try:
        result = sampling_manager.execute_sampling(strategy_id, parameters)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("create_sampling_strategy")
async def create_sampling_strategy_tool(strategy_id: str, strategy_type: str, description: str,
                                      parameters: List[str], validation: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a new sampling strategy.
    
    Args:
        strategy_id: Unique ID for the strategy
        strategy_type: Type of the strategy
        description: Description of the strategy
        parameters: List of parameters for the strategy
        validation: Optional validation rules
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = sampling_manager.create_strategy(strategy_id, strategy_type, description, parameters, validation)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("update_sampling_strategy")
async def update_sampling_strategy_tool(strategy_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing sampling strategy.
    
    Args:
        strategy_id: ID of the strategy to update
        updates: Dictionary of updates to apply
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = sampling_manager.update_strategy(strategy_id, updates)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("delete_sampling_strategy")
async def delete_sampling_strategy_tool(strategy_id: str) -> Dict[str, Any]:
    """
    Delete a sampling strategy.
    
    Args:
        strategy_id: ID of the strategy to delete
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = sampling_manager.delete_strategy(strategy_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("sampling_info")
async def sampling_info_tool() -> Dict[str, Any]:
    """
    Get information about the sampling system.
    
    Returns:
        Dictionary containing system information
    """
    try:
        return {
            "status": "success",
            "total_strategies": len(sampling_manager.sampling_strategies),
            "strategy_types": list(set(strategy["type"] for strategy in sampling_manager.sampling_strategies.values())),
            "available_strategies": list(sampling_manager.sampling_strategies.keys()),
            "supported_distributions": ["normal", "uniform", "exponential"],
            "supported_constraints": ["positive_integer", "non_negative_integer", "float_between_0_and_1", 
                                   "dict_with_positive_values", "list_of_positive_integers"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# MCP Server Implementation
# ============================================================================

@server("mcp-sampling-server")
class MCPSamplingServer:
    """MCP Server for sampling management."""
    
    def __init__(self):
        self.server = Server("mcp-sampling-server")
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server."""
        print(f"Initializing MCP Sampling server: {options.server_name} v{options.server_version}")
        print(f"Available strategies: {len(sampling_manager.sampling_strategies)}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down MCP Sampling server")


async def main():
    """Main function to run the MCP sampling server."""
    server = MCPSamplingServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-sampling-server",
                server_version="1.0.0",
                capabilities=server.server.get_capabilities(
                    notification_options=None,
                    request_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

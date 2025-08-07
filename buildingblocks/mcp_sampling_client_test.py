"""
MCP Sampling Client Test

This example demonstrates how to use the MCP sampling server with various
sampling strategies and parameters.

Requirements:
- pip install mcp
"""

import asyncio
import json
from typing import Dict, Any, List
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_sampling_server():
    """Test the MCP sampling server with various strategies."""
    
    # Connect to the sampling server
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_sampling_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-sampling-client") as session:
            print("Connected to MCP Sampling Server")
            
            # Test 1: List all sampling strategies
            print("\n=== Test 1: List Sampling Strategies ===")
            result = await session.call_tool("list_sampling_strategies", {})
            print(f"Available strategies: {json.dumps(result, indent=2)}")
            
            # Test 2: Get specific strategy details
            print("\n=== Test 2: Get Strategy Details ===")
            result = await session.call_tool("get_sampling_strategy", {"strategy_id": "random"})
            print(f"Random strategy: {json.dumps(result, indent=2)}")
            
            # Test 3: Validate parameters
            print("\n=== Test 3: Validate Parameters ===")
            params = {"sample_size": 10, "population_size": 100}
            result = await session.call_tool("validate_sampling_parameters", {
                "strategy_id": "random",
                "parameters": params
            })
            print(f"Validation result: {json.dumps(result, indent=2)}")
            
            # Test 4: Execute random sampling
            print("\n=== Test 4: Execute Random Sampling ===")
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "random",
                "parameters": {"sample_size": 10, "population_size": 100}
            })
            print(f"Random sampling result: {json.dumps(result, indent=2)}")
            
            # Test 5: Execute stratified sampling
            print("\n=== Test 5: Execute Stratified Sampling ===")
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "stratified",
                "parameters": {
                    "strata": {"group_a": 40, "group_b": 35, "group_c": 25},
                    "sample_size": 20,
                    "population_size": 100
                }
            })
            print(f"Stratified sampling result: {json.dumps(result, indent=2)}")
            
            # Test 6: Execute systematic sampling
            print("\n=== Test 6: Execute Systematic Sampling ===")
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "systematic",
                "parameters": {
                    "interval": 5,
                    "population_size": 100,
                    "start_index": 2
                }
            })
            print(f"Systematic sampling result: {json.dumps(result, indent=2)}")
            
            # Test 7: Execute cluster sampling
            print("\n=== Test 7: Execute Cluster Sampling ===")
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "cluster",
                "parameters": {
                    "clusters": [20, 30, 25, 25],
                    "clusters_to_select": 2,
                    "population_size": 100
                }
            })
            print(f"Cluster sampling result: {json.dumps(result, indent=2)}")
            
            # Test 8: Execute adaptive sampling
            print("\n=== Test 8: Execute Adaptive Sampling ===")
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "adaptive",
                "parameters": {
                    "criteria": "high_value",
                    "max_samples": 50,
                    "threshold": 0.7
                }
            })
            print(f"Adaptive sampling result: {json.dumps(result, indent=2)}")
            
            # Test 9: Execute Monte Carlo sampling
            print("\n=== Test 9: Execute Monte Carlo Sampling ===")
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "monte_carlo",
                "parameters": {
                    "iterations": 1000,
                    "distribution": "normal",
                    "parameters": {"mean": 0, "std": 1}
                }
            })
            print(f"Monte Carlo sampling result: {json.dumps(result, indent=2)}")
            
            # Test 10: Execute bootstrap sampling
            print("\n=== Test 10: Execute Bootstrap Sampling ===")
            sample_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            result = await session.call_tool("execute_sampling", {
                "strategy_id": "bootstrap",
                "parameters": {
                    "data": sample_data,
                    "bootstrap_samples": 100,
                    "sample_size": 10
                }
            })
            print(f"Bootstrap sampling result: {json.dumps(result, indent=2)}")
            
            # Test 11: Create custom strategy
            print("\n=== Test 11: Create Custom Strategy ===")
            result = await session.call_tool("create_sampling_strategy", {
                "strategy_id": "custom_weighted",
                "strategy_type": "weighted",
                "description": "Custom weighted sampling strategy",
                "parameters": ["weights", "sample_size"],
                "validation": {
                    "required": ["weights", "sample_size"],
                    "constraints": {
                        "sample_size": "positive_integer",
                        "weights": "list_of_positive_floats"
                    }
                }
            })
            print(f"Create strategy result: {json.dumps(result, indent=2)}")
            
            # Test 12: Get sampling system info
            print("\n=== Test 12: Get System Info ===")
            result = await session.call_tool("sampling_info", {})
            print(f"System info: {json.dumps(result, indent=2)}")
            
            print("\n=== All Tests Completed ===")


async def test_sampling_validation():
    """Test parameter validation with invalid parameters."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_sampling_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-sampling-validation-client") as session:
            print("\n=== Testing Parameter Validation ===")
            
            # Test invalid parameters
            test_cases = [
                {
                    "name": "Negative sample size",
                    "strategy_id": "random",
                    "parameters": {"sample_size": -5, "population_size": 100}
                },
                {
                    "name": "Missing required parameter",
                    "strategy_id": "random",
                    "parameters": {"sample_size": 10}
                },
                {
                    "name": "Invalid threshold value",
                    "strategy_id": "adaptive",
                    "parameters": {"criteria": "test", "max_samples": 10, "threshold": 1.5}
                },
                {
                    "name": "Invalid strata format",
                    "strategy_id": "stratified",
                    "parameters": {"strata": "invalid", "sample_size": 10, "population_size": 100}
                }
            ]
            
            for test_case in test_cases:
                print(f"\n--- {test_case['name']} ---")
                result = await session.call_tool("validate_sampling_parameters", {
                    "strategy_id": test_case["strategy_id"],
                    "parameters": test_case["parameters"]
                })
                print(f"Validation result: {json.dumps(result, indent=2)}")


async def test_sampling_comparison():
    """Compare different sampling strategies on the same population."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_sampling_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-sampling-comparison-client") as session:
            print("\n=== Comparing Sampling Strategies ===")
            
            population_size = 1000
            sample_size = 100
            
            strategies = [
                {
                    "name": "Random Sampling",
                    "strategy_id": "random",
                    "parameters": {"sample_size": sample_size, "population_size": population_size}
                },
                {
                    "name": "Systematic Sampling",
                    "strategy_id": "systematic",
                    "parameters": {"interval": 10, "population_size": population_size}
                },
                {
                    "name": "Stratified Sampling",
                    "strategy_id": "stratified",
                    "parameters": {
                        "strata": {"strata_1": 400, "strata_2": 350, "strata_3": 250},
                        "sample_size": sample_size,
                        "population_size": population_size
                    }
                }
            ]
            
            for strategy in strategies:
                print(f"\n--- {strategy['name']} ---")
                result = await session.call_tool("execute_sampling", {
                    "strategy_id": strategy["strategy_id"],
                    "parameters": strategy["parameters"]
                })
                
                if result["status"] == "success":
                    print(f"Sample size: {result['sample_size']}")
                    print(f"Sampling fraction: {result['sampling_fraction']:.3f}")
                    if "sample_indices" in result:
                        print(f"First 10 indices: {result['sample_indices'][:10]}")
                else:
                    print(f"Error: {result['message']}")


async def main():
    """Main function to run all sampling tests."""
    print("Starting MCP Sampling Client Tests")
    
    try:
        # Run basic tests
        await test_sampling_server()
        
        # Run validation tests
        await test_sampling_validation()
        
        # Run comparison tests
        await test_sampling_comparison()
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")


if __name__ == "__main__":
    asyncio.run(main())

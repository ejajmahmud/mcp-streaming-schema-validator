"""CLI for mcp-streaming-schema-validator."""
import sys
import argparse
from .validator import MCPStreamingSchemaValidator


def main():
    parser = argparse.ArgumentParser(description="MCP Streaming Schema Validator CLI")
    parser.add_argument("--demo", action="store_true", help="Run schema validator demo")
    args = parser.parse_args()

    if args.demo:
        val = MCPStreamingSchemaValidator()
        valid_req = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "read_file"}}
        bad_req = {"jsonrpc": "1.0", "id": 2, "method": "ping"}

        r1 = val.validate_message(valid_req)
        r2 = val.validate_message(bad_req)

        print(f"[+] Valid MCP Request: is_valid={r1.is_valid}")
        print(f"[*] Bad MCP Request: is_valid={r2.is_valid} (Error: '{r2.error}')")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()

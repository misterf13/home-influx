#!/home/fgarcia/testenv/bin/python3
import argparse
import asyncio
import json
import libeagle

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch device data from the Eagle connection.")
    parser.add_argument('-n', '--hostname', type=str, required=True, help='Hostname of the Eagle device')
    parser.add_argument('-u', '--username', type=str, required=True, help='Username for the connection')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password for the connection')

    return parser.parse_args()

async def main():
    args = parse_args()
    async with libeagle.Connection(
        hostname=args.hostname,
        username=args.username,
        password=args.password,
        debug=False
    ) as conn:
        devices = await conn.device_list()
        assert len(devices) > 0

        for device in devices:
            query = await conn.device_query(device["HardwareAddress"])

            if "Components" not in query or not query["Components"]:
                continue

            for component in query["Components"]:
                variables = component.get("Variables", {})
                if not isinstance(variables, dict) or not variables:
                    continue

                keys_to_extract = {
                    "zigbee:InstantaneousDemand": "InstantaneousDemand",
                    "zigbee:Price": "Price",
                    "zigbee:PriceCurrency": "PriceCurrency",
                    "zigbee:PriceTier": "PriceTier",
                    "zigbee:Multiplier": "Multiplier",
                    "zigbee:Divisor": "Divisor",
                    "zigbee:CurrentSummationDelivered": "CurrentSummationDelivered",
                    "zigbee:PriceStartTime" : "PriceStartTime",
                    "zigbee:PriceDuration" : "PriceDuration"
                }

                # Convert and clean values
                extracted_data = {
                    "HardwareAddress": query.get("HardwareAddress"),
                    "ConnectionStatus": query.get("ConnectionStatus")
                }

                for zigbee_key, new_key in keys_to_extract.items():
                    if zigbee_key in variables:
                        value = variables[zigbee_key]
                        if value.isdigit():  # Convert to int if possible
                            extracted_data[new_key] = int(value)
                        else:
                            try:
                                extracted_data[new_key] = float(value)
                            except ValueError:
                                extracted_data[new_key] = value  # Keep as string if conversion fails

                print(json.dumps(extracted_data, indent=2))

# Run the async main function
asyncio.run(main())

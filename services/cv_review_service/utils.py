def build_endpoint_data(name="None", path="", description="", method="") -> dict:
    description = f"endpoint for {name}" if description == "" else description
    return {name: "/", "description": description, "method": method}

long_to_short = {
    "(x-1.5)^2 + sin(5x)": "func_3",
    "(x-2)^2 + 1": "func_1",
    "plateau_function": "func_2.1",
    "asymmetric_function": "func_2.2",
}


def get_short_func_name(func_name: str):
    if func_name.startswith("Plat"):
        return "func_2.1"
    if func_name.startswith("Asym"):
        return "func_2.2"
    return long_to_short.get(func_name, func_name.replace(" ", "_"))

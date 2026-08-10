import typing


def file_reader(config_txt: str) -> dict[str, str]:
    config = {}
    with open(config_txt, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def validator(pre_config: dict[str, str]) -> dict[str, typing.Any]:
    config: dict[str, typing.Any] = {}

    try:
        width = int(pre_config.get("WIDTH", 0))
        height = int(pre_config.get("HEIGHT", 0))
    except ValueError:
        raise ValueError(
            "WIDTH e HEIGHT devem ser números inteiros válidos."
        )

    if width <= 0 or height <= 0:
        raise ValueError(
            "WIDTH e HEIGHT devem ser números maiores que 0."
        )

    config["WIDTH"] = width
    config["HEIGHT"] = height

    for key, val in pre_config.items():
        if key in ("WIDTH", "HEIGHT"):
            continue

        elif key in ("ENTRY", "EXIT"):
            try:
                parts = val.split(",")

                if len(parts) != 2:
                    raise ValueError("Esperado exatamente duas coordenadas.")

                x = int(parts[0].strip())
                y = int(parts[1].strip())
                coord = (x, y)

            except ValueError as error:
                raise ValueError(
                    f"{key} deve estar no formato 'x,y'. Erro: {error}"
                )

            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(
                    f"A coordenada {key} {coord} está fora "
                    f"dos limites ({width}x{height})!"
                )

            config[key] = coord

        elif key == "PERFECT":
            val_lower = val.strip().lower()

            if val_lower in ("true", "1", "yes"):
                config["PERFECT"] = True

            elif val_lower in ("false", "0", "no"):
                config["PERFECT"] = False

            else:
                raise ValueError(
                    f"PERFECT deve ser True ou False, recebido: '{val}'"
                )

        elif key == "OUTPUT_FILE":
            if not val.strip():
                raise ValueError(
                    "OUTPUT_FILE não pode estar vazio."
                )

            config["OUTPUT_FILE"] = val.strip()

        else:
            config[key] = val

    return config


if __name__ == "__main__":
    config = file_reader("config.txt")
    print(config)

    config = validator(config)
    print()
    print("Convertendo dicionário...")
    print()

    print(config)

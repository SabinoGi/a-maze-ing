import typing


class ConfigParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def file_reader(self) -> dict[str, str]:
        """Reads the configuration file defined in self.file_path."""
        config = {}
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config

    def validator(self, pre_config: dict[str, str]) -> dict[str, typing.Any]:
        """Validates and converts values from the configuration dictionary."""
        config: dict[str, typing.Any] = {}

        try:
            width = int(pre_config.get("WIDTH", 0))
            height = int(pre_config.get("HEIGHT", 0))
        except ValueError:
            raise ValueError(
                "WIDTH and HEIGHT must be valid integers."
            )

        if width <= 0 or height <= 0:
            raise ValueError(
                "WIDTH and HEIGHT must be numbers greater than 0."
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
                        raise ValueError(
                            "Expected exactly two coordinates."
                        )

                    x = int(parts[0].strip())
                    y = int(parts[1].strip())
                    coord = (x, y)

                except ValueError as error:
                    raise ValueError(
                        f"{key} must be in 'x,y' format. Error: {error}"
                    )

                if not (0 <= x < width and 0 <= y < height):
                    raise ValueError(
                        f"The coordinate {key} {coord} is out of "
                        f"bounds ({width}x{height})!"
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
                        f"PERFECT must be True or False, received: '{val}'"
                    )

            elif key == "OUTPUT_FILE":
                if not val.strip():
                    raise ValueError(
                        "OUTPUT_FILE cannot be empty."
                    )

                config["OUTPUT_FILE"] = val.strip()

            elif key == "SEED":
                seed = pre_config["SEED"].strip()

                if seed.lower() in ("none", ""):
                    config["SEED"] = None
                else:
                    try:
                        config["SEED"] = int(seed)
                    except ValueError:
                        raise ValueError("SEED must be an integer or None!")

            else:
                config[key] = val

        return config

    def parse(self) -> dict[str, typing.Any]:
        """Executes reading and validation sequentially."""
        pre_config = self.file_reader()
        return self.validator(pre_config)

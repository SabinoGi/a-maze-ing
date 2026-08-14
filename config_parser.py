import typing


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""
    pass


class ConfigParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def file_reader(self) -> dict[str, str]:
        """Reads the configuration file."""
        config = {}

        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(
                        f"Invalid configuration syntax: '{line}'"
                    )

                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip()

                if not key:
                    raise ConfigError(
                        f"Invalid configuration syntax: '{line}'"
                    )

                config[key] = value

        return config

    def validator(
        self,
        pre_config: dict[str, str]
    ) -> dict[str, typing.Any]:
        """Validates and converts configuration values."""

        required_keys = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "PERFECT",
            "OUTPUT_FILE",
            "SEED",
        }

        allowed_keys = required_keys | {"SEED"}

        missing_keys = required_keys - pre_config.keys()

        if missing_keys:
            raise ConfigError(
                "Missing mandatory key(s): "
                + ", ".join(sorted(missing_keys))
            )

        unknown_keys = pre_config.keys() - allowed_keys

        if unknown_keys:
            raise ConfigError(
                "Unknown configuration key(s): "
                + ", ".join(sorted(unknown_keys))
            )

        config: dict[str, typing.Any] = {}

        # WIDTH and HEIGHT
        try:
            width = int(pre_config["WIDTH"])
            height = int(pre_config["HEIGHT"])
        except ValueError:
            raise ConfigError(
                "WIDTH and HEIGHT must be valid integers."
            )

        if width <= 0 or height <= 0:
            raise ConfigError(
                "WIDTH and HEIGHT must be numbers greater than 0."
            )

        config["WIDTH"] = width
        config["HEIGHT"] = height

        # ENTRY and EXIT
        for key in ("ENTRY", "EXIT"):
            val = pre_config[key]

            try:
                parts = val.split(",")

                if len(parts) != 2:
                    raise ValueError(
                        "Expected exactly two coordinates."
                    )

                x = int(parts[0].strip())
                y = int(parts[1].strip())

            except ValueError as error:
                raise ConfigError(
                    f"{key} must be in 'x,y' format. Error: {error}"
                )

            if not (0 <= x < width and 0 <= y < height):
                raise ConfigError(
                    f"The coordinate {key} ({x}, {y}) is out of "
                    f"bounds ({width}x{height})!"
                )

            config[key] = (x, y)

        # PERFECT
        val_lower = pre_config["PERFECT"].strip().lower()

        if val_lower in ("true", "1", "yes"):
            config["PERFECT"] = True

        elif val_lower in ("false", "0", "no"):
            config["PERFECT"] = False

        else:
            raise ConfigError(
                f"PERFECT must be True or False, received: "
                f"'{pre_config['PERFECT']}'"
            )

        # OUTPUT_FILE
        output_file = pre_config["OUTPUT_FILE"].strip()

        if not output_file:
            raise ConfigError(
                "OUTPUT_FILE cannot be empty."
            )

        config["OUTPUT_FILE"] = output_file

        # SEED
        if "SEED" in pre_config:
            seed = pre_config["SEED"].strip()

            if seed.lower() in ("none", ""):
                config["SEED"] = None

            else:
                try:
                    config["SEED"] = int(seed)
                except ValueError:
                    raise ConfigError(
                        "SEED must be an integer or None!"
                    )

        return config

    def parse(self) -> dict[str, typing.Any]:
        """Reads and validates the configuration file."""
        pre_config = self.file_reader()
        return self.validator(pre_config)

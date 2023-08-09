import sys
import carvekit
import photoid
import prepartial
import tempfile


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with tempfile.NamedTemporaryFile(), tempfile.NamedTemporaryFile() as stage_1, stage_2:
        photoid.process(input_path, stage_1.name)
        carvekit.process(stage_1.name, stage_2.name)
        prepartial(stage_2.name, output_path)
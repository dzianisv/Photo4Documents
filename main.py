import sys
import carvekit
import photoid
import tempfile


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with tempfile.NamedTemporaryFile() as temp_file:
        carvekit.process(input_path, temp_file.name)
        photoid.process(temp_file.name, output_path)
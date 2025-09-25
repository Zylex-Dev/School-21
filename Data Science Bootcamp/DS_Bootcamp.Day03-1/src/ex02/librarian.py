import os
import subprocess
import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


class Librarian:
    """
    A class for managing library installation and archiving of a virtual environment.
    """

    def __init__(
        self, libraries: list[str], rec_file: str, env_path: str, archive_name: str
    ):
        self.libraries = libraries
        self.rec_file = rec_file
        self.env_path = env_path
        self.archive_name = archive_name

    @staticmethod
    def check_virtualenv() -> None:
        if "VIRTUAL_ENV" not in os.environ:
            raise Exception("This script must be run inside a virtual environment.")

    def archive_virtualenv(self) -> None:
        if not os.path.exists(self.env_path):
            logging.error(f"Directory {self.env_path} does not exist")
            return

        try:
            subprocess.run(["tar", "cvzf", self.archive_name, self.env_path])
            logging.info(f"Virtual environment archieved to {self.archive_name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to archive virtual environment: {e}")

    def create_requirements_file(self) -> None:
        with open(self.rec_file, "w") as f:
            for library in self.libraries:
                f.write(f"{library}\n")
        logging.info(
            f"File '{self.rec_file}' was created with the following libraries: {self.libraries}"
        )

    def install_libraries(self) -> None:
        if not os.path.exists(self.rec_file):
            logging.error(f"File '{self.rec_file}' does not exist")
            return

        logging.info(f"Installing libraries from '{self.rec_file}...'")
        try:
            result = subprocess.run(
                ["pip", "install", "-r", self.rec_file], capture_output=True, text=True
            )
            logging.debug(result.stdout)
            logging.info("Libraries installed successfully")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install libraries: {e.stderr}")

    def save_installed_libraries(self) -> None:
        with open(self.rec_file, "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f)
        logging.info(f"All installed libraries saved to '{self.rec_file}'")

    def display_requirements_file(self) -> None:
        try:
            with open(self.rec_file, "r") as f:
                file_content = f.read()
            logging.info(f"Contents of {self.rec_file}:\n{'-' * 40}\n{file_content}")
        except FileNotFoundError:
            logging.error(f"File {self.rec_file} was not found")

    def run(self) -> None:
        try:
            self.check_virtualenv()
            self.create_requirements_file()
            self.install_libraries()
            self.save_installed_libraries()
            self.display_requirements_file()
        except Exception as e:
            logging.error(f"{e}")


if __name__ == "__main__":
    setup_logging()
    librarian = Librarian(
        libraries=["beautifulsoup4", "pytest"],
        rec_file="requirements.txt",
        env_path="../../sigfrydj",
        archive_name="env.tar.gz",
    )
    librarian.run()
    # librarian.archive_virtualenv() -- Additional use

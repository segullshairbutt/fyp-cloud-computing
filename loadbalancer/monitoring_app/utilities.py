import subprocess
import os

JAR_FILE_PATH = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], "openapi-generator-cli.jar")


def create_server_stub(config_file, project_directory):
    print(config_file)
    output_directory = os.path.join(project_directory, "server-stubs", str(config_file.split('/')[-1]).split('.')[0])
    subprocess.call(["java", "-jar", JAR_FILE_PATH, "generate", "-i", config_file, "-g", "spring", "-o", output_directory])
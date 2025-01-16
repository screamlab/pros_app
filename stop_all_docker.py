import subprocess


def stop_all_docker_containers():
    try:
        # Execute the docker stop command
        result = subprocess.run(
            "docker stop $(docker ps -aq)",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print("All Docker containers have been stopped successfully.")
        print("Output:", result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("Error occurred while stopping Docker containers.")
        print("Error message:", e.stderr.strip())


if __name__ == "__main__":
    stop_all_docker_containers()

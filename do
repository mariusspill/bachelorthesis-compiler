#!/usr/bin/env bash

show_help() {
  echo "USAGE"
  echo ""
  echo "  ./do [OPTIONS] COMMAND"
  echo ""
  echo "OPTIONS"
  echo ""
  echo "  --no-docker, -nd     Run commands without using Docker."
  echo "  -h, --help           Show this help message."
  echo ""
  echo "COMMAND"
  echo ""
  echo "  shell                opens a shell inside the docker container with"
  echo "                       gcc, qemu, python3, and vim installed and"
  echo "                       the project directory mounted as a volume"
  echo ""
  echo "  compile PATH [ARGS]  compiles python file PATH to tmp directory in docker"
  echo "                       container. Optionally, pass additional command line"
  echo "                       arguments ARGS to your compiler.py"
  echo ""
  echo "  run PATH [ARGS]      like 'compile', but runs the generated file with"
  echo "                       qemu after compilation"
  echo ""
  echo "  test [PATH]          runs all tests in docker container or a specific test"
  echo "                       file/folder relative to the tests directory"
  echo ""
  echo "  docker-rebuild       rebuilds the docker image (in case the Dockerfile"
  echo "                       has changed)"
  echo ""
  echo "  clean                clears tmp directory"
  exit 1
}

USE_DOCKER=true
WORK_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
REPO_ROOT=$(dirname "$WORK_DIR")  # Root of the repository
IMAGE_NAME="cc-riscv"

# Check for .no-docker file in the root of the repository
if [ -f "$REPO_ROOT/.no-docker" ]; then
  USE_DOCKER=false
fi

while [[ "$1" == --* || "$1" == -* ]]; do
  case "$1" in
    --no-docker|-nd)
      USE_DOCKER=false
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Invalid option: $1"
      exit 1
      ;;
  esac
done

function ensure_docker_image {
  if ! sudo docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    echo "docker image not found! building the image.."
    sudo docker build -t "$IMAGE_NAME" "$WORK_DIR"
  fi
}

function execute_command {
  local cmd="$1"
  shift
  if [ "$USE_DOCKER" = true ]; then
    ensure_docker_image
    sudo docker run -e "PYTHONHASHSEED=1" -it --rm -v "$WORK_DIR:/cc" -w /cc -u "$(id -u):$(id -g)" "$IMAGE_NAME" bash -c "$cmd"
  else
    bash -c "$cmd"
  fi
}

case "$1" in
  shell)
    execute_command "bash"
    ;;
  compile)
    FILE_NAME="$(basename "$2" .py)"
    mkdir -p "$WORK_DIR/tmp"
    execute_command "python3 src/compiler.py -i \"$2\" -o \"tmp/$FILE_NAME.S\" ${@:3}"
    ;;
  run)
    FILE_NAME="$(basename "$2" .py)"
    mkdir -p "$WORK_DIR/tmp"
    execute_command "python3 src/compiler.py -i \"$2\" -o \"tmp/$FILE_NAME.S\" ${@:3} && \
      riscv64-linux-gnu-gcc -static \"tmp/$FILE_NAME.S\" \"runtime/runtime.c\" -o \"tmp/$FILE_NAME\" && \
      qemu-riscv64-static \"tmp/$FILE_NAME\""
    ;;
  test)
    TEST_PATH=${2:-""}
    if [ -n "$TEST_PATH" ]; then
      execute_command "python3 tests/test.py --src \"tests/$TEST_PATH\" ${@:3}"
    else
      execute_command "python3 tests/test.py ${@:2}"
    fi
    ;;
  docker-rebuild)
    echo "Rebuilding the docker image..."
    sudo docker build -t "$IMAGE_NAME" "$WORK_DIR"
    ;;
  clean)
    rm -rf "$WORK_DIR/tmp/"
    ;;
  *)
    echo "Invalid command line arguments. Run with --help for documentation."
    exit 1
    ;;
esac

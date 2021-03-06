workflow "CI" {
    on = "push"
    resolves = [
        "lint",
        "test-35",
        "test-36",
        "test-37"
    ]
}

action "lint" {
    uses = "docker://python:3.7-alpine"
    runs = "./actions_runner.sh"
    args = "pip install black && make lint"
}

action "test-35" {
    uses = "docker://python:3.5-alpine"
    runs = "./actions_runner.sh"
    args = "make install test"
}

action "test-36" {
    uses = "docker://python:3.6-alpine"
    runs = "./actions_runner.sh"
    args = "make install test"
}

action "test-37" {
    uses = "docker://python:3.7-alpine"
    runs = "./actions_runner.sh"
    args = "make install test"
}

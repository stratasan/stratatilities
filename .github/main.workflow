workflow "CI" {
    on = "push"
    resolves = [
        "lint",
        "test-35",
        "test-36",
        "test-37"
    ]
}

action "test-35" {
    uses = "docker://python:3.5-alpine"
    runs = "/bin/sh"
    args = "cd ${GITHUB_WORKSPACE}; apk add make; make install test"
}

action "test-36" {
    uses = "./actions/test-36"
    args = "cd ${GITHUB_WORKSPACE}; make install test"
}

action "test-37" {
    uses = "./actions/test-37"
    args = "cd ${GITHUB_WORKSPACE}; make install test"
}

action "lint" {
    uses = "./actions/lint"
    args = "cd ${GITHUB_WORKSPACE}; make lint"
}

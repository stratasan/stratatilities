workflow "CI" {
    on = "push"
    resolves = [
        "test-35",
        "test-36",
        "test-37"
    ]
}

action "lint" {
    uses = "./actions/lint"
    args = "cd ${GITHUB_WORKSPACE}; make lint"
}

action "test-35" {
    needs = ["lint"]
    uses = "docker://python:3.5-alpine"
    runs = ["/bin/sh", "-c"]
    args = "apk add make; make install test"
}

action "test-36" {
    needs = ["lint"]
    uses = "./actions/test-36"
    args = "cd ${GITHUB_WORKSPACE}; apk add make; make install test"
}

action "test-37" {
    needs = ["lint"]
    uses = "./actions/test-37"
    args = "cd ${GITHUB_WORKSPACE}; make install test"
}

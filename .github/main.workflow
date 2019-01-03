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
    uses = "./actions/test-35"
    args = "cd ${GITHUB_WORKSPACE}; make test"
}

action "test-36" {
    uses = "./actions/test-36"
    args = "cd ${GITHUB_WORKSPACE}; make test"
}

action "test-37" {
    uses = "./actions/test-37"
    args = "cd ${GITHUB_WORKSPACE}; make test"
}

action "lint" {
    uses = "./actions/lint"
    args = "cd ${GITHUB_WORKSPACE}; make lint"
}
